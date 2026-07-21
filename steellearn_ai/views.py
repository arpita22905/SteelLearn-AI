from django.shortcuts import render, redirect
from .forms_document import DocumentUploadForm
from .models import TrainingDocument
from .forms import ChatForm
from .services.groq_service import get_ai_response
from .utils.pdf_reader import extract_text_from_pdf
from .models import TrainingDocument
from .services.summary_service import summarize_document
from .models import TrainingDocument
from .services.quiz_service import generate_quiz
from django.http import JsonResponse


def home(request):
    return render(request, "steellearn_ai/home.html")

def chat(request):

    print("Method:", request.method)

    form = ChatForm()

    if "messages" not in request.session:
        request.session["messages"] = []

    messages = request.session["messages"]

    if request.method == "POST":

        print("POST received")

        form = ChatForm(request.POST)

        print("Form valid:", form.is_valid())

        if form.is_valid():

            question = form.cleaned_data["question"]

            answer = get_ai_response(question)

            print("Header:", request.headers.get("X-Requested-With"))

            return JsonResponse({
                "question": question,
                "answer": answer,
            })

    latest_document = TrainingDocument.objects.order_by("-uploaded_at").first()

    recent_documents = TrainingDocument.objects.order_by("-uploaded_at")[:5]

    return render(
        request,
        "steellearn_ai/chat.html",
        {
            "form": form,
            "messages": messages,
            "latest_document": latest_document,
            "recent_documents": recent_documents,
        },
    )
def clear_chat(request):

    request.session["messages"] = []

    return redirect("chat")


def new_chat(request):

    request.session["messages"] = []

    return redirect("chat")

def upload_document(request):

    if request.method == "POST":

        form = DocumentUploadForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            document = form.save()

            extracted_text = extract_text_from_pdf(
                document.file.path
            )

            document.extracted_text = extracted_text

            document.save()

            return redirect("chat")

    else:

        form = DocumentUploadForm()

    return render(
        request,
        "steellearn_ai/upload_document.html",
        {
            "form": form,
        },


    )

def summarize_pdf(request, document_id):

    document = TrainingDocument.objects.get(id=document_id)

    summary = summarize_document(document.extracted_text)

    return render(
        request,
        "steellearn_ai/document_summary.html",
        {
            "document": document,
            "summary": summary,
        },
    )



def document_library(request):

    documents = TrainingDocument.objects.all().order_by("-uploaded_at")

    return render(
        request,
        "steellearn_ai/document_library.html",
        {
            "documents": documents,
        },
    )

def generate_document_quiz(request, document_id):

    document = TrainingDocument.objects.get(id=document_id)

    quiz = generate_quiz(document.extracted_text)

    print(type(quiz))
    print(quiz)

    return render(
        request,
        "steellearn_ai/document_quiz.html",
        {
            "document": document,
            "quiz": quiz,
        },
    )