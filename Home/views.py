import json

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
                                                   end_time__gte=date.today())
    course_file = CourseFile.objects.filter(course_template_experiment__in=class_homework.values_list('course_template_experiment'))
    homework_experiment = HomeworkExperiment.objects.filter(class_homework__in=class_homework)
    userExpHomeworkFiles =File.objects.filter(experiment__in=homework_experiment.values_list('experiment'))

    print("class_student")
    for c in class_student:
        print(c.uid)

    print("class_homework")
    for c in class_homework:
        print(c.uid)

    print("course_file")
    for c in course_file:
        print(c.uid)

    classHomeworkItem = []
    for c_t_experiment in class_homework:
        cou_file = []
        for c_file in course_file:
            if str(c_file.course_template_experiment.uid) == str(c_t_experiment.course_template_experiment.uid):
                cou_file.append({
                    "fileId": str(c_file.uid),
                    "fileName": c_file.file_name,
                })
        classHomeworkItem.append({
            "theClass": str(c_t_experiment.the_class.uid),
            "expId": str(c_t_experiment.uid),
            "expName": c_t_experiment.course_template_experiment.name,
            "fileList": [],
            "expCourseware": cou_file,
        })

    print(json.dumps(classHomeworkItem))

    for f in userExpHomeworkFiles:
        for c in classHomeworkItem:
            if str(f.experiment.uid) == c['expId']:
                c['fileList'].append({
                    "fileId": f.uid,
                    "fileName": f.file_name,
                })
                break

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
                break

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
    freeExps = Experiment.objects.filter(user=user, type=experiment_free)
    # 一次取回了所有实验文件
    freeExpFiles = File.objects.filter(experiment__in=freeExps)  # .only('id', 'file_name', 'free_exp')
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
    course_template_exp = CourseTemplateExperiment.objects.filter(course_template__in=course_templates)  # .distinct()
    c_t_e_files = CourseFile.objects.filter(course_template_experiment__in=course_template_exp)

    the_classes = TheClass.objects.filter(course__in=courses)
    students = ClassStudent.objects.filter(the_class__in=the_classes)

    # exps = ClassExp.objects.filter(templatecontent__in=templateContents).distinct()
    # expFiles = FileClassExp.objects.filter(class_exp__in=exps)
    # theClasses = TheClass.objects.filter(course__in=courses)
    # students = User2.objects.filter(classes__in=theClasses).distinct()

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
                    "fileName": file.file_name
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

    # templateItems = {}
    # for template in course_templates:
    #     if str(template.course.uid) in templateItems.keys():
    #         templateItems[str(template.course.uid)]['templateExp'].append(template)
    #     else:
    #         templateItems[str(template.course.uid)] = {
    #             'courseId': template.course.uid,
    #             'templateId': template.uid,
    #             'templateName': template.name,
    #             'templateExp': [template],
    #         }

    # expFileDict = {exp.uid: [] for exp in course_template_exp}
    # for file in c_t_e_files:
    #     expFileDict[str(file.experiment.uid)].append({"fileId": str(file.uid), "fileName": file.file_name})
    # expItems = [
    #     {
    #         # 'templateId': list(exp.templatecontent_set.values_list('id', flat=True)),
    #         'templateId': exp.course_template.uid,
    #         'templateExpId': exp.uid,
    #         'expName': exp.name,
    #         'expFile': expFileDict[str(exp.uid)]
    #     }
    #     for exp in course_template_exp
    # ]

    # expDict = {}
    # for expItem in expItems:
    #     for id in expItem['templateId']:
    #         expDict[id] = expItem

    # templateItems = [
    #     {
    #         # 'courseId': list(template.courses.values_list('id', flat=True)),
    #         'courseId': template.course.uid,
    #         'templateId': template.uid,
    #         'templateName': template.name,
    #         # 'templateExp': [expDict[i] for i in template.course_set.values_list('uid', falt=True)],
    #     }
    #     for template in course_templates
    # ]
    #
    #
    # templateDict = {course.uid: [] for course in courses}
    # for templateItem in templateItems:
    #     for id in templateItem['courseId']:
    #         if id in templateDict.keys():
    #             templateDict[id].append(templateItem)

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
        })

    for stu in students:
        for cla in classItem:
            if str(stu.the_class.uid) == cla['classId']:
                cla["classStudent"].append(stu.user.name)
                break

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

    # studentDict = {theClass.uid: [] for theClass in the_classes}
    # for student in students:
    #     for theClass in student.classes.all():
    #         studentDict[theClass.uid].append(student.name)

    # theClassItems = [
    #     {
    #         'courseId': theClass.course.uid,
    #         'classId': theClass.uid,
    #         'classNumber': "99999",
    #         'className': theClass.name,
    #         'templateId': theClass.course_template.uid,
    #         'templateName': theClass.course_template.name,
    #         'classStudent': studentDict[theClass.uid],
    #         'classStartTime': theClass.start_time,
    #         'classEndTime': theClass.end_time,
    #     }
    #     for theClass in the_classes
    # ]

    # theClassDict = {course.uid: [] for course in courses}
    # for theClassItem in theClassItems:
    #     theClassDict[theClassItem['courseId']].append(theClassItem)

    # context["classContent"] = [
    #     {
    #         'classTypeId': str(course.uid),
    #         'classType': course.name,
    #         'classTemplate': templateDict[str(course.uid)],
    #         'classList': theClassDict[str(course.uid)]
    #     }
    #     for course in courses
    # ]
    context["role"] = user.role
    print(user.role)
    return render(request, "Home/teacherHome.html", context=context)
