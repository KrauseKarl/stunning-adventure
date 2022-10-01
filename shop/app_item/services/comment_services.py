from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView

from app_item.forms import CommentForm
from app_item.models import Item, Comment


class AddComment:

    def _get_item(self, item):
        return get_object_or_404(Item, pk=item)

    def _get_form(self, **kwargs):
        return CommentForm(**kwargs)

    def add_comment(self, user, item, data):
        item = self._get_item(item)
        item.comments += 1
        item.save()
        form = CommentForm(data)
        new_comment = form.save(commit=False)
        new_comment.item = item

        new_comment.user = user
        new_comment.is_published = False
        new_comment.save()
        return new_comment

    def _get_permission(self, user, comment):
        if comment.user.id == user.id:
            del comment
            return True
        return False

    def _get_comment(self, comment_id):
        return Comment.objects.filter(id=comment_id)[0]

    def delete_comment(self, user, comment_id):
        comment = self._get_comment(comment_id)
        permission = self._get_permission(user, comment)
        if permission:
            comment.delete()
            return True
        return comment
