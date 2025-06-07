from django.db import models
from django.contrib.auth.models import User

# 使用者對其他使用者按讚的紀錄
class Like(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received')
    is_liked = models.BooleanField(default=True)  # ← 加上這一行
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({'Liked' if self.is_liked else 'Disliked'})"

# 雙方互讚後建立的配對
class Match(models.Model):
    user1 = models.ForeignKey(
        User, related_name='matches_as_user1', on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User, related_name='matches_as_user2', on_delete=models.CASCADE
    )
    matched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # 避免重複配對
        ordering = ['-matched_at']

    def __str__(self):
        return f"{self.user1.username} ❤️ {self.user2.username}"

class UnmatchRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unmatches_initiated')
    unmatched_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unmatches_received')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'unmatched_user')

    def __str__(self):
        return f"{self.user.username} unmatched {self.unmatched_user.username}"