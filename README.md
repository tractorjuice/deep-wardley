# Deep Wardley - Ultimate Wardley Chatbot

A Streamlit-based conversational AI application that helps users learn about and understand Wardley Mapping concepts using information from Simon Wardley's book and other resources.
It covers Wardley Mapping, Doctrine, Landscape, Climatic Patterns and Gameplays.

## Features

- Interactive chat interface for learning about Wardley Mapping
- Context-aware responses using LangGraph and RAG (Retrieval Augmented Generation)
- Two-step query processing (question rewriting and response generation)
- Conversation memory to maintain context of discussions
- British English language support
- Stream-based response generation for better UX
- Debug mode for development and troubleshooting

## Prerequisites

- Python 3.8+
- Streamlit
- Portkey AI account and API key
- OpenAI API key
- Pinecone account and configured index

## Required Environment Variables

The following secrets need to be configured in your Streamlit secrets:

```
PORTKEY_API_KEY=your_portkey_api_key
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
google_portkey_config=your_google_portkey_config
index_name=your_pinecone_index_name
prompt_template=your_prompt_template_id
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tractorjuice/deep-wardley.git
cd deep-wardley
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in `.streamlit/secrets.toml`

## Required Dependencies

- streamlit
- langchain-community
- langchain-core
- langchain-openai
- langchain-pinecone
- langchain
- langgraph
- portkey_ai

## Usage

1. Start the Streamlit application:
```bash
streamlit run streamlit_app.py
```

2. Start chatting with the assistant about Wardley Mapping

## Key Features

### Chat Interface
- Streaming responses for better user experience
- Chat history preservation across sessions
- Memory management with clear chat and clear memory options

### Knowledge Base
- Vector search using Pinecone for accurate information retrieval
- Context-aware responses with LangGraph workflow
- Question rewriting for improved search accuracy
- Professional tone maintenance

### Development Features
- Debug mode for testing and development
- Source viewing in debug mode
- Session tracking for analytics
- Comprehensive error handling

## Architecture

The application uses a combination of:
- LangGraph for orchestrating the conversation workflow
- Pinecone for vector storage and retrieval
- Portkey AI for API routing and monitoring
- Streamlit for the web interface
- LangChain for building the RAG pipeline

## Memory Management

The application maintains conversation context using:
- ConversationBufferWindowMemory with 10-message window
- Session-based message history
- Ability to clear both chat and memory states

## Limitations

- Requires active internet connection
- API key rate limits apply
- Memory limited to last 10 interactions
- Responses strictly limited to Wardley Mapping domain

## Contributing

Contributions to improve the Deep Wardley chatbot are welcome. Please feel free to submit pull requests or open issues to discuss proposed changes or enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Simon Wardley for the original Wardley Mapping concept and book
- Streamlit for the web framework
- OpenAI for the language model capabilities
- Portkey AI for API management
- Pinecone for vector search capabilities
- LangChain and LangGraph for the RAG and workflow components