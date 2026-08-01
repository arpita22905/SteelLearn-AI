import os

from groq import Groq
from dotenv import load_dotenv

from documents.rag.retriever import DocumentRetriever

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def get_ai_response(question):
    """
    Generate AI response using RAG + Groq.
    """

    try:

        retriever = DocumentRetriever()

        retrieved_documents = retriever.retrieve(
            query=question,
            k=4
        )

    except Exception:

        retrieved_documents = []

    if retrieved_documents:

        document_context = "\n\n".join(
            [doc.page_content for doc in retrieved_documents]
        )

        system_prompt = f"""
You are SteelLearn AI.

You are an AI-powered Learning & Development Assistant for industrial training.

You must answer ONLY using the retrieved document context below.

Rules:

1. Use ONLY the information provided in the context.
2. Never invent or assume information.
3. Do NOT use outside knowledge.
4. If the answer is not available in the context, reply exactly:

"I couldn't find this information in the uploaded training documents."

-----------------------------
DOCUMENT CONTEXT

{document_context}

-----------------------------
"""

    else:

        system_prompt = """
You are SteelLearn AI.

No relevant document context was found.

Reply exactly:

"I couldn't find this information in the uploaded training documents."
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
        max_tokens=1024,
    )

    return completion.choices[0].message.content