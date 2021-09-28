import json

from django.http import HttpResponse
from django.shortcuts import render
from Login.models import User
from Course.models import Course, CourseTemplate, CourseTemplateExperiment
# Create your views here.


def create_template(request):
    print(request.POST["courseId"])
    print(request.POST["templateName"])
    course = Course.objects.get(uid=request.POST["courseId"])  # find course
    newTemplate = CourseTemplate(course=course, name=request.POST["templateName"])
    newTemplate.save()

    data = {"state": "OK"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def create_experiment(request):
    print(request.POST["courseId"])
    print(request.POST["templateId"])
    print(request.POST["templateExpName"])
    # course = Course.objects.get(id=request.POST["courseId"])
    template = CourseTemplate.objects.get(uid=request.POST["templateId"])  # find template
    classExp = CourseTemplateExperiment(course_template=template, name=request.POST["templateExpName"])  # create a class exp
    classExp.save()

    data = {"state": "OK"}
    return HttpResponse(json.dumps(data), content_type='application/json')