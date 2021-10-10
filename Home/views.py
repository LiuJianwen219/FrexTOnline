import json
import time

from django.shortcuts import render
from Login.models import User
from Experiment.models import Experiment, experiment_free, experiment_course
from File.models import File, CourseFile
from datetime import date, datetime
from Class.models import ClassStudent, ClassHomework, HomeworkExperiment
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
    class_student = ClassStudent.objects.filter(user=user)
    # theClasses = user.classes.all().only('id', 'course').select_related('course')
    class_homework = ClassHomework.objects.filter(the_class__in=class_student.values_list('the_class'),
                                                   start_time__lte=date.today(),
                                                   end_time__gte=date.today()).order_by('start_time')
    course_file = CourseFile.objects.filter(course_template_experiment__in=class_homework.
                                            values_list('course_template_experiment')).order_by('upload_time')
    homework_experiment = HomeworkExperiment.objects.filter(user=user, class_homework__in=class_homework)
    userExpHomeworkFiles =File.objects.filter(experiment__in=homework_experiment.
                                              values_list('experiment')).order_by('create_time')

    # print("class_student")
    # for c in class_student:
    #     print(c.uid)
    #
    # print("class_homework")
    # for c in class_homework:
    #     print(c.uid)
    #
    # print("course_file")
    # for c in course_file:
    #     print(c.uid)
    #
    # print("userExpHomeworkFiles")
    # for c in userExpHomeworkFiles:
    #     print(c.uid)

    classHomeworkItem = []
    for c_t_experiment in class_homework:
        print(c_t_experiment.uid)
        cou_file = []
        for c_file in course_file:
            print(str(c_file.course_template_experiment.uid), str(c_t_experiment.course_template_experiment.uid))
            if str(c_file.course_template_experiment.uid) == str(c_t_experiment.course_template_experiment.uid):
                cou_file.append({
                    "fileId": str(c_file.uid),
                    "fileName": c_file.file_name,
                })
        for t in homework_experiment:
            print( str(t.class_homework.uid), str(c_t_experiment.uid))
            if str(t.class_homework.uid) == str(c_t_experiment.uid):
                classHomeworkItem.append({
                    "theClass": str(c_t_experiment.the_class.uid),
                    "expId": str(t.experiment.uid),
                    "expName": c_t_experiment.course_template_experiment.name,
                    "fileList": [],
                    "expCourseware": cou_file,
                })
        print(json.dumps(classHomeworkItem))
        print(c_t_experiment.uid)

    for f in userExpHomeworkFiles:
        for c in classHomeworkItem:
            print(str(f.experiment.uid), c['expId'])
            if str(f.experiment.uid) == c['expId']:
                c['fileList'].append({
                    "fileId": str(f.uid),
                    "fileName": f.file_name,
                    "fileType": f.type,
                    "fileNameOther": f.file_name_other,
                })

    print(json.dumps(classHomeworkItem))

    classItem = []
    for the_class in class_student:
        classItem.append({
            "id": str(the_class.the_class.uid),
            "expType": the_class.the_class.course.name,
            "expItems": []
        })

    for c_h_i in classHomeworkItem:
        for c_i in classItem:
            if c_h_i['theClass'] == c_i['id']:
                c_i['expItems'].append(c_h_i)

    print(json.dumps(classItem))

    # classExpHomeworkFileDict = {homework.uid: [] for homework in course_temp_exp}
    # for file in userExpHomeworkFiles:
    #     classExpHomeworkFileDict[str(file.class_homework.uid)].append({"fileId": file.uid, "fileName": file.file_name})
    #
    # classExpFileDict = {
    #     homework.id: [
    #         {"fileId": file.uid, "fileName": file.file_name}
    #         for file in homework.course_template_experiment.fileclassexp_set.all()
    #     ] for homework in course_temp_exp
    # }
    #
    # homeworkItems = [
    #     {
    #         "theClass": homework.the_class_uid,
    #         "expId": homework.uid,
    #         "expName": homework.exp.name,
    #         "fileList": classExpHomeworkFileDict[homework.uid],
    #         "expCourseware": classExpFileDict[homework.uid]
    #     }
    #     for homework in course_temp_exp
    # ]
    #


    # classExpHomeworkDict = {theClass.uid: [] for theClass in theClasses}
    # for homeworkItem in homeworkItems:
    #     classExpHomeworkDict[homeworkItem['theClass']].append(homeworkItem)
    # theClassItems = [
    #     {
    #         "id": theClass.uid,
    #         "expType": theClass.the_class.course.name,
    #         "expItems": classExpHomeworkDict[theClass.uid]
    #     }
    #     for theClass in theClasses
    # ]
    context["classExperiment"] = classItem
    return render(request, "Home/studentHome.html", context=context)


