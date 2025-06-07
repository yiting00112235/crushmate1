from profilepage.models import ProfilePhoto
from match.models import Like, Match
from bio.models import UserBio
from course.models import UserCourseSchedule  # ✅ 改成正確模型
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from match.models import UnmatchRecord

@login_required
def home(request):
    try:
        my_schedule = UserCourseSchedule.objects.get(user=request.user).schedule
    except UserCourseSchedule.DoesNotExist:
        my_schedule = {}

    # ✅ 檢查自己是否已上傳主照片
    has_main_photo = ProfilePhoto.objects.filter(user=request.user, is_main=True).exists()

    unmatched_users = UnmatchRecord.objects.filter(user=request.user).values_list('unmatched_user', flat=True)
    other_users = User.objects.exclude(id=request.user.id).exclude(id__in=unmatched_users)
    recommendations = []

    for user in other_users:
        if Like.objects.filter(from_user=request.user, to_user=user).exists():
            continue
        if Match.objects.filter(user1=request.user, user2=user).exists() or \
           Match.objects.filter(user1=user, user2=request.user).exists():
            continue

        try:
            user_schedule = UserCourseSchedule.objects.get(user=user).schedule
        except UserCourseSchedule.DoesNotExist:
            user_schedule = {}

        course_match_count = sum(
            1 for key in my_schedule
            if (
                key in user_schedule and
                my_schedule[key] and
                user_schedule[key] and
                my_schedule[key] == user_schedule[key]
            )
        )
        main_photo = ProfilePhoto.objects.filter(user=user, is_main=True).first()
        other_photos = ProfilePhoto.objects.filter(user=user, is_main=False)

        try:
            bio_obj = UserBio.objects.get(user=user)
            bio = bio_obj.bio
            department = bio_obj.department
        except UserBio.DoesNotExist:
            bio = ""
            department = ""

        if main_photo:
            recommendations.append({
                "user": user,
                "main_photo": main_photo,
                "other_photos": other_photos,
                "bio": bio,
                "department": department,
                "course_match_count": course_match_count,
            })

    recommendations.sort(key=lambda x: x['course_match_count'], reverse=True)

    return render(request, 'navigation/home.html', {
        "recommendations": recommendations,
        "has_main_photo": has_main_photo  # ✅ 新增
    })
