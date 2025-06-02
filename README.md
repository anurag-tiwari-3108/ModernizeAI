---
title: ModernizeAI
emoji: 🚀
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 5.32.1
app_file: app/frontend_gradio.py
pinned: false
---

# ModernizeAI Code Refactoring Agent

ModernizeAI is an AI-powered tool designed to transform legacy code into modern programming languages. It provides a user-friendly interface for pasting or uploading code, selecting options, and receiving refactored code with explanations.

## Features

- **Automatic Language Detection** for legacy code.
- **Inline Annotation** with clear comments.
- **Pseudocode Generation** in plain English.
- **Modern Refactor Suggestions** (Python, Java, C#, Go).
- **Explainability Mode** for refactor reasoning.
- **Syntax Highlighting** and file upload support in UI.
- **Multiple AI Providers**: OpenAI, Grok, Mistral (default), and others (can be extended).
- **Customizable Options**: Choose target language and LLM provider.

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/anurag-tiwari-3108/ModernizeAI.git
   cd ModernizeAI
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variables**
   - For local development, create a `.env` file in the root directory.
   - For Hugging Face Spaces, set secrets in the Space UI (Settings > Secrets).
   - Add your API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key
     GROK_API_KEY=your_grok_api_key
     MISTRAL_API_KEY=your_mistral_api_key
     ```

## Usage

1. **Run the application locally**
   ```bash
   make run
   ```
   or directly:
   ```bash
   python3 app/frontend_gradio.py
   ```

2. **Run on Hugging Face Spaces**
   - **Important:** Set `app_file: app/frontend_gradio.py` in your README config block (see above) so Hugging Face runs the correct entry point.
   - Ensure your imports use the correct module paths (e.g., `from agent_pipeline import ...` works if you run from the repo root and `app/frontend_gradio.py` is the entry point).
   - Push to your Hugging Face Space.
   - **Set your API keys as secrets in the Space settings**:  
     Go to your Space, click on "Settings" > "Secrets", and add the following keys:
     ```
     OPENAI_API_KEY=your_openai_api_key
     GROK_API_KEY=your_grok_api_key
     MISTRAL_API_KEY=your_mistral_api_key
     ```
     These secrets are required for the app to access the LLM providers.  
     **If you do not set `OPENAI_API_KEY`, you will get an error about missing the API key.**

3. **Open the application in your browser**
   - The application will launch at `http://localhost:7860`.

4. **Interact with the UI**
   - Paste or upload your legacy code.
   - Select the target language and LLM provider.
   - Click "Run Agent" to process the code.

## Supported AI Providers

- **OpenAI**: Default provider for processing code.
- **Grok**: Alternative provider for code refactoring.
- **Mistral**: Lightweight and efficient processing.
- **Extendable**: Add support for other providers like DeepSeek, Llama, etc.

## Project Structure

- `app/frontend_gradio.py` - Gradio-based web UI for user interaction.
- `app/agent_pipeline.py` - Core agent logic and LLM abstraction.
- `app/tests/` - Unit and integration tests.
- `requirements.txt` - Python dependencies.
- `Makefile` - Common tasks for setup, testing, and running the application.

## Extending

- **Add More Legacy Languages**: Extend `agent_pipeline.py` to support additional legacy languages.
- **Swap LLM Providers**: Extend the LLM client abstraction in `agent_pipeline.py` to integrate new AI providers.
- **UI Customization**: Modify `frontend_gradio.py` and `custom_css` for advanced UI enhancements.

## Screenshots

### Hero Section
![alt text](image.png)

## Dependencies

- Python 3.8+
- Gradio
- OpenAI Python SDK
- python-dotenv
- pygments

## Development & Testing

- **Run tests**:
  ```bash
  make test
  ```
- **Lint code**:
  ```bash
  make lint
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
