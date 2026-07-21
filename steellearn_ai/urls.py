from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("chat/", views.chat, name="chat"),
    path("clear-chat/", views.clear_chat, name="clear_chat"),
    path("new-chat/", views.new_chat, name="new_chat"),
    path("upload/",views.upload_document,name="upload_document",),
    path("summary/<int:document_id>/",views.summarize_pdf,name="summary",),
    path("documents/",views.document_library,name="document_library",),
    path("quiz/<int:document_id>/",views.generate_document_quiz,name="document_quiz",),
]