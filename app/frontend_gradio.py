import gradio as gr
from agent_pipeline import CodeCompanionAgent, OpenAILLMClient, get_llm_client
import openai
import os

# Remove dotenv usage for Hugging Face Spaces compatibility
# from dotenv import load_dotenv
# load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def run_agent(code, file, explain, target_lang, provider):
    # Prefer file input if provided
    if file is not None:
        if hasattr(file, "read"):
            file.seek(0)
            code = file.read().decode("utf-8")
        elif isinstance(file, str):
            code = file
    code = code or ""
    llm_client = get_llm_client(provider)
    agent = CodeCompanionAgent(llm_client)
    result = agent.process(code, explain, target_lang)
    return (
        result["language"],
        result["annotated_code"],
        result["pseudocode"],
        result["refactored_code"],
        result["explanation"] or "",
    )

# Advanced custom CSS for tile-based design
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

body, .gradio-container {
    font-family: 'Poppins', sans-serif !important;
    background: linear-gradient(120deg, #f8fafc 0%, #e2e8f0 100%) !important; /* Light mode background */
    color: #1e293b !important; /* Dark text for light mode */
    min-height: 100vh;
    overflow-x: hidden;
}

.card {
    background: rgba(255, 255, 255, 0.9); /* Brighter card background for light mode */
    border-radius: 1.5rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    margin-bottom: 2rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.gr-button {
    background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important; /* Darker button gradient */
    color: #fff !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    border-radius: 2rem !important;
    padding: 0.8rem 2rem !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.gr-button:hover {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
}

.gr-input, .gr-textbox, .gr-dropdown, .gr-checkbox {
    border-radius: 1rem !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
    background: rgba(255, 255, 255, 0.9) !important; /* Brighter input background */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    color: #1e293b !important; /* Dark text for light mode */
}

.gr-code {
    background: rgba(255, 255, 255, 0.9) !important; /* Brighter code background */
    border-radius: 1rem !important;
    padding: 1.5rem !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    color: #1e293b !important; /* Dark text for light mode */
    font-family: 'Poppins', monospace !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.gr-code:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

#hero-section h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #1e293b !important; /* Dark text for light mode */
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow for readability */
}

#hero-section p {
    font-size: 1.1rem;
    color: #475569 !important; /* Slightly lighter text for description */
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); /* Subtle shadow for readability */
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.HTML(
        """
        <div id="hero-section">
            <h1>ModernizeAI Code Refactoring Agent</h1>
            <p>Transform legacy code into modern languages with AI. Paste or upload your code, select your options, and get instant results with explanations and refactoring.</p>
        </div>
        """
    )
    with gr.Row():
        with gr.Column(scale=1, min_width=350):
            with gr.Group(elem_classes="card"):
                with gr.Tab("Paste Code"):
                    code_input = gr.Textbox(label="Legacy Code", lines=10, placeholder="Paste your legacy code here...")
                with gr.Tab("Upload File"):
                    file_input = gr.File(label="Upload Legacy Code File", file_types=[".txt", ".cob", ".for", ".abap", ".bas", ".pas", ".pl1", ".rpg"])
                explain_checkbox = gr.Checkbox(label="Explain Refactor", value=True)
                target_lang_dropdown = gr.Dropdown(["Python", "Java", "C#", "Go"], label="Target Language", value="Python")
                llm_provider_dropdown = gr.Dropdown(
                    choices=["OpenAI", "Grok", "Mistral"],
                    label="LLM Provider",
                    value="Mistral",
                    interactive=True,
                )
                run_button = gr.Button("Run Agent")
        with gr.Column(scale=2, min_width=400):
            with gr.Group(elem_classes="card"):
                detect_lang_output = gr.Textbox(label="Detected Language", interactive=False)
                annotated_code_output = gr.Code(label="Annotated Code", language="python")
                pseudocode_output = gr.Code(label="Pseudocode", language="python")
                refactored_code_output = gr.Code(label="Refactored Code", language="python")
                explanation_output = gr.Textbox(label="Explanation", interactive=False)

    run_button.click(
        run_agent,
        inputs=[
            code_input,
            file_input,
            explain_checkbox,
            target_lang_dropdown,
            llm_provider_dropdown,
        ],
        outputs=[
            detect_lang_output,
            annotated_code_output,
            pseudocode_output,
            refactored_code_output,
            explanation_output,
        ],
    )

demo.launch()
