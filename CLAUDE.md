# Deep Wardley Project Guide

## Commands
- Run app: `streamlit run streamlit_app.py`
- Install dependencies: `pip install -r requirements.txt`
- Check types: `mypy streamlit_app.py`
- Format code: `black .`
- Lint code: `flake8 .`

## Code Style
- **Imports**: Group standard library, third-party, and project imports
- **Naming**: snake_case for variables/functions, PascalCase for classes, ALL_CAPS for constants
- **Types**: Use type hints with `typing` module, especially for function parameters/returns
- **Error handling**: Use specific exceptions with descriptive messages
- **Documentation**: Use docstrings for functions/methods ("""Description""")
- **Formatting**: Max line length 100 characters
- **State Management**: Use Streamlit session_state for persistent variables
- **Comments**: Add comments for complex logic, not obvious behavior

## Project Structure
- Single streamlit_app.py for the main application
- LangGraph for conversation flow management
- Pinecone for vector storage
- Portkey for API management