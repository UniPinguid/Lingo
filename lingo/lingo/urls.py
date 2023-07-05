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
    path('project/tasks?id=IDHERE', task_detail, name='task_detail'),
    path('project/tasks?id=IDHERE/IDDATASET', dataset_classification, name='dataset_classification'),
    path('project/tasks?id=IDHERE/IDDATASET?edit=true', dataset_classification_edit, name='classification_edit'),
    path('project/tasks?id=IDHERE/IDDATASETEQ', dataset_equivalency, name='dataset_equivalency'),
    path('project/tasks?id=IDHERE/IDDATASETEQ?edit=true', dataset_equivalency_edit, name='equivalency_edit'),
    path('project/tasks?id=IDHERE/IDDATASETQA', dataset_qa, name='dataset_qa'),
    path('project/tasks?id=IDHERE/IDDATASETQA?edit=true', dataset_qa_edit, name='qa_edit')
]
