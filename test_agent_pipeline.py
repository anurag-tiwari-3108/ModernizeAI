import unittest
from agent_pipeline import CodeCompanionAgent, LLMClientBase

class DummyLLMClient(LLMClientBase):
    def chat(self, prompt: str) -> str:
        return "dummy response"

class TestCodeCompanionAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CodeCompanionAgent(DummyLLMClient())

    def test_detect_language_cobol(self):
        cobol_code = "IDENTIFICATION DIVISION.\nPROGRAM-ID. HELLO."
        self.assertEqual(self.agent.detect_language(cobol_code), "COBOL")

    def test_detect_language_fortran(self):
        fortran_code = "      SUBROUTINE HELLO"
        self.assertEqual(self.agent.detect_language(fortran_code), "FORTRAN")

    def test_pipeline(self):
        code = "IDENTIFICATION DIVISION.\nPROGRAM-ID. HELLO."
        result = self.agent.process(code)
        self.assertIn("dummy response", result["annotated_code"])

if __name__ == "__main__":
    unittest.main()
