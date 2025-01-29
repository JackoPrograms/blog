from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('pentest/', views.pentest, name='pentest'),
    path('security/', views.security, name='security'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Здесь передаётся аргумент pk при формировании url адреса на странице pentest.html и security.html, а отсюда он передаются в функцию views.post_detail
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]

# Эти настройки помагли добавить изображение к превтю статьи (часть 4)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)