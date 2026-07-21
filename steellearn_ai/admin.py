from django.contrib import admin
from .models import TrainingDocument
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    search_fields = ("title",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "role", "timestamp")
    list_filter = ("role",)
    search_fields = ("content",)

@admin.register(TrainingDocument)
class TrainingDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "uploaded_at",
    )

    search_fields = (
        "title",
    )