from . import views 
from django.urls import path
from .views import profile_page, delete_photo

urlpatterns = [
    path('profile/', profile_page, name='profilepage'),
    path('delete/<int:photo_id>/', delete_photo, name='delete_photo'),
    path('set_main/<int:photo_id>/', views.set_main_photo, name='set_main_photo'),
    path('upload_main_avatar/', views.upload_main_avatar, name='upload_main_avatar'),

]
