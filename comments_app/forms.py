from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    # text = forms.CharField(widget=forms.TextInput, label='')

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'leave a comment',
            })
        }
