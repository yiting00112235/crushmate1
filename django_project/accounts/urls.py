from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # 讓首頁就是登入畫面
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
