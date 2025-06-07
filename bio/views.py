from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserBio

@login_required
def bio_settings(request):
    profile, created = UserBio.objects.get_or_create(user=request.user)

    # 固定的 5 項興趣選項
    interest_choices = ['social media', 'exercise', 'Netflix', 'music', 'travel']

    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.height = request.POST.get('height') or None
        profile.weight = request.POST.get('weight') or None
        profile.department = request.POST.get('department', '')
        profile.interests = request.POST.getlist('interests')  # 多選 checkbox
        profile.save()
        return redirect('settings')

    return render(request, 'bio/bio.html', {
        'profile': profile,
        'interest_choices': interest_choices,
    })
