#!coding:utf-8


def clone_project(dir):
    try:
        from os import system
        command = 'git clone {0}'.format(dir)
        system(command)
        return 1
    except:
        return 0

def change_project_dir(dir_name,dir=None):
    from os import system
    if not dir:
        dir = "D:\\"
    print dir,dir_name
    command = 'move {0} {1}'.format(".\\"+dir_name,dir)
    system(command)
