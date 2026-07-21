from django import forms

from .models import TrainingDocument


class DocumentUploadForm(forms.ModelForm):

    class Meta:

        model = TrainingDocument

        fields = [
            "title",
            "file",
        ]