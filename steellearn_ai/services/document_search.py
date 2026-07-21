from ..models import TrainingDocument


def search_documents(question):

    question_words = question.lower().split()

    best_chunks = []

    documents = TrainingDocument.objects.all()

    for document in documents:

        chunks = document.extracted_text.split("\n\n")

        for chunk in chunks:

            score = 0

            chunk_lower = chunk.lower()

            for word in question_words:
                if word in chunk_lower:
                    score += 1

            if score > 0:
                best_chunks.append((score, chunk))

    
    best_chunks.sort(reverse=True, key=lambda x: x[0])

   
    return "\n\n".join(chunk for score, chunk in best_chunks[:3])