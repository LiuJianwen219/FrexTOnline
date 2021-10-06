import json

from django.http import HttpResponse

from Class.models import TheClass
from Course.models import Course, CourseTemplate, CourseTemplateExperiment
from FrexTOnline.views import response_ok, response_error
from File.models import CourseFile


# Create your views here.
def create_template(request):
    print(request.POST["courseId"])
    print(request.POST["templateName"])
    course = Course.objects.get(uid=request.POST["courseId"])  # find course
    newTemplate = CourseTemplate(course=course, name=request.POST["templateName"])
    newTemplate.save()
    # TODO: maybe drop the same name instance
    return HttpResponse(json.dumps(response_ok()), content_type='application/json')


def delete_template(request):
    print(request.POST["courseId"])
    print(request.POST["templateId"])
    template = CourseTemplate(uid=request.POST["templateId"])
    classExp = CourseTemplateExperiment.objects.filter(course_template=template)
    if len(classExp) > 0:
        return HttpResponse(json.dumps(response_error("请先删除模板下面的所有实验")), content_type='application/json')
    classes = TheClass.objects.filter(course_template=template)
    if len(classes) > 0:
        return HttpResponse(json.dumps(response_error("还有班级在使用模板")), content_type='application/json')
    template.delete()
    return HttpResponse(json.dumps(response_ok()), content_type='application/json')


def create_experiment(request):
    print(request.POST["courseId"])
    print(request.POST["templateId"])
    print(request.POST["templateExpName"])
    # course = Course.objects.get(id=request.POST["courseId"])
    template = CourseTemplate.objects.get(uid=request.POST["templateId"])  # find template
    classExp = CourseTemplateExperiment(course_template=template, name=request.POST["templateExpName"])
    classExp.save()
    # TODO: maybe drop the same name instance
    return HttpResponse(json.dumps(response_ok()), content_type='application/json')


def delete_experiment(request):
    print(request.POST["courseId"])
    print(request.POST["templateId"])
    print(request.POST["templateExpId"])
    classExp = CourseTemplateExperiment.objects.filter(uid=request.POST["templateExpId"])
    if len(classExp) == 0:
        return HttpResponse(json.dumps(response_error("实验已删除，请刷新")), content_type='application/json')
    else:
        courseFiles = CourseFile.objects.filter(course_template_experiment=classExp[0])
        for file in courseFiles:
            file.delete()
        classExp[0].delete()
    return HttpResponse(json.dumps(response_ok()), content_type='application/json')
