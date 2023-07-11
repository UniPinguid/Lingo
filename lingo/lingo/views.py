import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models.project import Project
from .models.label import Label
from .models.task import Dataset, Task
from .models.user import CusUser
from .models.taskindividual import TaskIndividual
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
from .settings import USERNAME
from django.utils import timezone
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
            #cuser = CusUser(phone, "1")
            #cuser.addUser()
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
            request.session['username'] = username
            USERNAME = username
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
    try:
        projects = Project.objects.filter(member__icontains=request.user.username)
    except MemoryError:
        projects = None
        return 0

    return render(request, 'pages/dashboard.html', { 'projects': projects })

# Project subscreens

def project(request, project_id):
    request.session['projectid'] = project_id
    temp = Project.objects.get(id_project = int(project_id))
    return render(request, 'pages/project/main.html', {'project': temp})

def members(request):
    return render(request, 'pages/project/members.html')

def tasks(request):
    projectid = request.session.get('projectid')
    tasks = Task.objects.filter(project_id = projectid)

    return render(request, 'pages/project/tasks.html', {'project_id': projectid, 'tasks':tasks})

def labels(request):
    return render(request, 'pages/project/labels.html')

def contribution(request):
    return render(request, 'pages/project/contribution.html')

# Tasks screen
def task_detail(request):
    request.session['taskid'] = request.GET.get('taskid')
    task = Task.objects.get(taskid = request.session['taskid'])
    datasets = task.datasets
    return render(request, 'pages/project/task/detail.html', {'project_id': request.session.get('projectid')
                                                              , 'cate': task.category, 'datasets': datasets})

def dataset_classification(request):
    return render(request, 'pages/project/task/classification/dataset.html')

def dataset_classification_edit(request):
    return render(request, 'pages/project/task/classification/edit.html')

def dataset_equivalency(request, datasetid):
    request.session['datasetid'] = request.GET.get('datasetid')
    dataset_id = int(datasetid)
    t = Task.objects.get(request.session.get('taskid'))
    datasets = t.datasets
    for dataset in datasets:
        if (dataset['datasetid'] == dataset_id):
            return render(request, 'pages/project/task/equivalency/dataset.html', {'dataset': dataset})
    

def dataset_equivalency_edit(request, datasetid):
    if (request.method == 'POST'):
        user = request.user.username
        task_id = request.session.get('taskid')
        dataset1 = request.POST['dataset1']
        dataset2 = request.POST['dataset2']
        label = request.POST['label']
        dataset_id = int(datasetid)
        revise = False

        task_individual = TaskIndividual.objects.filter(user=user, task=task_id).first()
        if task_individual is None:
            # Tạo document mới nếu chưa tồn tại
            task_individual = TaskIndividual(user=request.user.username, task=task_id, labeling=[])
        # Thêm thông tin gán nhãn vào document
        dataset_label = {"datasetid":dataset_id, "Data": [dataset1, dataset2], "label": label}
        task_individual.labeling.append(dataset_label)
        task_individual.revise = revise
        task_individual.done = not revise

        # Lưu document vào collection Task_Individual
        task_individual.save()

        # Chuyển hướng về trang danh sách dataset hoặc trang khác tùy ý
        return redirect(task_detail)

    elif(request.method == 'GET'):
        task_id = request.session.get('taskid')
        dataset_id = int(datasetid)
        task = Task.objects.get(taskid=task_id)
        datasets = task.datasets
        dataset1 = "System Error"
        dataset2 = "System Error"
        for dataset in datasets:
            if (dataset['datasetid'] == dataset_id):
                dataset1 = dataset['content'][0]
                dataset2 = dataset['content'][1]
                return render(request, 'pages/project/task/equivalency/edit.html'
                      , {"dataset_id": dataset_id, "task_id": task_id, "dataset1": dataset1,
                         "dataset2": dataset2})
        

def dataset_qa(request):
    return render(request, 'pages/project/task/qa/dataset.html')

