# match/urls.py
from django.urls import path
from .views import swipe, unmatch_view  # ✅ 匯入你需要的 view 函式

app_name = 'match'

urlpatterns = [
    path('swipe/', swipe, name='swipe'),
    path('unmatch/<str:username>/', unmatch_view, name='unmatch'),
]
