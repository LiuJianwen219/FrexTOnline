from django.shortcuts import render
from Login.models import User
from Experiment.models import Experiment, experiment_free, experiment_course
from File.models import File, HomeworkFile
from datetime import date, datetime
from Class.models import ClassStudent, ClassHomework

# Create your views here.

def home(request):
    return render(request, 'Home/home.html')


def introduce(request):
    return render(request, 'Home/introduction.html')


def experiment(request):
    user = User.objects.get(uid=request.session["u_uid"])
    context = {"freeExperiment": getFreeExpDrawer(user)}
    # 用户 -> 课程实验作业 -> 文件
    theClasses = ClassStudent.objects.filter(user=user)
    # theClasses = user.classes.all().only('id', 'course').select_related('course')
    course_temp_exp = ClassHomework.objects.filter(the_class__in=theClasses.values_list('the_class'),
                                            start_time__lte=date.today(),
                                            end_time__gte=date.today())

    print(course_temp_exp)

    classExpHomeworkFiles = HomeworkFile.objects.filter(
        course_template_experiment__in=course_temp_exp.values_list('course_template_experiment'))

    classExpHomeworkFileDict = {homework.uid: [] for homework in course_temp_exp}
    for file in classExpHomeworkFiles:
        classExpHomeworkFileDict[file.homework_id].append({"fileId": file.uid, "fileName": file.file_name})

    classExpFileDict = {
        homework.id: [
            {"fileId": file.uid, "fileName": file.file_name}
            for file in homework.exp.fileclassexp_set.all()
        ] for homework in course_temp_exp
    }

    homeworkItems = [
        {
            "theClass": homework.the_class_uid,
            "expId": homework.uid,
            "expName": homework.exp.name,
            "fileList": classExpHomeworkFileDict[homework.uid],
            "expCourseware": classExpFileDict[homework.uid]
        }
        for homework in course_temp_exp
    ]

    classExpHomeworkDict = {theClass.uid: [] for theClass in theClasses}
    for homeworkItem in homeworkItems:
        classExpHomeworkDict[homeworkItem['theClass']].append(homeworkItem)
    theClassItems = [
        {
            "id": theClass.uid,
            "expType": theClass.course.name,
            "expItems": classExpHomeworkDict[theClass.uid]
        }
        for theClass in theClasses
    ]
    context["classExperiment"] = theClassItems
    return render(request, "Home/studentHome.html", context=context)


def getFreeExpDrawer(user: User):
    # 按用户名获得自由实验信息
    freeExps = Experiment.objects.filter(user=user, type=experiment_free)
    # 一次取回了所有实验文件
    freeExpFiles = File.objects.filter(experiment__in=freeExps)#.only('id', 'file_name', 'free_exp')
    # 建立一个字典，键依次为所有的自由实验id，值为一个列表，列表中是储存各个文件信息的字典。扫描刚刚的文件列表以分类存放
    # 之后对作业文件、作业也是类似的操作
    freeExpFilesDict = {freeExp.uid: [] for freeExp in freeExps}
    for file in freeExpFiles:
        freeExpFilesDict[file.experiment.uid].append({"fileId": file.uid, "fileName": file.file_name})
    expItems = [
        {
            "expId": freeExp.uid,
            "expName": freeExp.name,
            "fileList": freeExpFilesDict[freeExp.uid]
        }
        for freeExp in freeExps
    ]
    print(expItems)
    return {"id": "0", "expType": "自由实验", "expItems": expItems}
