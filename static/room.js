const groupname=document.getElementById("group_name").value;
console.log(groupname);
const msg_send_button = document.getElementById("msg_send_button");
var username=document.getElementById("username").value;
var ws=new WebSocket(
  'ws://'
  +window.location.host
  +'/ws/ac/'+groupname
  +'/'
);

msg_send_button.addEventListener("click",sendsms);
function sendsms(){
  sms=document.getElementById("type_sms").value;
  var jsonStr=JSON.stringify({
    'message':sms, 
    'send_user':username,
  })
  ws.send(jsonStr);
  sms=document.getElementById("type_sms").value='';
}

ws.onopen = function(){
  console.log('connected');
} 


ws.onmessage = function(e){
  var parseData=JSON.parse(e.data);
  //user=parseData['user'];
  message=parseData['message'];
  user=parseData['username'];
  console.log(user);
  html='<div class="message-wrapper">\
  <div class="message-content">\
      <p class="name">'+ user +'</p>\
      <div class="message">'+ message + '</div></div></div>'
       
  var element=document.createElement("span");
  element.innerHTML=html;
  document.getElementById('chat-area').appendChild(element);
}


ws.onerror = function(e){
  console.log("error received");
}

ws.onclose = function(e){
  console.log("connection closed");
}


