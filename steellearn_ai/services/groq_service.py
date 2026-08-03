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

        # Create a fresh retriever so it always uses
        # the latest vector database after PDF upload.
        retriever = DocumentRetriever()

        retrieved_documents = retriever.retrieve(
            query=question
        )

        print("\n========== RETRIEVED DOCUMENTS ==========")
        print("Count:", len(retrieved_documents))

        for i, doc in enumerate(retrieved_documents):
            print(f"\nDocument {i + 1}")
            print(doc.page_content[:500])

    except Exception as e:

        print("Retriever Error:", e)

        retrieved_documents = []

    if retrieved_documents:

        document_context = "\n\n".join(
            doc.page_content
            for doc in retrieved_documents
        )

        system_prompt = f"""
You are SteelLearn AI.

You are an AI-powered Learning & Development Assistant for industrial training.

Answer ONLY using the retrieved document context below.

Rules:

1. Use ONLY the information present in the document context.
2. Never use outside knowledge.
3. Never invent information.
4. If the answer exists in the context, provide a complete explanation.
5. Use bullet points whenever appropriate.
6. If the context contains a definition, explain it clearly instead of replying with only a single phrase.
7. If the answer is NOT found in the context, reply exactly:

"I couldn't find this information in the uploaded training documents."

--------------------------------------------------
DOCUMENT CONTEXT

{document_context}

--------------------------------------------------
"""

    else:

        system_prompt = """
You are SteelLearn AI.

No relevant document context was found.

Reply exactly:

"I couldn't find this information in the uploaded training documents."
"""

    try:

        completion = client.chat.completions.create(

            # Keep your current model first.
            # Once everything works, you can switch to a faster model.
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

            max_tokens=700,
        )

        return completion.choices[0].message.content

    except Exception as e:

        print("Groq Error:", e)

        return "An error occurred while generating the response."