# match/views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Match, Like, UnmatchRecord
import json
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect


@csrf_exempt
@require_POST
@login_required
def swipe(request):
    data = json.loads(request.body)
    direction = data.get('direction')
    username = data.get('username')

    try:
        to_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    is_liked = (direction == 'right')

    # 儲存 Like（會更新重複的記錄）
    like_obj, _ = Like.objects.update_or_create(
        from_user=request.user,
        to_user=to_user,
        defaults={'is_liked': is_liked}
    )

    if is_liked:
        # 檢查是否雙向 Like 成功
        mutual_like = Like.objects.filter(
            from_user=to_user,
            to_user=request.user,
            is_liked=True
        ).exists()

        if mutual_like:
            # 用 user id 排序來避免重複
            user1, user2 = sorted([request.user, to_user], key=lambda u: u.id)
            Match.objects.get_or_create(user1=user1, user2=user2)
            return JsonResponse({'status': 'match'})

    return JsonResponse({'status': 'ok'})

@login_required
def unmatch_view(request, username):
    to_user = get_object_or_404(User, username=username)

    # 刪除配對
    match = Match.objects.filter(
        Q(user1=request.user, user2=to_user) | Q(user1=to_user, user2=request.user)
    ).first()
    if match:
        match.delete()

    # 刪除 Like
    Like.objects.filter(from_user=request.user, to_user=to_user).delete()
    Like.objects.filter(from_user=to_user, to_user=request.user).delete()

    # 新增 Unmatch 紀錄
    UnmatchRecord.objects.get_or_create(user=request.user, unmatched_user=to_user)
    UnmatchRecord.objects.get_or_create(user=to_user, unmatched_user=request.user)

    return redirect('user_list')  # 或 chat list/home