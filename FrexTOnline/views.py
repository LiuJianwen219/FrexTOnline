from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect

from Login.models import User
from Course.models import Course

# Create your views here.
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
    with open("test_mq.yaml", "r") as f:
        response = FileResponse(f.read())
        response['Content-Type'] = 'application/stream'
        response['Content-Disposition'] = 'attachment;filename={0}'.format(file.file_name)
        return response