
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqLLM:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found.")

        self.client = Groq(api_key=api_key)

    def generate_answer(self, question, documents):

        context = "\n\n".join(
            [doc.page_content for doc in documents]
        )

        prompt = f"""
You are SteelLearn AI, an AI Learning & Development Assistant.

Use ONLY the information provided in the context below.

If the answer cannot be found in the context,
reply exactly:

"I couldn't find the answer in the uploaded document."

------------------------
CONTEXT

{context}

------------------------

QUESTION

{question}

ANSWER
"""

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant for industrial learning and development."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,
            max_tokens=1024,
        )

        return response.choices[0].message.content