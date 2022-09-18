from tokenize import group
from django.db import models
from django.contrib import admin

# Create your models here.
class Chat(models.Model):
    content = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True)
    group=models.ForeignKey('Group',on_delete=models.CASCADE)

@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ('content','timestamp','group')

class Group(models.Model):
    name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ('name','timestamp')