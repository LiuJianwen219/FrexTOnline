import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from Class.models import TheClass
from Course.models import Course, CourseTemplate


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
