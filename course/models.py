from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class UserCourseSchedule(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    schedule = JSONField(default=dict)  # 用 { "Mon-1": "Math", ... } 的形式儲存

    def __str__(self):
        return f"{self.user.username} 的課表"
