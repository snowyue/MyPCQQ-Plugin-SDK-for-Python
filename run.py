from wsgiref.simple_server import make_server
from urllib import parse
import json,base64,requests
def index(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))#获取聊天信息
    html=str(request_body,'utf-8') #将以字节为单位的bytes转化为python unicode编码
    json_content=json.loads(html) #字典格式化
    '''{
    "Port":"8010",                    //监听的服务端口，范围为 8010-8020
    "Pid":"14880",                    //进程ID
    "Ver":"MyPCQQ Ver20170721",       //框架版本
    "MsgID":"40",                     //信息序号
    "Robot":"3509945636",             //机器人QQ
    "MsgType":"1",                    //信息类型
    "MsgSubType":"0",                 //信息子类型，默认 0
    "Source":"445491251",             //信息来源
    "Sender":"445491251",             //主动触发对象
    "Receiver":"3509945636",          //被动接收对象
    "Content":"5ZWq5ZWq5ZWq",         //正文内容，需要 base64解码
    "OrigMsg":""                      //原始数据，需要 base64解码
｝'''
    Port = json_content['Port']
    MsgType = json_content['MsgType']
    Source = json_content['Source']
    if(MsgType == "1"):
        content = base64.b64decode(json_content['Content']).decode()
        #print('Robot：', json_content['Robot'])  # 调试输出 机器人QQ号码
        print("来自好友的消息：",content)  # 调试输出 解码后的信息正文
    elif(MsgType == "2" and Source == "561024983"):
        content = base64.b64decode(json_content['Content']).decode()
        #print('Robot：', json_content['Robot'])  # 调试输出 机器人QQ号码
        print('来自群友的消息：',content)  # 调试输出 解码后的信息正文
        if(content == "测试"):
            sendmsg(json_content['Robot'],json_content['Source'],json_content['Sender'],"测试信息")
    return [b'<h1>How Are!</h1>']
def sendmsg(Robotqq,Source,Sender,text):
    get_text = "/?QQ=" + Robotqq + "&API="
    api_text = parse.quote("Api_SendMsg({},2,0,{},{},{})".format("'" + Robotqq + "'",
                                                                 "'" + Source + "'",
                                                                 "'" + Sender + "'",
                                                                 "'"+text+"'"))
    tt = requests.get("http://127.0.0.1:8010" + get_text + api_text)
    json_content = json.loads(tt.text)  # 字典格式化
    code = json_content["Code"]
    if(code == "0"):
        return True
    elif (code == "-1"):
        print("调度过程中发生了读写异常")
        return False
    elif (code == "-2"):
        print("找不到响应的机器人QQ")
        return False
    elif (code == "-3"):
        print("POST的API参数为空或解析失败")
        return False
    elif (code == "-4"):
        print("API不存在")
        return False
    elif (code == "-5"):
        print("API参数格式错误")
        return False
    elif (code == "-6"):
        print("API最多支持15个参数")
        return False
    else:
        print("unknow err")
        return False

port=900
httpd = make_server('', port, index)
httpd.serve_forever()
