#!coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Auto_deploy(models.Model):
    project_env_choices = (
        (u'dev_env', u'灰度发布'),
        (u'pro_env', u'正式发布'),
    )
    project_language = (
        (u'php', u'php'),
        (u'java', u'java'),
    )
    code_env_choices = (
        (u'git', u'git'),
        (u'svn', u'svn'),
    )
    project_name = models.CharField(max_length=256,verbose_name=u'项目名称')
    project_env =  models.CharField(max_length=256,choices=project_env_choices,verbose_name=u'项目环境')
    project_language = models.CharField(max_length=256,choices=project_language,verbose_name=u'项目语言')
    project_dir = models.CharField(max_length=256, verbose_name=u'项目地址')
    code_env = models.CharField(max_length=256,choices=code_env_choices,verbose_name=u'代码环境')
    deploy_dir = models.CharField(max_length=256,verbose_name=u'发布器存放代码目录')
    target_webroot = models.CharField(max_length=256,verbose_name=u'目标主机web根目录')
    target_server = models.CharField(max_length=256,verbose_name=u'目标主机地址')
    target_releases = models.CharField(max_length=256,verbose_name=u'目标主机版本库目录')
    publish_state = models.IntegerField(default=0,verbose_name=u'发布状态')
    publish_time = models.DateField(max_length=256,auto_now_add=True,verbose_name=u'发布时间')

