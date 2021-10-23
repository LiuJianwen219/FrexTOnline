import json
import logging
import time

import requests

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

from apscheduler.schedulers.background import BackgroundScheduler

from Class.models import ClassHomework, HomeworkExperiment
from Compile.thread_handler import TaskHandlerThread, TimeCounter
from Compile.compile_task import CompileTaskThread, send_task_to_rabbit_mq
from File.models import File, file_bit, file_log
from FrexTOnline.views import response_error, response_ok
from Home.views import access_record
from Login.models import User
from Experiment.models import Experiment, experiment_free, CompileRecord, ExperimentRecord, BurnRecord, compile_ing
from FrexTOnline.settings import Compile_MAX_Thread, Compile_MAX_Time, Judge_MAX_Time
import File.utils as fh
import config

# Create your views here.
logger = logging.getLogger(__name__)

compile_checker = None
threadIndex = 0
threadList = {}

# judgeChecker = None
# judgeThreadIndex = 0
# judgeThreadList = {}

countCom = 0


# countJud = 0


def introduce(request):
    return render(request, 'Home/studentHome.html')


@csrf_exempt
def create_free_project(request):
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        experiment_name = request.POST["freeExpName"]
        if len(experiment_name) > 100 or len(experiment_name) == 0:
            data = {"state": "ERROR", "info": "实验名称过长 100"}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            user = User.objects.get(uid=u_uid)
            redundancy = Experiment.objects.filter(user=user, name=experiment_name)
            if len(redundancy) != 0:
                data = {"state": "ERROR", 'info': "同名实验已存在"}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                experiment = Experiment(user=user, name=experiment_name, type=experiment_free)
                experiment.save()
                access_record(request, "create", "创建自由实验：%s %s" % (experiment_name, str(experiment.uid)))
                data = {"state": "OK", "trueExpName": experiment_name, "expId": str(experiment.uid)}
                return HttpResponse(json.dumps(data), content_type='application/json')

    data = {"state": "ERROR", "info": "非法请求"}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def delete_free_project(request):
    if 'is_login' not in request.session:
        return redirect('/')

    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        expId = request.POST["expId"]
        user = User.objects.get(uid=u_uid)
        experiments = Experiment.objects.filter(user=user, uid=expId)
        if len(experiments) != 0:
            for experiment in experiments:
                files = File.objects.filter(experiment=experiment)
                for file in files:
                    file.delete()
                    if fh.delete_experiment({
                        config.c_userId: str(user.uid),
                        config.c_experimentType: experiment.type,
                        config.c_experimentId: str(experiment.uid),
                        config.c_fileName: file.file_name,
                    }) == config.request_failed:
                        req = {"state": "ERROR", 'info': "删除文件失败"}
                        return HttpResponse(json.dumps(req), content_type='application/json')
                access_record(request, "delete", "删除自由实验：%s %s" % (experiment.name, str(experiment.uid)))
                experiment.delete()
            data = {"state": "OK", "info": "删除成功"}
            return HttpResponse(json.dumps(data), content_type='application/json')
        data = {"state": "ERROR", 'info': "实验不存在，请确认"}
        return HttpResponse(json.dumps(data), content_type='application/json')

    data = {"state": "ERROR", "info": "非法请求"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def free_compile(request):
    if 'is_login' not in request.session:
        return redirect('/')

    experiment = Experiment.objects.get(uid=request.POST["freeExpId"])
    access_record(request, "compile free", "编译自由实验：%s %s" % (experiment.name, str(experiment.uid)))
    return compile_all(request, experiment)


def course_compile(request):
    if 'is_login' not in request.session:
        return redirect('/')

    experiment = Experiment.objects.get(uid=request.POST.get('homeworkId'))
    access_record(request, "compile course", "编译课程实验：%s %s" % (experiment.name, str(experiment.uid)))
    return compile_all(request, experiment)


def compile_all(request, experiment):
    u_uid = request.session["u_uid"]
    if not u_uid:
        return redirect('/login/')

    if request.method == "POST":
        user = User.objects.get(uid=u_uid)
        topModuleName = request.POST["topModuleName"]
        fileNameOther = request.POST["fileNameOther"]
        # experiment = Experiment.objects.get(uid=request.POST["freeExpId"])
        # experiment = HomeworkExperiment.objects.get(class_homework_id=request.POST.get('homeworkId')).experiment
        files = File.objects.filter(experiment=experiment)
        compile_record = CompileRecord(user=user, experiment=experiment, file_name=fileNameOther)
        compile_record.save()

        fileNames = []
        for file in files:
            if file.type == "src":
                fileNames.append(file.file_name)

        content = {
            'userId': request.session['u_uid'],
            'experimentType': experiment.type,
            'experimentId': str(experiment.uid),
            'compileId': str(compile_record.uid),
            'fileNames': fileNames,
            'topModuleName': topModuleName,
            'file_name_other': fileNameOther,
        }

        global compile_checker
        if not compile_checker:
            compile_checker = BackgroundScheduler()
            compile_checker.add_job(detect_compile, "interval", seconds=5)
            compile_checker.start()
        compile_checker.pause()

        global threadList
        global threadIndex
        if len(threadList) >= Compile_MAX_Thread:  # 表示当前没有编译线程资源
            data = {"state": "OK", "testState": "暂时没有编译线程资源，请稍后重新提交 " + str(threadList), "info": "Waiting"}
            compile_checker.resume()
            return HttpResponse(json.dumps(data), content_type='application/json')

        content['threadIndex'] = str(threadIndex)  # 0
        # threadList[content['threadIndex']] = CompileHandleThread(TaskHandlerThread(CompileTaskThread, content),
        #                                                          TimeCounter(Compile_MAX_Time))  # 0
        threadList[content['threadIndex']] = TaskHandlerThread(
            CompileTaskThread(send_task_to_rabbit_mq, content), TimeCounter(Compile_MAX_Time))
        threadIndex += 1  # 1

        threadList[content['threadIndex']].start()
        print("compile start: " + json.dumps(content))

        compile_checker.resume()

        data = {"state": "OK", "testState": "提交成功，接下来交给后台处理", "info": "task submit"}
        return HttpResponse(json.dumps(data), content_type='application/json')

    data = {"state": "ERROR", "testState": "非POST请求", "info": "task submit error"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def detect_compile():
    global threadList
    global countCom
    if len(threadList) > 0 or countCom < 10:
        print("detect com " + str(len(threadList)))
        if len(threadList) == 0:
            countCom += 1
        else:
            countCom = 0

    needToDel = []
    for key in threadList:
        if threadList[key].get_time() > Compile_MAX_Time:  # 表示编译超时
            print("compile timeout: " + json.dumps(threadList[key].get_contents()))
            submit = CompileRecord.objects.get(uid=threadList[key].get_content("compileId"))
            submit.status = "编译超时，请稍后重新提交"
            submit.message += "Failed: code compile task time out.\n"
            submit.save()
            needToDel.append(threadList[key].get_content("threadIndex"))
        if threadList[key].get_task_result() is not None:  # 表示编译任务提交到了RabbitMQ
            # print("task submit over: " + json.dumps(threadList[key].get_contents()))
            result = threadList[key].get_task_result()
            # print("task submit over: " + json.dumps(result))
            if result['state'] == 'OK':
                # submit = SubmitList.objects.get(uid=threadList[key].get_content("submitId"))
                # submit.status = "提交编译任务成功"
                # submit.message += "Success: code compile task submit complete.\n"
                # submit.save()
                if not threadList[key].task_thread.is_sub_over():
                    submit = CompileRecord.objects.get(uid=threadList[key].get_content("compileId"))
                    submit.status = "提交编译任务成功"
                    submit.message += "Success: code compile task submit complete.\n"
                    submit.compile_start_time = datetime.now()
                    submit.save()
                    threadList[key].task_thread.set_sub_over()
                elif threadList[key].task_thread.is_over():
                    needToDel.append(key)
                else:
                    submit = CompileRecord.objects.get(uid=threadList[key].get_content("compileId"))
                    submit.status = "提交编译任务成功，编译{0}秒".format(threadList[key].get_time())
                    submit.message += str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + \
                                      " Running: compile {0} seconds\n".format(threadList[key].get_time())
                    submit.save()
            else:
                submit = CompileRecord.objects.get(uid=threadList[key].get_content("compileId"))
                submit.status = "提交编译任务失败，请重新提交"
                submit.message += "Failed: code compile task submit error.\n"
                submit.compile_end_time = datetime.now()
                submit.save()
                needToDel.append(key)
        threadList[key].time_add()

    for k in needToDel:
        print("compile thread delete: " + json.dumps(threadList[k].get_contents()))
        del threadList[k]


def get_compile_status(request):
    if 'is_login' not in request.session:
        return redirect('/')

    if request.method == "POST":
        e_uid = request.POST["expId"]
        compiles = CompileRecord.objects.filter(experiment__uid=e_uid).order_by('-compile_start_time')[:10]
        compile_status = []

        access_record(request, "get", "查看编译结果：%s" % e_uid)

        for c in compiles:
            compile_status.append({
                'fileName': c.file_name,
                'startTime': c.compile_start_time.__str__(),
                'stopTime': c.compile_end_time.__str__(),
                'status': c.status,
            })
        data = response_ok()
        data['compileStatus'] = compile_status
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(json.dumps(response_error("非法请求，请登陆")), content_type='application/json')


@csrf_exempt
def compile_result(request):
    if request.method == "POST":
        values = {
            "userId": request.POST.get("userId", None),
            "experimentType": request.POST.get("experimentType", None),
            "experimentId": request.POST.get("experimentId", None),
            "compileId": request.POST.get("compileId", None),
            "topModuleName": request.POST.get("topModuleName", None),
            "state": request.POST.get("state", None),
            "status": request.POST.get("status", None),
            "message": request.POST.get("message", None),
            "threadIndex": request.POST.get("threadIndex", None),
        }
        print(values)
        print(values["status"])

        submit = CompileRecord.objects.get(uid=values["compileId"])
        submit.status = values["status"]
        submit.message = submit.message + values["message"] + "\n"
        submit.compile_end_time = datetime.now()
        global threadList
        submit.comTime = threadList[values["threadIndex"]].get_time()
        submit.save()
        file_name_other = threadList[values["threadIndex"]].get_content('file_name_other')
        threadList[values["threadIndex"]].task_thread.set_over()

        # print(request.session['u_uid'])
        print(values['userId'])
        user = User.objects.get(uid=values['userId'])
        exp = Experiment.objects.get(uid=values["experimentId"])

        logFile = File()
        logFile.user = user
        logFile.experiment = exp
        logFile.type = file_log
        logFile.file_name = values["compileId"] + ".log"
        logFile.file_name_other = file_name_other + ".log"
        # logFile.content =
        logFile.save()

        if values['status'] != "编译成功":  # from FrexTCompiler final result
            data = {"state": "ERROR", 'trueFileName': "",
                    'fileId': "", 'info': "编译失败"}
            return HttpResponse(json.dumps(data), content_type='application/json')

        bitFile = File()
        bitFile.user = user
        bitFile.experiment = exp
        bitFile.type = file_bit
        bitFile.file_name = values["compileId"] + ".bit"
        bitFile.file_name_other = file_name_other + ".bit"
        # bitFile.content =
        bitFile.save()

        data = {"state": "OK", 'trueFileName': values["compileId"] + ".bit",
                'fileId': str(bitFile.uid), 'info': "编译成功"}
        return HttpResponse(json.dumps(data), content_type='application/json')

    data = {"state": "ERROR", "testState": "非POST请求", "info": "task submit error"}
    return HttpResponse(json.dumps(data), content_type='application/json')


SWState0 = ["1", "1", "0", "0", "1", "1", "0", "0", "0", "0", "0", "1", "1", "0", "0", "0"]
SWState2 = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
BTNState0 = ["1", "1", "0", "0", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
BTNState2 = [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
segMent = [0, 0, 2, 3, 4, 5, 6, 7]
ledState = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def experiment_start(request):
    if 'is_login' not in request.session:
        return redirect('/')

    type = request.GET.get('type')  # 有用
    print(type)
    expId = request.GET.get('expId')
    print(expId)
    try:
        experiment = Experiment.objects.get(uid=expId)
    except Experiment.DoesNotExist:
        experiment = HomeworkExperiment.objects.get(class_homework_id=expId).experiment

    user = User.objects.get(uid=request.session['u_uid'])
    experiment_record = ExperimentRecord(user=user, experiment=experiment)
    experiment_record.save()

    access_record(request, "experiment", "开始实验：er/%s e/%s e/%s" % (str(experiment_record.uid),
                                                                   experiment.name, str(experiment.uid)))

    bitFileList = []
    files = File.objects.filter(experiment=experiment)
    for f in files:
        if f.file_name.split('.')[-1] == "bit":
            bitFileList.append({
                'fileName': f.file_name,
                'fileNameOther': f.file_name_other,
            })

    context = {
        "expName": experiment.name,
        "SWState2": SWState2,
        "SWState": [
            {"id": "0", "state": "off"},
            {"id": "1", "state": "on"},
            {"id": "2", "state": "off"},
            {"id": "3", "state": "on"},
            {"id": "4", "state": "off"},
            {"id": "5", "state": "on"},
            {"id": "6", "state": "off"},
            {"id": "7", "state": "on"},
            {"id": "8", "state": "off"},
            {"id": "9", "state": "off"},
            {"id": "10", "state": "off"},
            {"id": "11", "state": "off"},
            {"id": "12", "state": "off"},
            {"id": "13", "state": "off"},
            {"id": "14", "state": "off"},
            {"id": "15", "state": "off"},
        ],
        "BTNState": BTNState2,
        "segMent": segMent,
        "ledState": ledState,
        "type": type,
        "expId": expId,
        "userId": user.uid,
        "bitFileList": bitFileList,
        # "bitFile": base64.b64encode(bitFile),
        # "bitFile": bitFile,
        "experiment_record": str(experiment_record.uid),
    }
    print(request)
    return render(request, "Experiment/experiment.html", context=context)


def experiment_status(request):
    if 'is_login' not in request.session:
        return redirect('/')

    experiment_record_uid = request.POST.get('experiment_record_uid')
    experiment_record = ExperimentRecord.objects.get(uid=experiment_record_uid)
    experiment_record.last_check_time = datetime.now()
    experiment_record.device = request.POST.get('device_id')
    experiment_record.save()

    access_record(request, "experiment", "正在实验：er/%s e/%s e/%s" % (str(experiment_record.uid),
                                                                   experiment_record.experiment.name,
                                                                   str(experiment_record.experiment.uid)))

    return HttpResponse(json.dumps(response_ok()), content_type='application/json')


def burn_bit(request):
    if 'is_login' not in request.session:
        return redirect('/')

    experiment_record_uid = request.POST.get('experiment_record_uid')
    experiment_record = ExperimentRecord.objects.get(uid=experiment_record_uid)
    bit_file_name = request.POST.get('bit_file_name')
    file = File.objects.get(experiment=experiment_record.experiment, file_name=bit_file_name)
    user = User.objects.get(uid=request.session['u_uid'])

    burn_record = BurnRecord(user=user, experiment_record=experiment_record, file=file, status=compile_ing)
    burn_record.save()

    access_record(request, "bit", "下载bit文件：er/%s e/%s e/%s f/%s b/%s" % (str(experiment_record.uid),
                                                                         experiment_record.experiment.name,
                                                                         str(experiment_record.experiment.uid),
                                                                         str(file.uid),
                                                                         str(burn_record.uid)))

    data = response_ok()
    data['burn_record_uid'] = str(burn_record.uid)
    return HttpResponse(json.dumps(data), content_type='application/json')


def burn_bit_status(request):
    if 'is_login' not in request.session:
        return redirect('/')

    burn_record_uid = request.POST.get('burn_record_uid')
    burn_record = BurnRecord.objects.get(uid=burn_record_uid)
    experiment_record = burn_record.experiment_record
    status = request.POST.get('status')
    burn_record.status = status
    burn_record.burn_over_time = datetime.now()
    burn_record.save()

    access_record(request, "bit", "下载bit文件状态：%s er/%s e/%s e/%s b/%s" % (status, str(experiment_record.uid),
                                                                         experiment_record.experiment.name,
                                                                         str(experiment_record.experiment.uid),
                                                                         str(burn_record.uid)))
    return HttpResponse(json.dumps(response_ok()), content_type='application/json')
