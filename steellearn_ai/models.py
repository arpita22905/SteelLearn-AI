from django.db import models


class Conversation(models.Model):

    ROLE_CHOICES = [
        ("New Employee", "New Employee"),
        ("Technician", "Technician"),
        ("Electrician", "Electrician"),
        ("Welder", "Welder"),
        ("Supervisor", "Supervisor"),
        ("HR", "HR"),
    ]

    title = models.CharField(max_length=255)

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="New Employee",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.role}: {self.content[:40]}"
    

class TrainingDocument(models.Model):

    title = models.CharField(max_length=255)

    file = models.FileField(upload_to="documents/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    extracted_text = models.TextField(blank=True)

    def __str__(self):
        return self.title