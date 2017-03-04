from django.shortcuts import render,redirect

# Create your views here.
from methods import clone_project,change_project_dir


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