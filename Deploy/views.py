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

def Add_Host(request):
    salt_api = SaltAPI()
    minions, minions_pre = salt_api.List_All_Key()
    return  render(request,'html/list_host.html',{'minions':minions,'minions_pre':minions_pre})

def Delete_Host(request,name):
    salt_api = SaltAPI()
    response = salt_api.Delete_Key(name)
    return  redirect('Deploy.views.List_Host')

def List_Host(request):
    salt_api = SaltAPI()
    minions, minions_pre = salt_api.List_All_Key()
    host_list = minions+minions_pre
    ip = salt_api.remote_server_info('*','cmd.run',"ifconfig  | grep 'inet addr:' |grep -v 127.0.0.1|cut -d'B' -f 1|cut -d':' -f 2")['return'][0].values()
    os = salt_api.remote_server_info('*','cmd.run','cat /etc/issue')['return'][0].values()
    is_alive = salt_api.is_salt_alive('*').values()
    data=zip(host_list,ip,os,is_alive)
    return  render(request,'html/list_host.html',{'data':data})