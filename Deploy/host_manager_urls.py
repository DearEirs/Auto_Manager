"""Auto_Deploy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from Deploy.views import List_Host,Add_Host,Delete_Host


urlpatterns = [
    url(r'^$',List_Host,name='List_Host'),
    url(r'Add/?P<note_name>.*?/$',Add_Host, name='Add_Host'),
    url(r'Delete/(?P<name>.*?)$', Delete_Host, name='Delete_Host'),
]
