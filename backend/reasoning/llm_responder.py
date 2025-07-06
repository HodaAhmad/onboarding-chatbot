# Step 3: Reasoning Layer - LLMResponder
# =======================================
# This module sends prompts to Gemini and returns the generated response.

import google.generativeai as genai

class LLMResponder:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite-001")

    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"[Error from LLM]: {str(e)}"


# ---- Example Usage ----
if __name__ == "__main__":
    responder = LLMResponder(api_key="your-api-key")
    test_prompt = "Explain what ECTS credits are."
    print(responder.generate(test_prompt))