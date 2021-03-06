import io
import json
import os
import uuid

from chardet import UniversalDetector
from chardet.enums import LanguageFilter
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect

import config
from Class.models import ClassHomework, HomeworkExperiment
from Course.models import Course, CourseTemplate, CourseTemplateExperiment
from Experiment.models import Experiment, experiment_course
from File.models import File, file_src, CourseFile, file_bit, file_report, file_log
import File.utils as fh
from FrexTOnline.views import response_ok, response_error
from Home.views import access_record
from .ZipUtilities import ZipUtilities

# Create your views here.
from Login.models import User


def handle_uploaded_file(p, f):
    with open(p, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def handle_uploaded_file_str(p, f):
    with open(p, 'w+') as destination:
        destination.write(f)


def reading_unknown_encoding_file(filename):
    detector = UniversalDetector(LanguageFilter.CHINESE)
    with open(filename, 'rb') as f:
        detector.feed(f.read())
        detector.close()
        encoding = detector.result['encoding']
        f = io.TextIOWrapper(f, encoding=encoding)
        f.seek(0)
        return f.read()


# 是否包含中文
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def upload_free_file(request):
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        print(request.POST.get('freeExpId'))
        f_objs = request.FILES.getlist('uploadFile')  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=u_uid)
        experiment = Experiment.objects.get(uid=request.POST.get('freeExpId'))

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
            ff.type = file_src
            ff.file_name = f_obj.name
            ff.file_path = "/tmp/" + f_obj.name
            # with open(ff.file_path, "rb") as tf:
            #     ff.content = tf.read()
            ff.save()

            access_record(request, "upload", "上传自由实验文件：%s %s" % (f_obj.name, str(ff.uid)))

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
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        user = User.objects.get(uid=u_uid)
        experiment = Experiment.objects.get(uid=request.POST.get('freeExpId'))
        f_uid = request.POST["freeFileId"]
        file = File.objects.get(uid=f_uid)
        try:
            access_record(request, "delete", "删除自由实验文件：%s %s" % (file.file_name, str(file.uid)))
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
    if 'is_login' not in request.session:
        return redirect('/')

    file = File.objects.get(uid=f_uid)
    try:
        values = {
            config.c_userId: str(file.user.uid),
            config.c_experimentType: file.experiment.type,
            config.c_experimentId: str(file.experiment.uid),
            config.c_fileName: file.file_name,
        }
        access_record(request, "download", "下载文件：%s %s" % (file.file_name, str(file.uid)))
        if file.type == file_src or file.type == file_report:
            file_content = fh.get_experiment(values, str(uuid.uuid1()))
        elif file.type == file_log:
            values[config.c_compileId] = file.file_name.split('.')[0]
            file_content = fh.get_log(values)
        elif file.type == file_bit:
            values[config.c_compileId] = file.file_name.split('.')[0]
            file_content = fh.get_bit(values)
        else:
            file_content = None
        if file_content:
            file_name = file.file_name
            if is_contains_chinese(file.file_name):
                file_name = str(uuid.uuid1()) + '.' + file.file_name.split('.')[-1]
            response = HttpResponse(file_content)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename={0}'.format(file_name)
            return response
        data = {"state": "ERROR", 'info': "unknown error"}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception:
        data = {"state": "ERROR", 'info': "internal error"}
        return HttpResponse(json.dumps(data), content_type='application/json')


