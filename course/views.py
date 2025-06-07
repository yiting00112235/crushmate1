from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserCourseSchedule

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
PERIODS = range(1, 10)
COURSE_OPTIONS = ['Math', 'German', 'English', 'Korean', 'Japanese']

@login_required
def course(request):
    schedule_obj, _ = UserCourseSchedule.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        schedule_data = {}
        for day in DAYS:
            for period in PERIODS:
                key = f"{day}-{period}"
                schedule_data[key] = request.POST.get(key, "")
        schedule_obj.schedule = schedule_data
        schedule_obj.save()
        return redirect('course')

    # ✅ 建立二維表格結構供 template 使用
    table = {day: {} for day in DAYS}
    for day in DAYS:
        for period in PERIODS:
            key = f"{day}-{period}"
            table[day][period] = schedule_obj.schedule.get(key, "")

    return render(request, 'course/course.html', {
        'schedule': schedule_obj.schedule,
        'table': table,
        'days': DAYS,
        'periods': PERIODS,
        'courses': COURSE_OPTIONS,
    })
