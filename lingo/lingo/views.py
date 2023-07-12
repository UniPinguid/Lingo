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
from django.utils import timezone
from django.db.models import Max
import json
from random import *
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
    temp = Project.objects.filter(id_project = int(project_id)).first()
    return render(request, 'pages/project/main.html', {'project': temp})

def members(request):
    return render(request, 'pages/project/members.html')

def tasks(request):
    projectid = request.session.get('projectid')
    tasks = Task.objects.filter(project_id = projectid)

    return render(request, 'pages/project/tasks.html', {'project_id': projectid, 'tasks':tasks})

def labels(request):
    projectid = request.session.get('projectid')
    labels = Label.objects.filter(project_id=projectid)
    return render(request, 'pages/project/labels.html', {"project_id": projectid,
                                                         "labels": labels})

def contribution(request):
    return render(request, 'pages/project/contribution.html')

# Tasks screen
def task_detail(request,taskid):
    request.session['taskid'] = int(taskid)
    task = Task.objects.get(taskid=taskid)
    datasets = task.datasets

    request.session['cate'] = task.category
    return render(request, 'pages/project/task/detail.html', {'project_id': request.session.get('projectid')
                                                              , 'cate': task.category, 'datasets': datasets,'task_id':taskid})

def dataset_classification(request, taskid):
    return render(request, 'pages/project/task/classification/dataset.html',
                  {"project_id": request.session.get("projectid"),
                   "taskid": taskid})

def dataset_classification_edit(request):
    return render(request, 'pages/project/task/classification/edit.html')

def dataset_equivalency(request, datasetid):
    request.session['datasetid'] = int(datasetid)
    dataset_id = int(datasetid)
    t = Task.objects.get(taskid=request.session.get('taskid'))
    datasets = t.datasets
    for dataset in datasets:
        if (dataset['datasetid'] == dataset_id):
            return render(request, 'pages/project/task/equivalency/dataset.html', {'dataset': dataset, 'project_id': request.session.get('projectid')
                                                                                   , 'taskid':request.session.get('taskid')})
        

    return JsonResponse({"message": "nothing"})
    

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
        return JsonResponse({"Message": "Gán nhãn thành công."})

    elif(request.method == 'GET'):
        task_id = request.session.get('taskid')
        dataset_id = int(datasetid)
        task = Task.objects.get(taskid=task_id)
        datasets = task.datasets
        dataset1 = "System Error"
        dataset2 = "System Error"
        for dataset in datasets:
            if (dataset['datasetid'] == dataset_id):
                dataset1 = dataset['content']
                dataset2 = dataset['content1']
                return render(request, 'pages/project/task/equivalency/edit.html'
                      , {"dataset_id": dataset_id, "task_id": task_id, "dataset1": dataset1,
                         "dataset2": dataset2, "project_id": request.session.get('projectid'),
                         "cate": request.session.get('cate')})
        

# def dataset_qa(request):
#     return render(request, 'pages/project/task/qa/dataset.html')

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
        # Đọc nội dung của file
        file_content = file.read().decode('utf-8').splitlines()

        # Xử lý nội dung file
        if len(file_content) >= 2:
            file_type = file_content[0]  # Loại file
            #dataset = file_content[1]  # Dữ liệu dataset

            # Tạo dictionary để lưu trữ thông tin dataset
            dataset_info = {
                "file_type": file_type,
                #"dataset": dataset
            }

            # Xử lý nội dung file cho từng loại file
            if file_type == "Text Classification" or file_type == "Entity" or file_type == "Equivalency_Question":
                # Cập nhật dataset cho loại file Text Classification, Entity, Equivalency_Question
                #dataset_info["requirement"] = ""
                if len(file_content) >= 3:
                    dataset_info["requirement"] = file_content[1]
                    dataset_info["content"] = file_content[2]
                else:
                    dataset_info["content"] = file_content[1]

            elif file_type == "Translation":
                # Cập nhật dataset cho loại file Translation
                dataset_info["requirement"] = ""
                dataset_info["content"] = ""
                if len(file_content) >= 3:
                    dataset_info["requirement"] = file_content[1]
                if len(file_content) >= 4:
                    dataset_info["content"] = file_content[2]

            elif file_type == "QA_Label" or file_type == "Equivalency":
                # Cập nhật dataset cho loại file QA_Label, Equivalency
                dataset_info["content"] = ""
                dataset_info["content1"] = ""
                if len(file_content) >= 3:
                    dataset_info["content"] = file_content[1]
                if len(file_content) >= 4:
                    dataset_info["content1"] = file_content[2]


        project_id = request.session.get('projectid')
        project1 = Project.objects.filter(id_project = project_id).first()
        if (project1.datasets is None):
            project1.datasets = []
        project1.datasets.append(dataset_info)
        # project1.save()
        Project.objects.filter(id_project=project_id).update(datasets=project1.datasets) 
        return JsonResponse({"Message": "Success"})

        

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
        max_projectid = Project.objects.aggregate(Max('id_project'))['id_project__max']
        if (max_projectid is None):
            project_id = 1
        else:
            project_id = max_projectid + 1

        
        #project_id = randint(1000,5000)
        obj = Project(projectname=project_name_value,tags=tags_value,
                      description=description_value,visibility=visibility_value,
                       id_project= project_id, member=member_value)
        res = obj.insertProject()
        if (res == 1):
            return JsonResponse({"message": "Tạo project thành công."})
        else:
            return JsonResponse({"message": "Tạo project thất bại."})
        

def create_label(request):
    if (request.method=='POST'):
        label_name_value = request.POST.get('label-name')
        description_value = request.POST.get('label-description')
        color_value = request.POST.get('label-color')
        obj = Label(labelname=label_name_value,description=description_value,color=color_value
                    ,project_id=request.session.get('projectid'))
        
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
        member_value += (request.user.username)
        project_id = request.session.get('projectid')
        max_taskid = Task.objects.aggregate(Max('taskid'))['taskid__max']
        
        obj = Task(title=title_value,category=category_value,description=description_value
                   ,member=member_value,date=datetime.now().date(),project_id=project_id
                   , taskid = int(max_taskid) + 1)
        res = obj.insertTask()
        if(res == 1):
            return JsonResponse({"message":"Tạo task thành công."})
        else:
            return JsonResponse({"message":"Tạo task thất bại."})
        
def dataset_qa(request, datasetid):
    if (request.method == "GET"):
        try:
            task = Task.objects.filter(id=request.session.get('taskid')).first()
            datasets = task.datasets
            for dataset in datasets:
                if (dataset['datasetid'] == int(datasetid)):
                    return render(request, 'pages/project/task/qa/dataset.html', {'dataset': dataset})
        except NameError:
            task = None 
        
    elif(request.method == "POST"):
        return 0


def display_dataset(request, task_id, dataset_id):
    task_id = int(task_id)
    dataset_id = int(dataset_id)
    task = Task.objects.filter(taskid=task_id).first()
    datasets = task.datasets
    for dataset in datasets:
        if (dataset['datasetid']==dataset_id):
            content = dataset['content']
            requirement = dataset['requirement']
            

    return render(request, 'pages/project/task/translation/edit.html', {'content': content, 'requirement': requirement, 'task_id':task_id,'project_id':request.session['projectid']})

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
        
def get_datasets(request):
    category = request.GET.get('category')
    datasets = Dataset.objects.filter(category=category).values('datasetid', 'content')
    return JsonResponse(list(datasets), safe=False)

        





