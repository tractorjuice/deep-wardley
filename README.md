# Ultimate Wardley Chatbot (Deep-Wardley)

A Streamlit-based conversational AI application that helps users learn about and understand Wardley Mapping concepts using information from Simon Wardley's book and other resources.
It covers Wardley Mapping, Doctrine, Landscripe, Climatic Patterns and Gameplays.

## Features

- Interactive chat interface for learning about Wardley Mapping
- Context-aware responses using vector search
- Conversation memory to maintain context
- British English language support
- Stream-based response generation
- Debug mode for development

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
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd ultimate-wardley-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in `.streamlit/secrets.toml`:
```toml
PORTKEY_API_KEY = "your_portkey_api_key"
OPENAI_API_KEY = "your_openai_api_key"
PINECONE_API_KEY = "your_pinecone_api_key"
```

## Required Dependencies

- streamlit
- langchain-openai
- langchain-pinecone
- portkey-ai

## Usage

1. Start the Streamlit application:
```bash
streamlit run streamlit_app.py
```

2. Start chatting with the assistant about Wardley Mapping

## Features

### Chat Interface
- Streaming responses for better user experience
- Chat history preservation
- Memory management with clear chat and clear memory options

### Knowledge Base
- Vector search using Pinecone
- Context-aware responses
- British English language support
- Professional tone maintenance

### Development Features
- Debug mode for testing
- Source viewing in debug mode
- Session tracking
- Comprehensive error handling

## Architecture

The application uses a combination of:
- Pinecone for vector storage and retrieval
- Portkey AI for API routing and monitoring
- Streamlit for the web interface

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

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the [LICENSE NAME] - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Simon Wardley for the original Wardley Mapping concept and book
- Streamlit for the web framework
- OpenAI for the language model capabilities
- Portkey AI for API management
- Pinecone for vector search capabilities