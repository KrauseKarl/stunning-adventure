from django import forms
from app_item.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('review',)
