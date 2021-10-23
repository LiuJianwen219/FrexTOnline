from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect

from Home.views import access_check_record
from Login.models import User
from Course.models import Course


# Create your views here.
def response_ok():
    return {"state": "OK"}


def response_error(info):
    return {"state": "ERROR", "info": info}


def test(request):
    user = User.objects.get(uid=request.session["u_uid"])
    c = Course(user=user, name="数字逻辑")
    c.save()
    return render(request, 'Home/home.html')


def favicon(request):
    return HttpResponse("favicon.ico")


def home(request):
    return redirect('/home/')


def resource(request):
    if access_check_record(request, "see", "查看资源信息"):
        return redirect("/")
    with open("resource.txt", "r") as f:
        return HttpResponse(f.read(), content_type="text/plain; charset=utf-8")
