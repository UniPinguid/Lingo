from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models.project import Project
from .models.label import Label
from .models.task import Task

# Main screens
def home(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'pages/signup.html')

def signin(request):
    return render(request, 'pages/signin.html')

def dashboard(request):
    return render(request, 'pages/dashboard.html')

# Project subscreens

def project(request):
    return render(request, 'pages/project/main.html')

def members(request):
    return render(request, 'pages/project/members.html')

def tasks(request):
    return render(request, 'pages/project/tasks.html')

def labels(request):
    return render(request, 'pages/project/labels.html')

def contribution(request):
    return render(request, 'pages/project/contribution.html')

# Tasks screen
def task_detail(request):
    return render(request, 'pages/project/task/detail.html')

def dataset(request):
    return render(request, 'pages/project/task/dataset.html')

def dataset_edit(request):
    return render(request, 'pages/project/task/edit.html')

def create_project(request):
    if (request.method=='POST'):
        project_name_value = request.POST.get('project-name')
        tags_value = request.POST.get('project-tag')
        description_value = request.POST.get('project-description')
        # color = request.POST.get('project_des')
        visibility_value = request.POST.get('visibility')
        member_value = request.POST.get('project-member')
        obj = Project(projectname=project_name_value,tags=tags_value,description=description_value,visibility=visibility_value,member=member_value)
        obj.save()
        return JsonResponse({"message":"Tạo project thành công."})

def create_label(request):
    if (request.method=='POST'):
        label_name_value = request.POST.get('label-name')
        description_value = request.POST.get('label-description')
        color_value = request.POST.get('label-color')
        obj = Label(labelname=label_name_value,description=description_value,color=color_value)
        try:
            obj.save()
            print("data vô rồi")
            return JsonResponse({"message": "Tạo label thành công."})
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Có lỗi xảy ra khi tạo label."})

def task_management(request,project_id):
    project = Project.objects.get(id=project_id)
    tasks = project.task_set.all()
    return render(request, 'project/tasks.html', {'project': project, 'tasks': tasks})