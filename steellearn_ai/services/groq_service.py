import os

from groq import Groq
from dotenv import load_dotenv
from ..services.document_search import search_documents

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def get_ai_response(question):

   
    document_context = search_documents(question)

    if document_context.strip():

        system_prompt = f"""
You are SteelLearn AI.

You are an AI-powered Learning & Development Assistant.

Use the uploaded company training documents below as your PRIMARY source of information.

If the answer exists in the document,
answer only from the document.

If the document does not contain the answer,
say:

"I couldn't find this information in the uploaded training documents."

Training Documents:

{document_context}
"""

    else:

        system_prompt = """
You are SteelLearn AI.

You are an AI-powered Learning & Development Assistant.

No training documents were found.

Politely inform the user that no relevant document is available.
"""

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],

        temperature=0.2,
    )

    return completion.choices[0].message.content