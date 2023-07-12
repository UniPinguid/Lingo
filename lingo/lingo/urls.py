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
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Main screens
    path('', home, name=''),
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('dashboard', dashboard, name='dashboard'),
    # Project subscreens
    path('project/<int:project_id>', project, name='project'),
    path('project/tasks', tasks, name='tasks'),
    path('project/members', members, name='members'),
    path('project/labels', labels, name='labels'),
    path('project/contribution', contribution, name='contribution'),
    path('project/dashboard',create_project,name='create_project'),
    path('project/main',upload_dataset,name='upload_dataset'),
    path('labels',create_label,name='create_label'),
    path('task',create_task,name='create_task'),
    path('get_matching_usernames/', get_matching_usernames, name='get_matching_usernames'),
    path('/process_project_members/', process_project_members, name='process_project_member'),
    # Task screens
    path('project/tasks/<int:taskid>', task_detail, name='task_detail'),
    path('project/tasks/class/<int:taskid>', dataset_classification, name='dataset_classification'),
    path('project/tasks?id=IDHERE/IDDATASET?edit=true', dataset_classification_edit, name='classification_edit'),
    path('project/tasks/equal/<int:datasetid>', dataset_equivalency, name='dataset_equivalency'),
    path('project/tasks/equal/edit/<int:datasetid>', dataset_equivalency_edit, name='equivalency_edit'),
    path('project/tasks/qa/<int:datasetid>', dataset_qa, name='dataset_qa'),
    path('project/tasks/qa/edit/<int:datasetid>', dataset_qa_edit, name='qa_edit'),
    #path('project/tasks/qa/edit/save', dataset_qa_edit_save, name='qa_edit_save'),
    path('project/tasks?id=IDHERE/IDDATASETTS', dataset_translation, name='dataset_translation'),
    path('project/tasks?id=IDHERE/IDDATASETS?edit=true', dataset_translation_edit, name='translation_edit'),
    path('project/tasks/<int:task_id>/<int:dataset_id>?edit=true', display_dataset,name='display_dataset'),
    path('translate',labeling_translate,name='labeling_translate'),
    path('get_datasets/', get_datasets, name='get_datasets'),

    #Favicon
    path(r'^favicon\.ico$', favicon_view)
]
