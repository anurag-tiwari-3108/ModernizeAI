from typing import Dict, Any
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
import os
import requests

# Expanded mapping for more legacy languages
LEXER_LANGUAGE_MAP = {
    "COBOL": "COBOL",
    "FORTRAN": "FORTRAN",
    "ABAP": "ABAP",
    "PL/I": "PL/I",
    "PASCAL": "Pascal",
    "ADA": "Ada",
    "RPG": "RPG",
    "ASSEMBLY": "Assembly",
    "ALGOL": "Algol",
    "BASIC": "BASIC",
    "CLIPPER": "Clipper",
    "DCL": "DCL",
    "MUMPS": "MUMPS",
    "JCL": "JCL",
    "TACL": "TACL",
    "REXX": "REXX",
    "VHDL": "VHDL",
    "VERILOG": "Verilog",
    # Add more as needed
}

class LLMClientBase:
    """Abstract LLM client interface."""
    def chat(self, prompt: str) -> str:
        raise NotImplementedError("LLMClientBase is abstract.")

class OpenAILLMClient(LLMClientBase):
    def __init__(self, openai_module, model="gpt-4"):
        self.openai = openai_module
        self.model = model

    def chat(self, prompt: str) -> str:
        try:
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2048,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"LLM Error: {e}"

class GrokLLMClient(LLMClientBase):
    def __init__(self, api_key, model="grok-3-latest"):
        self.api_key = api_key
        self.model = model

    def chat(self, prompt: str) -> str:
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            "model": self.model,
            "stream": False,
            "temperature": 0,
        }
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            if resp.status_code == 403:
                return "Grok LLM Error: 403 Forbidden. Check your GROK_API_KEY and ensure it is valid and has access."
            resp.raise_for_status()
            result = resp.json()
            # The response format may change; adjust as needed
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Grok LLM Error: {e}"

class MistralLLMClient(LLMClientBase):
    def __init__(self, api_key, model="mistral-medium"):
        self.api_key = api_key
        self.model = model

    def chat(self, prompt: str) -> str:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "stream": False,
        }
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            if resp.status_code == 403:
                return "Mistral LLM Error: 403 Forbidden. Check your MISTRAL_API_KEY and ensure it is valid and has access."
            resp.raise_for_status()
            result = resp.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Mistral LLM Error: {e}"

class CodeCompanionAgent:
    def __init__(self, llm_client: LLMClientBase):
        self.llm_client = llm_client

    def detect_language(self, code: str) -> str:
        try:
            lexer = guess_lexer(code)
            name = lexer.name.upper()
            if name == "TEXT ONLY":
                raise ClassNotFound("Text only lexer detected")
            for key in LEXER_LANGUAGE_MAP:
                if key in name:
                    return LEXER_LANGUAGE_MAP[key]
            return name
        except ClassNotFound:
            # Fallback: simple heuristics
            if "IDENTIFICATION DIVISION" in code.upper():
                return "COBOL"
            if "PROGRAM" in code.upper() and "PROCEDURE DIVISION" in code.upper():
                return "COBOL"
            if "SUBROUTINE" in code.upper() or "COMMON" in code.upper():
                return "FORTRAN"
            if "DATA BEGIN" in code.upper() or "ENDMODULE" in code.upper():
                return "ABAP"
            return "Unknown"

    def _llm(self, prompt: str) -> str:
        return self.llm_client.chat(prompt)

    def annotate_code(self, code: str, language: str) -> str:
        prompt = (
            f"Add clear inline comments to the following {language} code to explain its logic. "
            "Keep the original code structure and add comments in the style of the language. "
            "If the language uses unusual comment syntax, use it appropriately.\n\n"
            f"{code}"
        )
        return self._llm(prompt)

    def generate_pseudocode(self, code: str, language: str) -> str:
        prompt = (
            f"Read the following {language} code and write high-level pseudocode in plain English. "
            "Focus on clarity and main logic steps. Use bullet points or numbered steps if helpful.\n\n"
            f"{code}"
        )
        return self._llm(prompt)

    def suggest_refactor(self, code: str, language: str, target_lang: str = "Python") -> str:
        prompt = (
            f"Refactor the following {language} code into clean, modular {target_lang} code. "
            "Use modern best practices, meaningful function and variable names, and add docstrings or comments as appropriate. "
            "If the code is procedural, suggest splitting into functions or classes where possible.\n\n"
            f"{code}"
        )
        return self._llm(prompt)

    def explain_refactor(self, code: str, language: str, refactored_code: str) -> str:
        prompt = (
            f"Explain the main changes and reasoning behind refactoring this {language} code into the following code:\n\n"
            f"Original {language} code:\n{code}\n\n"
            f"Refactored code:\n{refactored_code}\n\n"
            "Focus on modularity, readability, maintainability, and any language-specific improvements."
        )
        return self._llm(prompt)

    def process(self, code: str, explain: bool = False, target_lang: str = "Python") -> Dict[str, Any]:
        language = self.detect_language(code)
        annotated = self.annotate_code(code, language)
        pseudocode = self.generate_pseudocode(code, language)
        refactored = self.suggest_refactor(code, language, target_lang)
        explanation = self.explain_refactor(code, language, refactored) if explain else None
        # Richer output formatting
        return {
            "language": language,
            "annotated_code": f"--- Annotated {language} Code ---\n{annotated}",
            "pseudocode": f"--- Pseudocode ---\n{pseudocode}",
            "refactored_code": f"--- {target_lang} Refactor ---\n{refactored}",
            "explanation": f"--- Refactor Explanation ---\n{explanation}" if explanation else "",
        }

def get_llm_client(provider=None):
    if provider is None or provider == "OpenAI":
        import openai
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        return OpenAILLMClient(openai)
    elif provider == "Grok":
        grok_api_key = os.environ.get("GROK_API_KEY")
        return GrokLLMClient(grok_api_key)
    elif provider == "Mistral":
        mistral_api_key = os.environ.get("MISTRAL_API_KEY")
        return MistralLLMClient(mistral_api_key)
    else:
        raise ValueError("Unknown LLM provider")
