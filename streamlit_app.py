import uuid, re
import streamlit as st
from typing import Annotated
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL, Portkey
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_pinecone import PineconeVectorStore
from langchain.tools.retriever import create_retriever_tool
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import HumanMessage
from langchain import hub

portkey_api_key = st.secrets["PORTKEY_API_KEY"]
openai_api_key = st.secrets["OPENAI_API_KEY"]
google_portkey_config = st.secrets["google_portkey_config"]
index_name = st.secrets["index_name"]
prompt_template = st.secrets["prompt_template"]
DEBUG = False

def extract_final_question(response_text):
    """Extract the question from <final_question> tags."""
    match = re.search(r'<final_question>(.*?)</final_question>', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

portkey_headers = createHeaders(
    api_key=portkey_api_key,
    config=google_portkey_config,
    trace_id = st.session_state.session_id,
    metadata = {"_user": st.session_state.session_id}
    )

# Page config
st.set_page_config(
    page_title="Ultimate Wardley Chatbot",
    page_icon=":material/chess:"
)

tags = ["Book Creator"]
temperature = 0.3

# Initialize vector store and retriever in session state
if "datastore" not in st.session_state:
    st.session_state.datastore = PineconeVectorStore(
        index_name=index_name,
        embedding=OpenAIEmbeddings()
    )

if "retriever" not in st.session_state:
    st.session_state.retriever = st.session_state.datastore.as_retriever(
        search_kwargs={"k": 5}
    )

# Initialize memory in session state
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(
        k=10,  # Keep last 10 interactions
        return_messages=True,
        memory_key="chat_history",
        output_key="output"
    )

# Create retriever tool
wardley_map_book = create_retriever_tool(
    st.session_state.retriever,
    "Wardley Mapping Books",
    "Search and return information about Wardley Mapping",
)

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title
st.title("Ultimate Wardley Chatbot")
st.markdown("""
This assistant helps you learn about Wardley Mapping using information from Simon Wardley's book and other resources.
""")

# Setup LangGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize graph and LLM
#@st.cache_resource
def initialize_graph(_openai_api_key, _portkey_api_key, _retriever_tool):
    graph_builder = StateGraph(State)

    llm = ChatOpenAI(
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=portkey_headers,
        api_key="PORTKEY_API_KEY",
        temperature=temperature,
        tags=tags + [f"session_{st.session_state.session_id}"]  # Add session_id to tags
    )

    # Rewrite question prompt
    rewrite_question_prompt = hub.pull("rewrite_question")
    # Create a prompt template that uses retrieved context and chat history
    prompt = hub.pull(prompt_template)

    def chatbot(state: State):
        # Get the user's message from the last message in state
        last_message = state["messages"][-1]
        user_message = last_message.content

        # Get chat history from memory
        chat_history = st.session_state.memory.load_memory_variables({})["chat_history"]
        chat_history_str = "\n".join([
            f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}"
            for msg in chat_history
        ])

        # Rewrite question for RAG
        with st.spinner("Thinking ... Processing question ..."):
            chain = rewrite_question_prompt | llm
            rewrite_response = chain.invoke({
                "chat_history": chat_history_str,
                "question": user_message
            })

            # Extract the rewritten question from the response
            rewritten_question = extract_final_question(rewrite_response.content)
            st.sidebar.write(rewritten_question)
            if rewritten_question is None:
                # If no tags found, use original question
                rewritten_question = user_message
                if DEBUG:
                    st.warning("No <final_question> tags found in rewrite response")

        # Use the retriever tool to get relevant context
        with st.spinner("Thinking ... Checking Sources ..."):
            retrieved_docs = st.session_state.retriever.invoke(rewritten_question)

        context = "\n\n".join(doc.page_content for doc in retrieved_docs)

        # Create the final prompt with context and history
        with st.spinner("Thinking ... Writing Answer"):
            chain = prompt | llm
            response = chain.invoke({
                "context": context,
                "chat_history": chat_history_str,
                "question": rewritten_question  # Use the rewritten question here
            })

        # Save the interaction to memory
        st.session_state.memory.save_context(
            {"input": user_message},  # Save original user message to memory
            {"output": response.content}
        )

        if DEBUG:
            # Show sources in an expander
            with st.expander("📚 Sources Used", expanded=False):
                for i, doc in enumerate(retrieved_docs, 1):
                    st.markdown(f"**Source {i}:**")
                    st.markdown(doc.page_content)
                    if hasattr(doc, 'metadata') and doc.metadata:
                        st.markdown("*Metadata:*")
                        st.json(doc.metadata)
                    st.divider()

            # Show rewritten question
            with st.expander("🔄 Question Processing", expanded=False):
                st.markdown("**Original Question:**")
                st.markdown(user_message)
                st.markdown("**Rewritten Question:**")
                st.markdown(rewritten_question)

        return {"messages": [response]}

    def do_nothing(state: State):
        return {"messages": [response]}

    def do_something(state: State):
        return {"messages": [response]}

    def do_check(state: State):
        return "Pass"

    graph_builder.add_node("chatbot", chatbot)

    graph_builder.add_node("do nothing", do_nothing)
    graph_builder.add_node("do something", do_something)
    graph_builder.add_conditional_edges("chatbot", do_check, {"Fail": "do nothing", "Pass": "do something"})
    graph_builder.add_edge("do something", END)
    graph_builder.add_edge("do nothing", END)

    graph_builder.set_entry_point("chatbot")
    #graph_builder.set_finish_point("chatbot")

    return graph_builder.compile()

# Initialize the graph
graph = initialize_graph(openai_api_key, portkey_api_key, wardley_map_book)

# Show workflow centred in sidebar
st.sidebar.write("Graph Model:")
st.sidebar.image(graph.get_graph().draw_mermaid_png())

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if question := st.chat_input("Ask me about Wardley Mapping"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Get bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Stream the response
        for event in graph.stream({"messages": [("user", question)]}):
            for value in event.values():
                # Handle both string and message object responses
                if isinstance(value["messages"][-1], str):
                    response = value["messages"][-1]
                else:
                    response = value["messages"][-1].content
                full_response = response
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add buttons for memory management
col1, col2 = st.columns(2)
with col1:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
with col2:
    if st.button("Clear Memory"):
        st.session_state.memory.clear()
        st.session_state.messages = []
        st.rerun()