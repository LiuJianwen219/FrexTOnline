import uuid
from django.db import models
from Login.models import User

# Create your models here.


class Course(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)     # 课程名字
    create_time = models.DateTimeField(auto_now_add=True)


class CourseTemplate(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)     # 课程模板名字
    create_time = models.DateTimeField(auto_now_add=True)


class CourseTemplateExperiment(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    course_template = models.ForeignKey(CourseTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)     # 课程模板实验名字
    create_time = models.DateTimeField(auto_now_add=True)
