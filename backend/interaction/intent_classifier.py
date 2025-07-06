import google.generativeai as genai

# ---- IntentClassifier ----
class IntentClassifier:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite-001")

    
    def classify(self, user_input: str) -> str:
        GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]

        if user_input.strip().lower() in GREETINGS:
            return "greeting"

        prompt = f"""
        You are a classification assistant for a university chatbot. Your task is to label the user's intent based on their input.

        Possible categories:
        - greeting
        - information_request
        - clarification
        - escalation
        - goodbye

        Respond with only the label.

        User Input:
        "{user_input}"
        """

        response = self.model.generate_content(prompt)
        return response.text.strip().lower()

