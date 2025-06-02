# How to Host ModernizeAI on Hugging Face Spaces

You can deploy your Gradio app on [Hugging Face Spaces](https://huggingface.co/spaces) for free. Here’s how:

## 1. Prepare Your Repository

- Make sure your code is in a public GitHub repository.
- Your main UI file should be named `app.py` or specify it in `README.md` (Hugging Face looks for `app.py` by default).
- Move or copy your main Gradio script to `app.py`:
  ```bash
  cp app/frontend_gradio.py app.py
  ```

## 2. Add a `requirements.txt`

- Ensure all dependencies are listed in `requirements.txt` (you already have this).

## 3. Remove or Adjust .env Usage

- Hugging Face Spaces does **not** support `.env` files for secrets.
- Instead, use [Hugging Face Secrets](https://huggingface.co/docs/hub/spaces-secrets) for API keys.
- In your code, replace `os.getenv("OPENAI_API_KEY")` with:
  ```python
  import os
  openai_api_key = os.environ.get("OPENAI_API_KEY")
  ```
- Set your secrets in the Hugging Face Space settings UI after deployment.

## 4. Push to Hugging Face

- Create a new Space at https://huggingface.co/spaces.
- Choose **Gradio** as the SDK.
- Clone the new Space repo:
  ```bash
  git clone https://huggingface.co/spaces/<your-username>/<your-space-name>
  cd <your-space-name>
  ```
- Copy your code and files into this repo:
  ```bash
  cp -r ../ModernizeAI/* .
  ```
- Commit and push:
  ```bash
  git add .
  git commit -m "Initial commit for Hugging Face Space"
  git push
  ```

## 5. Set Secrets in the Space UI

- Go to your Space on Hugging Face.
- Click **Settings > Secrets**.
- Add your API keys (e.g., `OPENAI_API_KEY`, `GROK_API_KEY`, `MISTRAL_API_KEY`).

## 6. Launch

- Your app will automatically build and launch.
- Visit your Space URL to use ModernizeAI in the cloud!

---

**Note:**  
- If your app uses subfolders (like `ui/`), update imports or move everything to the root, or set `PYTHONPATH` in your Space.
- Hugging Face Spaces have resource/time limits for free users.
- For persistent storage or advanced features, see Hugging Face documentation.

**Reference:**  
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
