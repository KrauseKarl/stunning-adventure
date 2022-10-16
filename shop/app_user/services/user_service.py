from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def get_user(request):
    print('++++++++++++++++++++++++++++user id = ', request.user.pk)
    try:
        return User.objects.get(id=request.user.id)
    except ObjectDoesNotExist:
        return None
