from django.db import models
from django.contrib.auth.models import User

class UserBio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)  # 單位：cm
    weight = models.PositiveIntegerField(blank=True, null=True)  # 單位：kg
    interests = models.JSONField(default=list, blank=True, null=True)  # 儲存興趣列表
    department = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} 的自我介紹"
