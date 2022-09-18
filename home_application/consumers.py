import asyncio
from email import message
from channels.generic.websocket import AsyncConsumer,SyncConsumer
import json
from channels.exceptions import StopConsumer
from django.dispatch import receiver
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async # it is used to run the code in async mode
from .models import *

# authentication in channels
'''
// user_obj=self.scope['user']
now check user is authenticated or not
// if self.scope['user'].is_authenticated:
// username=self.scope['user'].username
'''
'''
we have to write our orm query in seperate function and then call it in our consumer
when we use async_to_sync
*** we can use it as decorator too
@database_sync_to_async
'''
'''
json.dumps : dictionary to json string
json.loads : json string to dictionary
===================================
javascript
================
JSON.Stringify : Dict to json string
JSON.parse : json string to dict
'''

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print(self.channel_layer)
        print(self.channel_name)
        '''
        for each browser tab we are getting a new channel name.
        Now we hav eto add the channels inside a group.
        they are by default syncronu.
        it need to be syncronu for the SyncConsumer.
        self.channel_layer.group_add('groupname',self.channel_name)
        '''
        async_to_sync(self.channel_layer.group_add)
        (self.group_name,# group name
        self.channel_name)

        self.send({
            "type":"websocket.accept",
        })

    def websocket_receive(self,event):
        print(event)
        text_data=event['text']
        
        for i in range(50):
            self.send({
                "type":"websocket.send",
                "text":str(i)
            })
            sleep(1)
    def websocket_disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):


        '''
        like request in views we have scops in channels
        '''
        # print(self.scope)
        self.group_name=self.scope['url_route']['kwargs']['group_name']
        '''
        for each browser tab we are getting a new channel name.
        Now we hav eto add the channels inside a group.
        they are by default syncronus
        self.channel_layer.group_add('groupname',self.channel_name)
        '''
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.send({
            "type":"websocket.accept",
        })

    async def websocket_receive(self,event):
        print(event)
        text_data=event['text']
        text_data=json.loads(text_data)
        message=(text_data['message'])
        #print(message)
        username=self.scope['user'].username
        #sending_user=''
        # finding the group object  
        group_obj= await database_sync_to_async (Group.objects.get)(name=self.group_name)
        '''
        another way is like below in message save
        '''
        if message:
            await Chat_save_to_database(group_obj,message)

        self.send_user=text_data['send_user']

        await self.channel_layer.group_send(
            self.group_name,
            {
            'type':'chatsms_send',
            'text':message,
            'send_user':self.send_user
            }
        )

    '''
    async def will not be used
    because @database_sync_to_async is applicable for only syncronus code
    '''


    async def chatsms_send(self,event):
        print('*****')
        print(event)
        username=self.scope['user'].username
        payload={'username':event['send_user'],'message':event['text']}
        payload=json.dumps(payload)
        await self.send({
            'type':'websocket.send',
            'text':payload
        })


    async def websocket_disconnect(self, close_code):
        self.channel_layer.group_discard(self.group_name,self.channel_name)
        raise StopConsumer()

@database_sync_to_async
def Chat_save_to_database(group_obj,message):
    chat=Chat.objects.create(group=group_obj,content=message)
   
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_group_name = 'Test-Room'
#         self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         print('accepted')
#         await self.accept()
#     async def disconnect(self,close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#         print('disconnected')

        
#     async def receive(self, text_data):
#         receive_dict = json.loads(text_data)
#         message = receive_dict['message']
        
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'send.message',
#                 'message': message
#             }
#         )
#         await self.send(text_data=json.dumps({
#             "type": "websocket.send",
#             'message':message
#         }))