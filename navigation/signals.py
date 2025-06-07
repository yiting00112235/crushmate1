from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from profilepage.models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # 使用 get_or_create 可以避免 race condition
        Profile.objects.get_or_create(user=instance)
    else:
        # 這裡直接用 try 會更安全
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)

