import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from Class.models import TheClass, ClassStudent
from Course.models import Course, CourseTemplate
from Login.models import User


# Create your views here.
def create_class(request):
    print(request.POST)
    print(request.POST["courseId"])
    print(request.POST["templateId"])
    print(request.POST["newClassName"])
    print(request.POST["newClassStartTime"])
    print(request.POST["newClassEndTime"])

    course = Course.objects.get(uid=request.POST["courseId"])
    courseTemplate = CourseTemplate.objects.get(uid=request.POST["templateId"])

    start = datetime.strptime(request.POST["newClassStartTime"], '%Y-%m-%d')
    end = datetime.strptime(request.POST["newClassEndTime"], '%Y-%m-%d')
    the_class = TheClass(course=course, course_template=courseTemplate, name=request.POST["newClassName"],
                         start_time=start, end_time=end)
    the_class.save()

    data = {"state": "OK"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def add_student(request):
    print(request.POST)
    print(request.POST["classId"])
    print(request.POST["studentNumbers"])
    theClass = TheClass.objects.get(uid=request.POST['classId'])
    numbers = request.POST["studentNumbers"].split(",")
    for n in numbers:
        try:
            user = User.objects.get(name=n)
        except User.DoesNotExist:
            data = {"state": "ERROR", "info": "学生{n}不存在！"}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            cs = ClassStudent(user=user, the_class=theClass)
            cs.save()

    data = {"state": "OK"}
    return HttpResponse(json.dumps(data), content_type='application/json')

