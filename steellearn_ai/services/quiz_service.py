import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_quiz(text):

    prompt = f"""
You are an AI Learning & Development assistant.

Generate exactly 10 multiple choice questions from the training document.

Return ONLY valid JSON.

The format MUST be exactly:

[
  {{
    "question":"What is PPE?",
    "options":[
      "Helmet",
      "Gloves",
      "Personal Protective Equipment",
      "Shoes"
    ],
    "answer":2
  }}
]

Rules:

- Generate exactly 10 questions.
- Every question must have exactly 4 options.
- answer must be the correct option index:
  0 = first option
  1 = second option
  2 = third option
  3 = fourth option
- Questions should test understanding.
- Use ONLY information present in the document.
- Do NOT use markdown.
- Do NOT explain anything.
- Return ONLY valid JSON.
- Do not wrap JSON inside ```.

Training Document:

{text}
"""

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],

        temperature=0.3,
    )

    response = completion.choices[0].message.content.strip()

    
    response = response.replace("```json", "")
    response = response.replace("```", "").strip()

    try:
        quiz = json.loads(response)
        return quiz

    except json.JSONDecodeError:
        print(response)
        return []