import urllib2,urllib
import json
from django.conf import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salt.settings")
import django
django.setup()


class SaltAPI(object):

    _token_id = ''
    def __init__(self):
        self.url = settings.SALT_API_URL
        self.username = settings.SALT_API_AUTH_USER
        self.password = settings.SALT_API_AUTH_PASS

    def Get_Token(self):
        params = {"eauth": "pam", "username": self.username, "password": self.password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode )
        req = self.Post_Request(obj, prefix='/login')
        self._token_id = req['return'][0]['token']

    def Post_Request(self,key_encode,prefix='/'):
        url = self.url + prefix
        headers = {}
        req = urllib2.Request(url,key_encode,headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    def Accept_Key(self,note_name):
        params = {'client':'wheel','fun':'key.accept','match':note_name}
        obj = urllib.urlencode(params)
        self.Get_Token()
        content = self.Post_Request(obj)
        ret = content['return'][0]['success']
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
        self.Get_Token()
        content = self.Post_Request(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions.minions_pre

    def Remote_Exe(self,tgt,fun,arg,expr_form):
        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        obj = urllib.urlencode(params)
        self.Get_Token()
        content = self.Post_Request(obj)
        jid = content['return'][0]['jid']
        return jid

    def file_copy(self, tgt, fun, arg1, arg2, expr_form):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        params2 = {'arg': arg2}
        arg_add = urllib.urlencode(params2)
        obj = urllib.urlencode(params)
        obj = obj + '&' + arg_add
        self.Get_Token()
        content = self.Post_Request(obj)
        ret = content['return'][0]
        return ret

    def remote_server_info(self, tgt, fun):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.urlencode(params)
        self.Get_Token()
        content = self.Post_Request(obj)
        ret = content['return'][0][tgt]
        return ret