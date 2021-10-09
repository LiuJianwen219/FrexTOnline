import json
import os

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render

import config
from Class.models import ClassHomework, HomeworkExperiment
from Course.models import Course, CourseTemplate, CourseTemplateExperiment
from Experiment.models import Experiment, experiment_course
from File.models import File, file_src, CourseFile, file_bit
import File.utils as fh
from .ZipUtilities import ZipUtilities


# Create your views here.
from Login.models import User


def handle_uploaded_file(p, f):
    with open(p, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_free_file(request):
    if request.method == "POST":
        print(request.POST.get('freeExpId'))
        f_objs = request.FILES.getlist('uploadFile')  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=request.session["u_uid"])
        experiment = Experiment.objects.get(uid=request.POST.get('freeExpId'))

        if len(f_objs) == 0:
            req = {"state": "OK", 'info': "没有文件上传，请检查"}
            return HttpResponse(json.dumps(req), content_type='application/json')

        cnt = 0
        for f_obj in f_objs:
            if len(f_obj.name) > 100 or len(f_obj.name) <= 0:
                req = {"state": "ERROR", "info": "文件名超出限定长度 100"}
                return HttpResponse(json.dumps(req), content_type='application/json')

            handle_uploaded_file("/tmp/"+f_obj.name, f_obj)
            ff = File()
            ff.user = user
            ff.experiment = experiment
            ff.type = file_src
            ff.file_name = f_obj.name
            ff.file_path = "/tmp/"+f_obj.name
            # with open(ff.file_path, "rb") as tf:
            #     ff.content = tf.read()
            ff.save()

            with open(ff.file_path, 'rb') as f:
                if fh.post_experiment({
                    config.c_userId: str(user.uid),
                    config.c_experimentType: experiment.type,
                    config.c_experimentId: str(experiment.uid),
                    config.c_fileName: f_obj.name,
                }, f) == config.request_failed:
                    req = {"state": "ERROR", 'info': "保存自由实验上传的作业文件失败"}
                    return HttpResponse(json.dumps(req), content_type='application/json')
            cnt += 1
            req = {"state": "OK", "trueFileName": f_obj.name, "fileId": ff.uid.__str__()}
            return HttpResponse(json.dumps(req), content_type='application/json')

        if cnt == len(f_objs):  # TODO make this useful
            req = {"state": "OK", 'info': "文件上传成功"}
            return HttpResponse(json.dumps(req), content_type='application/json')
        else:
            req = {"state": "ERROR", 'info': "文件上传失败"}
            return HttpResponse(json.dumps(req), content_type='application/json')

    req = {"state": "ERROR", 'info': "非法请求"}
    return HttpResponse(json.dumps(req), content_type='application/json')


def delete_free_file(request):
    if request.method == "POST":
        user = User.objects.get(uid=request.session["u_uid"])
        experiment = Experiment.objects.get(uid=request.POST.get('freeExpId'))
        f_uid = request.POST["freeFileId"]
        file = File.objects.get(uid=f_uid)
        try:
            file.delete()
            if fh.delete_experiment({
                config.c_userId: str(user.uid),
                config.c_experimentType: experiment.type,
                config.c_experimentId: str(experiment.uid),
                config.c_fileName: file.file_name,
            }) == config.request_failed:
                req = {"state": "ERROR", 'info': "删除文件失败"}
                return HttpResponse(json.dumps(req), content_type='application/json')
        except Exception as e:
            data = {"state": "ERROR", "info": e}
        else:
            data = {"state": "OK"}
        return HttpResponse(json.dumps(data), content_type='application/json')

    data = {"state": "ERROR", 'info': "未知的错误，请尝试刷新"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def download_file(request, f_uid):
    file = File.objects.get(uid=f_uid)
    try:
        values = {
            config.c_userId: str(file.user.uid),
            config.c_experimentType: file.experiment.type,
            config.c_experimentId: str(file.experiment.uid),
            config.c_fileName: file.file_name,
        }
        if file.type == "src":
            file_content = fh.get_experiment(values)
        elif file.type == "log":
            values[config.c_compileId] = file.file_name.split('.')[0]
            file_content = fh.get_log(values)
        elif file.type == "bit":
            values[config.c_compileId] = file.file_name.split('.')[0]
            file_content = fh.get_bit(values)
        else:
            file_content = None
        if file_content:
            response = HttpResponse(file_content)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename={0}'.format(file.file_name)
            return response
        data = {"state": "ERROR", 'info': "unknown error"}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception:
        data = {"state": "ERROR", 'info': "internal error"}
        return HttpResponse(json.dumps(data), content_type='application/json')


def upload_bit(request):
    if request.method == "POST":
        f_obj = request.FILES.get('upBitFile')  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=request.session["u_uid"])
        try:
            experiment = Experiment.objects.get(uid=request.POST.get('expId'))
        except Experiment.DoesNotExist:
            experiment = HomeworkExperiment.objects.get(class_homework_id=request.POST.get('expId')).experiment

        if len(f_obj.name) > 100 or len(f_obj.name) <= 0:
            req = {"state": "ERROR", "info": "文件名超出限定长度 100"}
            return HttpResponse(json.dumps(req), content_type='application/json')

        handle_uploaded_file("/tmp/"+f_obj.name, f_obj)
        ff = File()
        ff.user = user
        ff.experiment = experiment
        ff.type = file_bit
        ff.file_name = f_obj.name
        ff.file_path = "/tmp/"+f_obj.name
        # with open(ff.file_path, "r") as tf:
        #     ff.content = tf.read()
        ff.save()

        with open(ff.file_path, 'rb') as f:
            if fh.post_bit({
                config.c_userId: str(user.uid),
                config.c_experimentType: experiment.type,
                config.c_experimentId: str(experiment.uid),
                config.c_compileId: f_obj.name.split('.')[0],
            }, f) == config.request_failed:
                req = {"state": "ERROR", 'info': "保存自由实验上传的作业文件失败"}
                return HttpResponse(json.dumps(req), content_type='application/json')

        req = {"state": "OK", "trueFileName": f_obj.name, "fileId": ff.uid.__str__()}
        return HttpResponse(json.dumps(req), content_type='application/json')

    req = {"state": "ERROR", 'info': "非法请求"}
    return HttpResponse(json.dumps(req), content_type='application/json')


