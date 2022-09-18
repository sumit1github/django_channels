from multiprocessing import context
from django.shortcuts import render
from .models import *
import secrets
# Create your views here.
def unique_group_check(group_name):
    if (Group.objects.filter(name=group_name).exists())==True:
        return True
    else:
        return False
def index(request,group_name):
    user_name=request.user.username
    #saving the group name 
    chats=[]
    if (Group.objects.filter(name=group_name).exists())==False:
        group=Group.objects.create(name=group_name)
    else:
        group=Group.objects.get(name=group_name)
    chats=Chat.objects.filter(group=group)
    context={'username':user_name,'group_name':group_name,'chats':chats}
    return render(request, 'index2.html',context)

