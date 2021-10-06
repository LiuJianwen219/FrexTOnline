import json
from datetime import datetime, date

from django.http import HttpResponse
from django.shortcuts import render
from Class.models import TheClass, ClassStudent, ClassHomework, HomeworkExperiment
from Course.models import Course, CourseTemplate, CourseTemplateExperiment
from Experiment.models import Experiment, experiment_course
from FrexTOnline.views import response_ok
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
    return HttpResponse(json.dumps(response_ok()), content_type='application/json')


def delete_class(request):
    print(request.POST["classId"])
    the_class = TheClass.objects.get(uid=request.POST["classId"])
    the_class.delete()
    return HttpResponse(json.dumps(response_ok()), content_type='application/json')


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
            data = {"state": "ERROR", "info": "学生{0}不存在！".format(n)}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            cs = ClassStudent(user=user, the_class=theClass)
            cs.save()
    return HttpResponse(json.dumps(response_ok()), content_type='application/json')


def get_template_class(request):
    print(request.POST)
    print(request.POST["templateId"])

    template = CourseTemplate.objects.get(uid=request.POST["templateId"])
    theClass = TheClass.objects.filter(course_template=template,
                                       end_time__gte=date.today()).distinct()

    classesName = []
    classesId = []
    for c in theClass:
        classesName.append(c.name)
        classesId.append(str(c.uid))

    data = {'state': "OK", 'classesId': classesId, 'classesName': classesName}
    return HttpResponse(json.dumps(data), content_type='application/json')


def dispatch_experiment(request):
    print(request.POST)
    print(request.POST["courseId"])
    print(request.POST["templateId"])
    print(request.POST["templateExpId"])
    print(request.POST["classId"])
    print(request.POST["startTime"])
    print(request.POST["endTime"])

    theClass = TheClass.objects.get(uid=request.POST["classId"])
    classExp = CourseTemplateExperiment.objects.get(uid=request.POST["templateExpId"])
    start = datetime.strptime(request.POST["startTime"], '%Y-%m-%d')
    end = datetime.strptime(request.POST["endTime"], '%Y-%m-%d')
    classExpHomework = ClassHomework(the_class=theClass, course_template_experiment=classExp,
                                     start_time=start, end_time=end)
    classExpHomework.save()

    class_students = ClassStudent.objects.filter(the_class=theClass)
    for n in class_students:
        # TODO 重复的情况
        experiment = Experiment(user=n.user, type=experiment_course, name=classExpHomework.name)
        experiment.save()
        homework_experiment = HomeworkExperiment(user=n.user, class_homework=classExpHomework, experiment=experiment)
        homework_experiment.save()
    return HttpResponse(json.dumps(response_ok()), content_type='application/json')