def upload_course(request):
    if request.method == "POST":
        print(request.POST["courseId"])
        print(request.POST["templateId"])
        print(request.POST['templateExpId'])

        f_obj = request.FILES.getlist('courseFiles')[0]  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=request.session["u_uid"])
        course = Course.objects.get(uid=request.POST["courseId"])
        courseTemplate = CourseTemplate.objects.get(uid=request.POST["templateId"])
        courseTemplateExperiment = CourseTemplateExperiment.objects.get(uid=request.POST['templateExpId'])

        if len(f_obj.name) > 100 or len(f_obj.name) <= 0:
            req = {"state": "ERROR", "info": "文件名超出限定长度 100"}
            return HttpResponse(json.dumps(req), content_type='application/json')

        handle_uploaded_file("/tmp/"+f_obj.name, f_obj)
        ff = CourseFile()
        ff.course_template_experiment = courseTemplateExperiment
        ff.file_name = f_obj.name
        ff.file_path = "/tmp/"+f_obj.name
        # with open(ff.file_path, "r") as tf:
        #     ff.content = tf.read()
        ff.save()

        with open(ff.file_path, 'rb') as f:
            if fh.post_course({
                config.c_userId: str(user.uid),
                config.c_courseId: str(course.uid),
                config.c_courseTemplateId: str(courseTemplate.uid),
                config.c_courseTemplateExperimentId: str(courseTemplateExperiment.uid),
                config.c_fileName: f_obj.name,
            }, f) == config.request_failed:
                req = {"state": "ERROR", 'info': "保存课件失败"}
                return HttpResponse(json.dumps(req), content_type='application/json')

        req = {"state": "OK", "fileName": f_obj.name, "fileId": ff.uid.__str__()}
        return HttpResponse(json.dumps(req), content_type='application/json')

    req = {"state": "ERROR", 'info': "非法请求"}
    return HttpResponse(json.dumps(req), content_type='application/json')


