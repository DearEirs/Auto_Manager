from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from methods import clone_project,change_project_dir
from saltapi import SaltAPI
import json

def Add_Deploy(request):
    print request.POST
    if request.method == 'POST':
        target_webroot = request.POST['target_webroot']
        project_name = request.POST['project_name']
        code_env = request.POST['code_env']
        project_env = request.POST['project_env']
        deploy_dir = request.POST['deploy_dir']
        project_language = request.POST['project_language']
        target_server = request.POST['target_server']
        project_dir = request.POST['project_dir']
        target_releases = request.POST['target_releases']
        '''
        project_dir = request.POST['project_dir']
        clone_project(project_dir)
        '''
        return render(request, 'html/add_deploy.html')
    return render(request, 'html/add_deploy.html')

def Deploy(request):
    print request.POST
    if request.method == 'POST':
        '''
        project_dir = request.POST['project_dir']
        dir_name = project_dir.split('/')[-1]
        if clone_project(project_dir):
            change_project_dir(dir_name)
        '''
        return  render(request, 'html/deploy.html')
    return render(request, 'html/deploy.html')

def Add_Host(request):
    note_name = request.POST['note_name']
    print note_name
    salt_api = SaltAPI()
    result = salt_api.Accept_Key(note_name)
    if result:
        result = 'success'
    else:
        result = 'fail'
    return HttpResponse(json.dumps(result))

def Delete_Host(request):
    note_name = request.POST['note_name']
    salt_api = SaltAPI()
    result = salt_api.Delete_Key(note_name)
    if result:
        result = 'success'
    else:
        result = 'fail'
    return HttpResponse(json.dumps(result))


def List_Host(request):
    salt_api = SaltAPI()
    minions, minions_pre = salt_api.List_All_Key()
    host_list = minions+minions_pre
    ip = salt_api.Remote_Server_Info('*','cmd.run',"ifconfig  | grep 'inet addr:' |grep -v 127.0.0.1|cut -d'B' -f 1|cut -d':' -f 2")['return'][0].values()
    os = salt_api.Remote_Server_Info('*','cmd.run','cat /etc/issue')['return'][0].values()
    is_alive = salt_api.Is_Salt_Alive('*').values()
    data=zip(host_list,ip,os,is_alive)
    return  render(request,'html/list_host.html',{'data':data})

def Remote_Execution(request,):
    print request.POST
    if request.method == "POST":
        print request.POST
        tgt = request.POST['tgt']
        fun = request.POST['fun']
        arg = request.POST['args']
        salt_api = SaltAPI()
        result = salt_api.Remote_Server_Info(tgt,fun,arg)
        result = result['return'][0]
        print result
        return HttpResponse(json.dumps(result))
    return render(request,'html/remote_exe.html')

def test(request):
    return render(request, 'html/base.html')
