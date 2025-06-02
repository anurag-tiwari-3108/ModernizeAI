# Code Companion for Legacy Systems

A modern AI-powered agent to help you understand, annotate, and refactor legacy code (COBOL, Fortran, ABAP, etc.) into modern languages like Python, Java, C#, and Go.

## Features

- **Automatic Language Detection** for legacy code
- **Inline Annotation** with clear comments
- **Pseudocode Generation** in plain English
- **Modern Refactor Suggestions** (Python, Java, C#, Go)
- **Explainability Mode** for refactor reasoning
- **Syntax Highlighting** and file upload support in UI

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```sh
   make install
   ```

3. **Set your OpenAI API key**
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=your-openai-api-key
     ```

4. **Run the application**
   ```sh
   make run
   ```

5. **Run tests**
   ```sh
   make test
   ```

## Usage

- Paste or upload legacy code in the Gradio UI.
- Select target language and options.
- View annotated code, pseudocode, refactored code, and explanations.

## Project Structure

- `frontend_gradio.py` - Gradio web UI
- `agent_pipeline.py` - Core agent logic and LLM abstraction
- `test_agent_pipeline.py` - Unit and integration tests
- `requirements.txt` - Python dependencies
- `Makefile` - Common tasks

## Extending

- Add more legacy languages in `agent_pipeline.py`
- Swap LLM providers by extending the LLM client abstraction

---

**For questions or contributions, open an issue or pull request.**
