import uuid
from django.db import models

from Login.models import User

# Create your models here.

experiment_free = "free"
experiment_course = "course"

experiment_enum = [
    (experiment_free, experiment_free),
    (experiment_course, experiment_course),
]

burn_success = "success"
burn_fail = "fail"

burn_enum = [
    (burn_success, burn_success),
    (burn_fail, burn_fail),
]


compile_ing = "ing"
compile_success = "success"
compile_fail = "fail"
compile_unknown = "unknown"

compile_enum = [
    (compile_ing, compile_ing),
    (compile_success, compile_success),
    (compile_fail, compile_fail),
    (compile_unknown, compile_unknown),
]


class Experiment(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=8, choices=experiment_enum)
    create_time = models.DateTimeField(auto_now_add=True)


class CompileRecord(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=256)
    status = models.CharField(max_length=256)  # compile flow status, refresh in process
    message = models.TextField()  # compile flow message, refresh/append in process
    compile_start_time = models.DateTimeField(null=True)  # start compile time
    compile_end_time = models.DateTimeField(null=True)  # end compile time


class ExperimentRecord(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    device = models.CharField(max_length=32, default="")
    start_time = models.DateTimeField(auto_now_add=True)
    stop_time = models.DateTimeField()


class BurnRecord(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment_record = models.ForeignKey(ExperimentRecord, on_delete=models.CASCADE)
    file = models.CharField(max_length=256, default="")
    burn_start_time = models.DateTimeField(auto_now_add=True)
    burn_over_time = models.DateTimeField()
    status = models.CharField(max_length=8, choices=burn_enum, default=compile_unknown)
