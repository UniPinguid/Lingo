"""
URL configuration for lingo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from lingo.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # Main screens
    path('', home, name=''),
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('dashboard', dashboard, name='dashboard'),
    # Project subscreens
    path('project', project, name='project'),
    path('project/tasks', tasks, name='tasks'),
    path('project/members', members, name='members'),
    path('project/labels', labels, name='labels'),
    path('project/contribution', contribution, name='contribution'),
    path('project/dashboard',create_project,name='create_project'),
    path('labels',create_label,name='create_label'),
    # Task screens
    path('project/tasks?id=IDHERE', task_detail, name='task_detail')
]
