import urllib2,urllib
import json
from django.conf import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Auto_Deploy.settings")
import django
django.setup()
import ssl


class SaltAPI(object):

    __token_id = ''
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.__url = settings.SALT_API_URL
        self.__url = self.__url.rstrip('/')
        self.__username = settings.SALT_API_AUTH_USER
        self.__password = settings.SALT_API_AUTH_PASS

    def Get_Token(self):
        params = {"eauth": "pam", "username": self.__username, "password": self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        content = self.Post_Request(obj, prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError

    def Post_Request(self,obj,prefix='/'):
        url = self.__url + prefix
        self.__token_id = self.__token_id.decode('utf-8')
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib2.Request(url,obj,headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    def Accept_Key(self,note_name):
        params = {'client':'wheel','fun':'key.accept','match':note_name}
        obj = urllib.urlencode(params)
        self.Get_Token()
        content = self.Post_Request(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def Delete_Key(self,note_name):
        params = {'client':'wheel','fun':'key.delete','match':note_name}
        obj = urllib.urlencode(params)
        self.Get_Token()
        content = self.Post_Request(obj)
        ret = content['return'][0]['data']['success']
        return  ret

    def List_All_Key(self):
        params = {'client':'wheel','fun':'key.list_all'}
        obj = urllib.urlencode(params)
        obj = urllib.unquote(obj)
        self.Get_Token()
        content = self.Post_Request(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions,minions_pre

    def Remote_Exe(self,tgt,fun,arg,expr_form):
        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        obj = urllib.urlencode(params)
        self.Get_Token()
        content = self.Post_Request(obj)
        jid = content['return'][0]['jid']
        return jid

    def File_Copy(self, tgt, fun, arg1, arg2, expr_form):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        params2 = {'arg': arg2}
        arg_add = urllib.urlencode(params2)
        obj = urllib.urlencode(params)
        obj = obj + '&' + arg_add
        self.Get_Token()
        content = self.Post_Request(obj)
        ret = content['return'][0]
        return ret

    def Remote_Server_Info(self,tgt,fun,arg=None):
        if not arg:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun,'arg':arg}
        obj = urllib.urlencode(params)
        self.Get_Token()
        content = self.Post_Request(obj)
        ret = content
        return ret

    def Is_Salt_Alive(self,tgt):
        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping'}
        obj = urllib.urlencode(params)
        self.Get_Token()
        content = self.Post_Request(obj)
        ret = content['return'][0]
        return ret
'''
a = SaltAPI().remote_server_info('*','status.all_status')
b = SaltAPI().remote_server_info('*','cmd.run','cat /etc/issue')
c = SaltAPI().remote_server_info('*','cmd.run','cat /etc/issue')
print a['return'][0]['minion']['meminfo']['MemTotal']
print b['return'][0]['minion'].split('\n')[0]
print c['return'][0]['minion'].split('\n')[0]
d = SaltAPI().is_salt_alive('*')
print d
e = SaltAPI().Accept_Key('minion1')
print e

a = SaltAPI().remote_server_info('*','status.all_status')
print a['return'][0]['minion']['meminfo']['MemTotal']
print a['return'][0]['minion']['cpuinfo']['cpu cores']
for i in  a['return'][0]['minion']:
    print i
'''

#print SaltAPI().remote_server_info('*','cmd.run',"ifconfig  | grep 'inet addr:' |grep -v 127.0.0.1|cut -d'B' -f 1|cut -d':' -f 2")
