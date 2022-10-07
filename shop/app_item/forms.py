from django import forms
from django.utils.safestring import mark_safe

from app_item.models import Comment, Item


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('review',)


class ItemForm(forms.ModelForm):
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'magenta', 'white', 'black', ]

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        w = self.fields['color'].widget
        choices = []
        for key, value in w.choices:
            if key in self.colors:
                value = mark_safe(f'<div type="radio" style="background-color:{value};'
                                  f'height:20px; width:30px; position: relative; float: left;'
                                  f'border-radius: 20px; box-shadow: 0 0 5px; '
                                  f'margin: 0 5px; padding:2px"></div>')
                choices.append((key, value))
        w.choices = choices

    class Meta:
        model = Item
        fields = '__all__'
