
from django import forms


class ChatForm(forms.Form):

    question = forms.CharField(

        widget=forms.TextInput(

            attrs={

                "placeholder": "Ask SteelLearn AI...",

                "class": "chat-input",

                "autocomplete": "off",

            }

        )

    )