def upload_bit(request):
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        f_obj = request.FILES.get('upBitFile')  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=u_uid)
        try:
            experiment = Experiment.objects.get(uid=request.POST.get('expId'))
        except Experiment.DoesNotExist:
            experiment = HomeworkExperiment.objects.get(class_homework_id=request.POST.get('expId')).experiment

        if len(f_obj.name) > 100 or len(f_obj.name) <= 0:
            req = {"state": "ERROR", "info": "文件名超出限定长度 100"}
            return HttpResponse(json.dumps(req), content_type='application/json')

        handle_uploaded_file("/tmp/" + f_obj.name, f_obj)
        ff = File()
        ff.user = user
        ff.experiment = experiment
        ff.type = file_bit
        ff.file_name = f_obj.name
        ff.file_path = "/tmp/" + f_obj.name
        # with open(ff.file_path, "r") as tf:
        #     ff.content = tf.read()
        ff.save()

        access_record(request, "upload", "上传bit文件：%s %s" % (ff.file_name, str(ff.uid)))

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
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        print(request.POST["courseId"])
        print(request.POST["templateId"])
        print(request.POST['templateExpId'])

        f_obj = request.FILES.getlist('courseFiles')[0]  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=u_uid)
        course = Course.objects.get(uid=request.POST["courseId"])
        courseTemplate = CourseTemplate.objects.get(uid=request.POST["templateId"])
        courseTemplateExperiment = CourseTemplateExperiment.objects.get(uid=request.POST['templateExpId'])

        if len(f_obj.name) > 100 or len(f_obj.name) <= 0:
            req = {"state": "ERROR", "info": "文件名超出限定长度 100"}
            return HttpResponse(json.dumps(req), content_type='application/json')

        handle_uploaded_file("/tmp/" + f_obj.name, f_obj)
        ff = CourseFile()
        ff.course_template_experiment = courseTemplateExperiment
        ff.file_name = f_obj.name
        ff.file_path = "/tmp/" + f_obj.name
        # with open(ff.file_path, "r") as tf:
        #     ff.content = tf.read()
        ff.save()

        access_record(request, "upload", "上传课程文件：%s %s" % (ff.file_name, str(ff.uid)))

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
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        print(request.POST["courseId"])
        print(request.POST["templateId"])
        print(request.POST['templateExpId'])
        print(request.POST["fileId"])

        user = User.objects.get(uid=u_uid)
        course = Course.objects.get(uid=request.POST["courseId"])
        courseTemplate = CourseTemplate.objects.get(uid=request.POST["templateId"])
        courseTemplateExperiment = CourseTemplateExperiment.objects.get(uid=request.POST['templateExpId'])
        courseFile = CourseFile.objects.get(uid=request.POST["fileId"])

        try:
            access_record(request, "delete", "删除课件文件：%s %s" % (courseFile.file_name, str(courseFile.uid)))
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
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    user = User.objects.get(uid=u_uid)
    homework = HomeworkExperiment.objects.get(experiment__uid=homeworkId).class_homework
    courseTemplateExperiment = homework.course_template_experiment
    courseTemplate = homework.course_template_experiment.course_template
    course = homework.course_template_experiment.course_template.course
    fileClassExp = CourseFile.objects.filter(course_template_experiment=homework.course_template_experiment)

    access_record(request, "download", "下载课件文件：%s %s" % (homework.name, str(homework.uid)))

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
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        print(request.POST.get('homeworkId'))
        print(request.POST.get('homeworkFileType'))
        fileType = request.POST.get('homeworkFileType')
        f_objs = request.FILES.getlist('uploadFile')  # 暂时考虑只能上传一个文件
        user = User.objects.get(uid=u_uid)
        experiment = Experiment.objects.get(uid=request.POST.get('homeworkId'))

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

            access_record(request, "upload", "上传课程实验文件：%s %s" % (ff.file_name, str(ff.uid)))

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
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        user = User.objects.get(uid=u_uid)
        experiment = Experiment.objects.get(uid=request.POST.get('homeworkId'))
        file = File.objects.get(uid=request.POST["classFileId"])
        try:
            access_record(request, "delete", "删除课程实验文件：%s %s" % (file.file_name, str(file.uid)))
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


