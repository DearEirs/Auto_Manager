from django.shortcuts import render,redirect

# Create your views here.
from methods import clone_project,change_project_dir
from saltapi import SaltAPI

def Add_Deploy(request):
    print request.POST
    if request.method == 'POST':
        project_dir = request.POST['project_dir']
        clone_project(project_dir)
        return render(request, 'html/add_deploy.html')
    return render(request, 'html/add_deploy.html')

def Deploy(request):
    if request.method == 'POST':
        project_dir = request.POST['project_dir']
        dir_name = project_dir.split('/')[-1]
        if clone_project(project_dir):
            change_project_dir(dir_name)
        return  render(request, 'html/deploy.html')
    return render(request, 'html/deploy.html')

def Index(request):
    if request.method == 'POST':
        return  render(request, 'html/base.html')
    return  render(request,'html/base.html')

def Host_Maneger(request):
    return render(request,'html/host_manager.html')

def List_Host(request):
    salt_api = SaltAPI()
    host_list = salt_api.List_All_Key()
    return  render(request,'html/list_host.html',{'host_list':host_list})
