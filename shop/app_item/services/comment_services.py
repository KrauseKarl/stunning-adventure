from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView

from app_item.forms import CommentForm
from app_item.models import Comment


class AddComment:

    form_class = CommentForm

    def _get_item(self, ):
        pass
    @require_http_methods(["POST"])
    def add_comment(self, item, user):
        form = CommentForm
