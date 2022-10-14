from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def get_user(request):
    try:
        return User.objects.filter(user=request.user).first()
    except ObjectDoesNotExist:
        return None