def getFreeExpDrawer(user: User):
    # 按用户名获得自由实验信息
    freeExps = Experiment.objects.filter(user=user, type=experiment_free).order_by('create_time')
    # 一次取回了所有实验文件
    freeExpFiles = File.objects.filter(experiment__in=freeExps).order_by('create_time')  # .only('id', 'file_name', 'free_exp')
    # 建立一个字典，键依次为所有的自由实验id，值为一个列表，列表中是储存各个文件信息的字典。扫描刚刚的文件列表以分类存放
    # 之后对作业文件、作业也是类似的操作
    freeExpFilesDict = {freeExp.uid: [] for freeExp in freeExps}
    for file in freeExpFiles:
        freeExpFilesDict[file.experiment.uid].append({
            "fileId": file.uid,
            "fileName": file.file_name,
            "fileType": file.type,
            "fileNameOther": file.file_name_other,
        })
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
    course_templates = CourseTemplate.objects.filter(course__in=courses).order_by('create_time')
    course_template_exp = CourseTemplateExperiment.objects.\
        filter(course_template__in=course_templates).order_by('create_time')  # .distinct()
    c_t_e_files = CourseFile.objects.filter(course_template_experiment__in=course_template_exp).order_by('upload_time')

    the_classes = TheClass.objects.filter(course__in=courses).order_by('name')
    students = ClassStudent.objects.filter(the_class__in=the_classes).order_by('enter_time')
    class_homework = ClassHomework.objects.filter(the_class__in=the_classes).order_by("end_time", "start_time")

    # 实验部分
    expItem = []
    for exp in course_template_exp:
        expItem.append({
            'templateId': str(exp.course_template.uid),
            'templateExpId': str(exp.uid),
            'expName': exp.name,
            'expFile': [],
        })

    for file in c_t_e_files:
        for exp in expItem:
            if str(file.course_template_experiment.uid) == exp['templateExpId']:
                exp['expFile'].append({
                    "fileId": str(file.uid),
                    "fileName": file.file_name,
                })
                break

    templateItem = []
    for template in course_templates:
        templateItem.append({
            'courseId': str(template.course.uid),
            'templateId': str(template.uid),
            'templateName': template.name,
            'templateExp': [],
        })

    for exp in expItem:
        for tem in templateItem:
            if exp['templateId'] == tem['templateId']:
                tem['templateExp'].append(exp)
                break

    # 班级部分
    courseItem = []
    for c in courses:
        courseItem.append({
            'classTypeId': str(c.uid),
            'classType': c.name,
            'classTemplate': [],
            'classList': [],
        })

    classItem = []
    for the in the_classes:
        classItem.append({
            'courseId': str(the.course.uid),
            'classId': str(the.uid),
            'classNumber': the.name,
            'className': the.name,
            'templateId': str(the.course_template.uid),
            'templateName': the.course_template.name,
            'classStudent': [],
            'classStartTime': the.start_time,
            'classEndTime': the.end_time,
            'classHomework': [],
        })

    for stu in students:
        for cla in classItem:
            if str(stu.the_class.uid) == cla['classId']:
                cla["classStudent"].append(stu.user.name)
                break

    for homework in class_homework:
        for cla in classItem:
            if str(homework.the_class.uid) == cla['classId']:
                cla["classHomework"].append({
                    "homeworkName": homework.course_template_experiment.name,
                    "homeworkId": str(homework.course_template_experiment.uid),
                    "homeworkStartTime": homework.start_time,
                    "homeworkEndTime": homework.end_time,
                    "homeworkState": "ing" if homework.start_time < date.today() < homework.end_time else "over"
                })

    for cla in classItem:
        for cou in courseItem:
            if cla['courseId'] == cou['classTypeId']:
                cou['classList'].append(cla)
                break

    for tem in templateItem:
        for cou in courseItem:
            if tem['courseId'] == cou['classTypeId']:
                cou['classTemplate'].append(tem)

    context["classContent"] = courseItem
    context["role"] = user.role
    return render(request, "Home/teacherHome.html", context=context)
