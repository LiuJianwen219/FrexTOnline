import json

from django.http import HttpResponse, FileResponse
from django.shortcuts import render

import config
from Course.models import Course
from Experiment.models import Experiment
from File.models import File, file_src, CourseFile
import File.utils as fh


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
            with open(ff.file_path, "r", encoding='gbk') as tf:
                ff.content = tf.read()
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


def download_free_file(request, f_uid):
    file = File.objects.get(uid=f_uid)
    try:
        response = FileResponse(file.content)
        response['Content-Type'] = 'application/zip'
        response['Content-Disposition'] = 'attachment;filename={0}'.format(file.file_name)
        return response
    except Exception:
        data = {"state": "ERROR", 'info': "未知的错误1，请尝试刷新"}
        return HttpResponse(json.dumps(data), content_type='application/json')


def upload_bit(request):
    if request.method == "POST":
        f_obj = request.FILES.get('upBitFile')  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=request.session["u_uid"])
        experiment = Experiment.objects.get(uid=request.POST.get('expId'))

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

        f_obj = request.FILES.get('upBitFile')  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=request.session["u_uid"])
        course = Course.objects.get(uid=request.POST["courseId"])
        courseTemplate = Course.objects.get(uid=request.POST["templateId"])
        courseTemplateExperiment = Experiment.objects.get(uid=request.POST['templateExpId'])

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

        req = {"state": "OK", "trueFileName": f_obj.name, "fileId": ff.uid.__str__()}
        return HttpResponse(json.dumps(req), content_type='application/json')

    req = {"state": "ERROR", 'info': "非法请求"}
    return HttpResponse(json.dumps(req), content_type='application/json')
