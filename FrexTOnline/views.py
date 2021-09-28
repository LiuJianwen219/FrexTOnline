from django.http import HttpResponse
from django.shortcuts import render, redirect

from Login.models import User
from Course.models import Course

# Create your views here.
def test(request):
    user = User.objects.get(request.session.get('u_uid'))
    c = Course(user=user, name="数字逻辑")
    c.save()
    return render(request, 'Home/home.html')


def favicon(request):
    return HttpResponse("favicon.ico")


def home(request):
    return redirect('/home/')
