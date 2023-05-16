"""drfauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from users.views import views
from users.views import breadrumbs_views
from users.views import profile_views
from users.views import test_views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('profile/', profile_views.ProfileView.as_view()),
    path('profile/update_avatar', profile_views.ProfileAvatarView.as_view()),
    path('profile/courses/', views.ProfileCoursesView.as_view()),
    path('courses/<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('lessons/<int:lesson_id>/', views.LessonStepsView.as_view(), name='lesson_steps'),
    path('steps/<int:step_id>/', views.StepDetailView.as_view(), name='step_detail'),
    path('test/<int:test_id>/', test_views.TaskTestView.as_view(), name='test_view'),
    path('test/check/<int:test_id>/', test_views.CheckTaskTestView.as_view(), name='test_view'),
    path('test/results/<int:test_id>/', test_views.ResultsTaskTestView.as_view(), name='test_view'),
    path('stats/', views.StatsView.as_view(), name='stats_view'),
    path('breadcrumbs/', breadrumbs_views.BreadcrumbsView.as_view(), name='breadcrumbs_view')
    # получить все степы по уроку
    # получить материал по html ресурсу
    # получить данные по тестам
    # принять данные теста
    # выдать статистику по курсу, теме, уроку
]
