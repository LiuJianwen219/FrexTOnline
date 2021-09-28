import uuid
from django.db import models
from Login.models import User
from Experiment.models import Experiment
from Course.models import CourseTemplateExperiment
from Class.models import ClassHomework

# Create your models here.

file_src = "src"
file_bit = "bit"
file_log = "log"
file_other = "other"
file_unknown = "unknown"

file_enum = [
    (file_src, file_src),
    (file_bit, file_bit),
    (file_log, file_log),
    (file_other, file_other),
    (file_unknown, file_unknown),
]


class File(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=file_enum)
    create_time = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=256)
    file_path = models.CharField(max_length=512)        # 临时存放位置
    content = models.TextField()


class CourseFile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    course_template_experiment = models.ForeignKey(CourseTemplateExperiment, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=256)
    file_path = models.CharField(max_length=512)  # 临时存放位置
    content = models.TextField()
    upload_time = models.DateTimeField(auto_now_add=True)


class HomeworkFile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_homework = models.ForeignKey(ClassHomework, on_delete=models.CASCADE, null=False)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=256)
    file_path = models.CharField(max_length=512)        # 临时存放位置
    content = models.TextField()
