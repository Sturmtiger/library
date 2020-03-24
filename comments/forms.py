from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].label = False

    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {"text": forms.TextInput(attrs={"placeholder": "leave a comment"})}