def dataset_qa_edit(request, datasetid):
    if(request.method == "GET"):
        task_id = request.session.get('taskid')
        dataset_id = dataset_id
        task = Task.objects.get(taskid=task_id)
        datasets = task.datasets
        ques = "System Error"
        for dataset in datasets:
            if (dataset['datasetid'] == dataset_id):
                ques = dataset['content']
        
        return render(request, 'pages/project/task/qa/edit.html', {'dataset_id': dataset_id, "ques": ques, 'task_id': task_id})
    elif (request.method == "POST"):
        ques = request.POST.get('ques')
        ans = request.POST.get('ans')
        task_value = request.session.get('taskid')
        dataset_id = datasetid
        task_individual = TaskIndividual.objects.filter(user=request.user.username,task=task_value).first()
        if (task_individual is None):
            task_individual = TaskIndividual(user=request.user.username,task=task_value,labeling=[])
        label = {"dataset_id": dataset_id, "Dataset":ques, "Requirement": "Answer the Question", "Label":ans}
        task_individual.labeling.append(label)
        task_individual.revise = False
        task_individual.done = True
        task_individual.time = datetime.now()
        task_individual.save()
        return JsonResponse({"message":"Gán nhãn dịch thành công."})
        

# def dataset_qa_edit_save(request):
#     if(request.method == 'POST'):
#         ques = request.POST.get('ques')
#         ans = request.POST.get('ans')
#         task_value = request.POST.get('taskid')
#         dataset_id = request.POST.get('dataset_id')
#         task_individual = TaskIndividual.objects.filter(user=USERNAME,task=task_value).first()
#         if (task_individual is None):
#             task_individual = TaskIndividual(user=USERNAME,task=task_value,labeling=[])
#         label = {"dataset_id": dataset_id, "Dataset":ques, "Requirement": "Answer the Question", "Label":ans}
#         task_individual.labeling.append(label)
#         task_individual.revise = False
#         task_individual.done = True
#         task_individual.time = datetime.now()
#         task_individual.save()
#         return JsonResponse({"message":"Gán nhãn dịch thành công."})
    
    




def dataset_translation(request):
    return render(request, 'pages/project/task/translation/dataset.html')

def dataset_translation_edit(request):
    return render(request, 'pages/project/task/translation/edit.html')

def upload_dataset(request):
    if(request.method == "POST"):
        file = request.FILES['dataset']
        file_content = file.read().decode("utf-8")
        project_id = request.session.get('projectid')
        project1 = Project.objects.get(project_id = project_id)
        dataset = {
            "Tên hiển thị": file.name,
            "content": file_content,
            "time": timezone.now()
        }

        project1.datasets.append(dataset)
        project1.save()
        return JsonResponse({"message": "Import thành công"})

        

def create_project(request):
    if (request.method=='POST'):
        project_name_value = request.POST.get('project-name')
        tags_value = request.POST.get('project-tag')
        description_value = request.POST.get('project-description')
        # color = request.POST.get('project_des')
        visibility_value = request.POST.get('visibility')
        member_value = []
        member_value.extend(request.POST.get('project-member'))
        member_value.append(request.user.username)
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
        project_id = request.session.get('projectid')
        obj = Task(title=title_value,category=category_value,description=description_value,member=member_value,date=datetime.now().date(),project_id=1)
        res = obj.insertTask()
        if(res == 1):
            return JsonResponse({"message":"Tạo task thành công."})
        else:
            return JsonResponse({"message":"Tạo task thất bại."})
        
def dataset_qa(request):
    if (request.method == "GET"):
        try:
            task = Task.objects.filter(id=request.GET.get('task_id'))
        except NameError:
            task = None 
        return render(request, 'pages/project/task/qa/dataset.html', {'task': task})
    elif(request.method == "POST"):
        return 0


def display_dataset(request, task_id, dataset_id):
    task_id = int(task_id)
    dataset_id = int(dataset_id)
    task = Task.objects.get(taskid=task_id)
    datasets = task.datasets
    for dataset in datasets:
        if (dataset['datasetid']==dataset_id):
            content = dataset['content']
            requirement = dataset['requirement']
            

    return render(request, 'pages/project/task/translation/edit.html', {'content': content, 'requirement': requirement, 'task_id':task_id})

def labeling_translate(request):
    if (request.method=='POST'):
        requirement_value = request.POST.get('labeling-requirement')
        content_value = request.POST.get('labeling-content')
        label_value = request.POST.get('editor-textarea')
        task_value = request.POST.get('labeling-translate-taskid')
        task_individual = TaskIndividual.objects.filter(user=request.user.username,task=task_value).first()
        if (task_individual is None):
            task_individual = TaskIndividual(user=request.user.username,task=task_value,labeling=[])
        label = {"Dataset":content_value, "Requirement":requirement_value, "Label":label_value}
        task_individual.labeling.append(label)
        task_individual.revise = False
        task_individual.done = True
        task_individual.time = datetime.now()
        task_individual.save()
        return JsonResponse({"message":"Gán nhãn dịch thành công."})
        
        





