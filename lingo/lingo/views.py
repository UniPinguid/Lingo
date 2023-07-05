from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models.project import Project
from .models.label import Label
from .models.task import Task
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Main screens
def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'email' in request.POST and 'phone' in request.POST and 'password' not in request.POST:
            # Bước 1: Nhập thông tin
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            return render(request, 'pages/password_setup.html', {'username': username, 'email': email, 'phone': phone})
        elif 'username' in request.POST and 'email' in request.POST and 'password' in request.POST:
            # Bước 2: Nhập mật khẩu
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            phone = request.POST['phone']
            user = User.objects.create_user(username=username, email=email, password=password)
            # #user.phone = phone
            # #user.save()
            # user = User.objects.create(username=username, email=email)
            # user.set_password(password)
            # user.phone = phone
            user.save()
            return redirect(signin)
    else:
        return render(request, 'pages/signup.html')
        

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Đăng nhập thành công, chuyển hướng đến trang dashboard hoặc trang chính của ứng dụng của bạn
            return redirect(dashboard)  # Thay 'dashboard' bằng tên URL của trang dashboard của bạn
        else:
            # Đăng nhập thất bại, thông báo lỗi hoặc hiển thị lại form đăng nhập với thông báo lỗi
            error_message = "username: " + username + " password: " + password
            return render(request, 'pages/signin.html', {'error_message': error_message})
    else:
        # Hiển thị form đăng nhập
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

def dataset_classification(request):
    return render(request, 'pages/project/task/classification/dataset.html')

def dataset_classification_edit(request):
    return render(request, 'pages/project/task/classification/edit.html')

def dataset_equivalency(request):
    return render(request, 'pages/project/task/equivalency/dataset.html')

def dataset_equivalency_edit(request):
    return render(request, 'pages/project/task/equivalency/edit.html')

def dataset_qa(request):
    return render(request, 'pages/project/task/qa/dataset.html')

def dataset_qa_edit(request):
    return render(request, 'pages/project/task/qa/edit.html')

def create_project(request):
    if (request.method=='POST'):
        project_name_value = request.POST.get('project-name')
        tags_value = request.POST.get('project-tag')
        description_value = request.POST.get('project-description')
        # color = request.POST.get('project_des')
        visibility_value = request.POST.get('visibility')
        member_value = request.POST.get('project-member')
        obj = Project(projectname=project_name_value,tags=tags_value,description=description_value,visibility=visibility_value,member=member_value)
        res = obj.insertProject()
        if(res == 1):
            return JsonResponse({"message":"Tạo project thành công."})
        else:
            return JsonResponse({"message":"Tạo project thất bại."})

def create_label(request):
    if (request.method=='POST'):
        label_name_value = request.POST.get('label-name')
        description_value = request.POST.get('label-description')
        color_value = request.POST.get('label-color')
        obj = Label(labelname=label_name_value,description=description_value,color=color_value)
        try:
            obj.save()
            return JsonResponse({"message": "Tạo label thành công."})
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Có lỗi xảy ra khi tạo label."})

def task_management(request,project_id):
    project = Project.objects.get(id=project_id)
    tasks = project.task_set.all()
    return render(request, 'project/tasks.html', {'project': project, 'tasks': tasks})


def label_list(request, project_id):
    temp = Label(project_id=project_id)
    labels = temp.getLabelList(project_id)
    return render(request, 'project/labels.html', {'labels': labels})

def create_task(request):
    if (request.method=='POST'):
        title_value = request.POST.get('task-title')
        category_value = request.POST.get('task-category')
        description_value = request.POST.get('task-description')
        member_value = request.POST.get('task-member')
        obj = Task(title=title_value,category=category_value,description=description_value,member=member_value,date=datetime.now().date(),project_id=1)
        res = obj.insertTask()
        if(res == 1):
            return JsonResponse({"message":"Tạo task thành công."})
        else:
            return JsonResponse({"message":"Tạo task thất bại."})
        
# def Cuslogin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # Đăng nhập thành công, chuyển hướng đến trang dashboard hoặc trang chính của ứng dụng của bạn
#             return redirect('dashboard')  # Thay 'dashboard' bằng tên URL của trang dashboard của bạn
#         else:
#             # Đăng nhập thất bại, thông báo lỗi hoặc hiển thị lại form đăng nhập với thông báo lỗi
#             error_message = "Invalid username or password."
#             return render(request, 'signin', {'error_message': error_message})
#     else:
#         # Hiển thị form đăng nhập
#         return render(request, 'signin')