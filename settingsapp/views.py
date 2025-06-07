from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profilepage.models import ProfilePhoto, Profile

@login_required
def settings_page(request):
    profile = Profile.objects.filter(user=request.user).first()
    main_photo = ProfilePhoto.objects.filter(user=request.user, is_main=True).first()

    return render(request, 'settingsapp/settings.html', {
        'user_profile': {
            'main_photo': main_photo,
            # 直接移除 department，或保留空字串以防模板錯誤
            'department': ''
        }
    })
