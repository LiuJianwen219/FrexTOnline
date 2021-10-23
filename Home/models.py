import uuid
from django.db import models
from Login.models import User, LoginRecord


class AccessRecord(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_record = models.ForeignKey(LoginRecord, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=32)
    url_path = models.CharField(max_length=128)
    raw_uri = models.CharField(max_length=256)
    body = models.TextField(default="")
    action = models.CharField(max_length=256, default="")
    other_info = models.TextField(default="")
