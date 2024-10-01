from django.core.serializers import serialize
from django.http import HttpResponse

from main.models import User


def get_employ(request):
    res = User.objects.all()[:10]
    json_data = serialize("json", res, fields=("username"))
    return HttpResponse(json_data, content_type="application/json")