def download_homework_report(request, h_uid, file_type):
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    user = User.objects.get(uid=u_uid)
    if user.role != 'teacher' and user.role != 'admin':
        req = {"state": "ERROR", 'info': "Wrong role, please login correctly first."}
        return HttpResponse(json.dumps(req), content_type='application/json')
    class_homework = ClassHomework.objects.get(uid=h_uid)
    if file_type == "report":
        report_files = File.objects.filter(experiment__homeworkexperiment__class_homework=class_homework,
                                           type=file_type).order_by("user")
    else:
        report_files = File.objects.filter(experiment__homeworkexperiment__class_homework=class_homework
                                           ).order_by("user")

    access_record(request, "download", "下载学生实验报告：%s %s" % (class_homework.name, str(class_homework.uid)))

    if report_files:
        allZip = ZipUtilities()
        userZip = ZipUtilities()
        userId = ""
        newZipFileName = ""
        for f in report_files:
            if str(f.user.uid) != userId:
                if userId != "":
                    userZip.toLocal(os.path.join(config.work_dir, newZipFileName))
                    allZip.toZip(os.path.join(config.work_dir, newZipFileName), "")
                    userZip = ZipUtilities()
                userId = str(f.user.uid)
                newZipFileName = f.user.name + ".zip"

            newFileName = f.user.name + "_" + f.file_name
            if fh.get_experiment({
                config.c_userId: str(f.user.uid),
                config.c_experimentType: f.experiment.type,
                config.c_experimentId: str(f.experiment.uid),
                config.c_fileName: f.file_name,
            }, newFileName) == config.request_failed:
                break
            userZip.toZip(os.path.join(config.work_dir, newFileName), "")
        if userId != "":
            userZip.toLocal(os.path.join(config.work_dir, newZipFileName))
            allZip.toZip(os.path.join(config.work_dir, newZipFileName), "")

        response = StreamingHttpResponse(allZip.zip_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format("作业报告.zip")
        return response

    req = {"state": "ERROR", 'info': "No report files of this homework, please check first."}
    return HttpResponse(json.dumps(req), content_type='application/json')


def get_experiment_file_content(request):
    if 'is_login' not in request.session:
        return redirect('/')

    if request.method == "POST":
        file_id = request.POST.get('fileId')
        file = File.objects.get(uid=file_id)

        access_record(request, "get", "查看最新实验文件内容：%s %s" % (file.file_name, str(file.uid)))

        new_file_name = str(uuid.uuid1()) + ".tmp"
        content = fh.get_experiment({
            config.c_userId: str(file.user.uid),
            config.c_experimentType: file.experiment.type,
            config.c_experimentId: str(file.experiment.uid),
            config.c_fileName: file.file_name,
        }, new_file_name)
        if not content:
            return HttpResponse(json.dumps(response_error("获取文件数据错误")), content_type='application/json')

        try:
            data = response_ok()
            data['fileContent'] = reading_unknown_encoding_file(os.path.join(config.work_dir, new_file_name))
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception:
            return HttpResponse(json.dumps(response_error("edit not support")), content_type='application/json')


def edit_experiment_file(request):
    if 'is_login' not in request.session:
        return redirect('/')

    if request.method == "POST":
        op_type = request.POST.get('type')
        file_id = request.POST.get('fileId')
        file_content = request.POST.get('fileContent')
        print(file_id)
        print(file_content)

        file = File.objects.get(uid=file_id)
        file.content = file_content
        file.save()

        access_record(request, "edit", "编辑实验文件内容：%s %s" % (file.file_name, str(file.uid)))

        tmp_file_path = os.path.join("/tmp/", str(uuid.uuid1()) + ".tmp")
        handle_uploaded_file_str(tmp_file_path, file_content)

        with open(tmp_file_path, 'rb') as f:
            if fh.post_experiment({
                config.c_userId: str(file.user.uid),
                config.c_experimentType: file.experiment.type,
                config.c_experimentId: str(file.experiment.uid),
                config.c_fileName: file.file_name,
            }, f) == config.request_failed:
                req = {"state": "ERROR", 'info': "修改文件失败"}
                return HttpResponse(json.dumps(req), content_type='application/json')

        return HttpResponse(json.dumps(response_ok()), content_type='application/json')