def delete_course(request):
    if request.method == "POST":
        print(request.POST["courseId"])
        print(request.POST["templateId"])
        print(request.POST['templateExpId'])
        print(request.POST["fileId"])

        user = User.objects.get(uid=request.session["u_uid"])
        course = Course.objects.get(uid=request.POST["courseId"])
        courseTemplate = CourseTemplate.objects.get(uid=request.POST["templateId"])
        courseTemplateExperiment = CourseTemplateExperiment.objects.get(uid=request.POST['templateExpId'])
        courseFile = CourseFile.objects.get(uid=request.POST["fileId"])

        try:
            courseFile.delete()
            if fh.delete_course({
                config.c_userId: str(user.uid),
                config.c_courseId: str(course.uid),
                config.c_courseTemplateId: str(courseTemplate.uid),
                config.c_courseTemplateExperimentId: str(courseTemplateExperiment.uid),
                config.c_fileName: courseFile.file_name,
            }) == config.request_failed:
                req = {"state": "ERROR", 'info': "删除文件失败"}
                return HttpResponse(json.dumps(req), content_type='application/json')
        except Exception as e:
            data = {"state": "ERROR", "info": e}
        else:
            data = {"state": "OK"}
        return HttpResponse(json.dumps(data), content_type='application/json')

    data = {"state": "ERROR", 'info': "未知的错误，请尝试刷新"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def download_course(request, homeworkId):
    print(homeworkId)
    user = User.objects.get(uid=request.session["u_uid"])
    homework = HomeworkExperiment.objects.get(experiment__uid=homeworkId).class_homework
    courseTemplateExperiment = homework.course_template_experiment
    courseTemplate = homework.course_template_experiment.course_template
    course = homework.course_template_experiment.course_template.course
    fileClassExp = CourseFile.objects.filter(course_template_experiment=homework.course_template_experiment)

    if fileClassExp:
        utilities = ZipUtilities()
        for f in fileClassExp:
            if fh.get_course({
                config.c_userId: str(user.uid),
                config.c_courseId: str(course.uid),
                config.c_courseTemplateId: str(courseTemplate.uid),
                config.c_courseTemplateExperimentId: str(courseTemplateExperiment.uid),
                config.c_fileName: f.file_name,
            }) == config.request_failed:
                break
            utilities.toZip(os.path.join(config.work_dir, f.file_name), "")

        response = StreamingHttpResponse(utilities.zip_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("下载.zip")
        return response

    req = {"state": "ERROR", 'info': "no file of this experiment"}
    return HttpResponse(json.dumps(req), content_type='application/json')


def upload_homework(request):
    if request.method == "POST":
        print(request.POST.get('homeworkId'))
        print(request.POST.get('homeworkFileType'))
        fileType = request.POST.get('homeworkFileType')
        f_objs = request.FILES.getlist('uploadFile')  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=request.session["u_uid"])
        experiment = Experiment.objects.get(uid=request.POST.get('homeworkId'))
        # homework = ClassHomework.objects.get(uid=request.POST.get('homeworkId'))
        # homework_experiments = HomeworkExperiment.objects.filter(user=user, class_homework=homework)
        # if len(homework_experiments) == 0:
        #     experiment = Experiment(user=user, name=homework.name, type=experiment_course)
        #     experiment.save()
        #     homework_experiment = HomeworkExperiment(user=user, class_homework=homework, experiment=experiment)
        #     homework_experiment.save()
        # else:
        #     homework_experiment = homework_experiments[0]
        #     experiment = homework_experiment.experiment

        if len(f_objs) == 0:
            req = {"state": "OK", 'info': "没有文件上传，请检查"}
            return HttpResponse(json.dumps(req), content_type='application/json')

        cnt = 0
        for f_obj in f_objs:
            if len(f_obj.name) > 100 or len(f_obj.name) <= 0:
                req = {"state": "ERROR", "info": "文件名超出限定长度 100"}
                return HttpResponse(json.dumps(req), content_type='application/json')

            handle_uploaded_file("/tmp/" + f_obj.name, f_obj)
            ff = File()
            ff.user = user
            ff.experiment = experiment
            if fileType:
                ff.type = fileType
            else:
                ff.type = file_src
            ff.file_name = f_obj.name
            ff.file_path = "/tmp/" + f_obj.name
            # with open(ff.file_path, "r", encoding='gbk') as tf:
            #     ff.content = tf.read()
            ff.save()

            with open(ff.file_path, 'rb') as f:
                if fh.post_experiment({
                    config.c_userId: str(user.uid),
                    config.c_experimentType: experiment.type,
                    config.c_experimentId: str(experiment.uid),
                    config.c_fileName: f_obj.name,
                }, f) == config.request_failed:
                    req = {"state": "ERROR", 'info': "保存实验文件"}
                    return HttpResponse(json.dumps(req), content_type='application/json')
            cnt += 1
            req = {"state": "OK", "trueFileName": f_obj.name, "fileId": ff.uid.__str__()}
            return HttpResponse(json.dumps(req), content_type='application/json')

        if cnt == len(f_objs):  # TODO make this useful
            req = {"state": "OK", 'info': "文件上传成功"}
            return HttpResponse(json.dumps(req), content_type='application/json')
        else:
            req = {"state": "ERROR", 'info': "文件上传失败"}
            return HttpResponse(json.dumps(req), content_type='application/json')

    req = {"state": "ERROR", 'info': "非法请求"}
    return HttpResponse(json.dumps(req), content_type='application/json')


def delete_homework(request):
    if request.method == "POST":
        user = User.objects.get(uid=request.session["u_uid"])
        experiment = Experiment.objects.get(uid=request.POST.get('homeworkId'))
        file = File.objects.get(uid=request.POST["classFileId"])
        try:
            file.delete()
            if fh.delete_experiment({
                config.c_userId: str(user.uid),
                config.c_experimentType: experiment.type,
                config.c_experimentId: str(experiment.uid),
                config.c_fileName: file.file_name,
            }) == config.request_failed:
                req = {"state": "ERROR", 'info': "删除文件失败"}
                return HttpResponse(json.dumps(req), content_type='application/json')
        except Exception as e:
            data = {"state": "ERROR", "info": e}
        else:
            data = {"state": "OK"}
        return HttpResponse(json.dumps(data), content_type='application/json')
    data = {"state": "ERROR", 'info': "未知的错误，请尝试刷新"}
    return HttpResponse(json.dumps(data), content_type='application/json')
