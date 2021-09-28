from django.shortcuts import render
from Login.models import User
from Experiment.models import Experiment, experiment_free, experiment_course
from File.models import File, HomeworkFile, CourseFile
from datetime import date, datetime
from Class.models import ClassStudent, ClassHomework
from Course.models import Course, CourseTemplate, CourseTemplateExperiment
from Class.models import TheClass
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


def course(request):
    user = User.objects.get(uid=request.session["u_uid"])

    context = {"experiments": getFreeExpDrawer(user)}

    courses = Course.objects.filter(user=user)
    course_templates = CourseTemplate.objects.filter(course__in=courses)
    course_template_exp = CourseTemplateExperiment.objects.filter(course_template__in=course_templates)#.distinct()
    c_t_e_files = CourseFile.objects.filter(course_template_experiment__in=course_template_exp)

    the_classes = TheClass.objects.filter(course__in=courses)
    students = ClassStudent.objects.filter(the_class__in=the_classes)

    # exps = ClassExp.objects.filter(templatecontent__in=templateContents).distinct()
    # expFiles = FileClassExp.objects.filter(class_exp__in=exps)
    # theClasses = TheClass.objects.filter(course__in=courses)
    # students = User2.objects.filter(classes__in=theClasses).distinct()

    # 实验部分
    expFileDict = {exp.uid: [] for exp in course_template_exp}
    for file in c_t_e_files:
        expFileDict[file.class_exp_id].append({"fileId": file.uid, "fileName": file.file_name})
    expItems = [
        {
            # 'templateId': list(exp.templatecontent_set.values_list('id', flat=True)),
            'templateId': exp.course_template.uid,
            'templateExpId': exp.uid,
            'expName': exp.name,
            'expFile': expFileDict[exp.uid]
        }
        for exp in course_template_exp
    ]

    expDict = {}
    for expItem in expItems:
        for id in expItem['templateId']:
            expDict[id] = expItem

    templateItems = [
        {
            # 'courseId': list(template.courses.values_list('id', flat=True)),
            'courseId': template.course.uid,
            'templateId': template.id,
            'templateName': template.name,
            'templateExp': [expDict[i] for i in template.templatecontent_set.values_list('id', flat=True)]
        }
        for template in course_templates
    ]

    templateDict = {course.id: [] for course in courses}
    for templateItem in templateItems:
        for id in templateItem['courseId']:
            if id in templateDict.keys():
                templateDict[id].append(templateItem)

    # 班级部分
    studentDict = {theClass.id: [] for theClass in the_classes}
    for student in students:
        for theClass in student.classes.all():
            studentDict[theClass.id].append(student.name)
    theClassItems = [
        {
            'courseId': theClass.course.uid,
            'classId': theClass.uid,
            'classNumber': "99999",
            'className': theClass.name,
            'templateId': theClass.course_template.uid,
            'templateName': theClass.course_template.name,
            'classStudent': studentDict[theClass.uid],
            'classStartTime': theClass.start_time,
            'classEndTime': theClass.end_time,
        }
        for theClass in the_classes
    ]


    theClassDict = {course.id: [] for course in courses}
    for theClassItem in theClassItems:
        theClassDict[theClassItem['courseId']].append(theClassItem)

    context["classContent"] = [
        {
            'classTypeId': course.id,
            'classType': course.name,
            'classTemplate': templateDict[course.id],
            'classList': theClassDict[course.id]
        }
        for course in courses
    ]
    context["role"] = user.role
    print(user.role)
    return render(request, "Home/teacherHome.html", context=context)
