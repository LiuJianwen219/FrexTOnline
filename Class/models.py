import uuid
from django.db import models
from Login.models import User
from Experiment.models import Experiment
from Course.models import Course, CourseTemplate, CourseTemplateExperiment

# Create your models here.


class TheClass(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_template = models.ForeignKey(CourseTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)  # 班级名字
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()


class ClassStudent(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    the_class = models.ForeignKey(TheClass, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enter_time = models.DateTimeField(auto_now_add=True)


class ClassHomework(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    the_class = models.ForeignKey(TheClass, on_delete=models.CASCADE)
    course_template_experiment = models.ForeignKey(CourseTemplateExperiment, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)  # 作业名字，目前可以等于课程模板实验名字
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
