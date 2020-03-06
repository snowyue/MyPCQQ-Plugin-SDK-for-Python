import uvicorn
from urllib import parse
import json, base64, requests



class Pympq(object):

    def __init__(self):
        self.Ret=2
        self.Mpq_index=0
        self.Port = ""       #监听的服务端口，范围为 8010-8020
        self.Pid=""          #进程ID
        self.Ver = ""        #框架版本
        self.MsgID = ""      #信息序号
        self.Robot = ""      #机器人QQ
        self.MsgType = ""    #信息类型
        self.MsgSubType = "" #信息子类型，默认 0
        self.Source = ""     #信息来源
        self.Sender = ""     #主动触发对象
        self.Receiver = ""   #被动接收对象
        self.Content = ""    #正文内容，需要 base64解码
        self.OrigMsg = ""    #原始数据，需要 base64解码
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
    def Error(self,json_str):
        json_content = json.loads(json_str)  # 字典格式化
        code = json_content["Code"]
        #print(code,json_content["Data"])
        #print(self.Mpq_base64_decode(json_content["Data"]))
        if (code == "0"):
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
        return False
    def index(self,environ, start_response):
        start_response('200 OK', [('Content-Type', 'json/html')])
        if(environ.get("REQUEST_METHOD")=="GET"):
            return [b"<h1>It's GET</h1>"]
        elif(environ.get("REQUEST_METHOD")=="POST"):
            request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))#获取聊天信息
            html=str(request_body,'utf-8') #将以字节为单位的bytes转化为python unicode编码
            m_info = self.Mpq_main(html)
            response_body = json.dumps(m_info)
            print(1111,response_body)
        return [response_body.encode("Utf-8")]
    def Mpq_main(self,environ):
        json_content = json.loads(environ)  # 字典格式化
        #print(json_content)
        if (self.Mpq_index == 0):
            self.Port = json_content['Port']            # 监听的服务端口，范围为 8010-8020
            self.Pid = json_content['Pid']              # 进程ID
            self.Ver = json_content['Ver']              # 框架版本
            self.MsgID = json_content['MsgID']          # 信息序号
            self.Robot = json_content['Robot']          # 机器人QQ
            self.MsgType = json_content['MsgType']      # 信息类型
            self.MsgSubType = json_content['MsgSubType']# 信息子类型，默认 0
            self.Source = json_content['Source']        # 信息来源
            self.Sender = json_content['Sender']        # 主动触发对象
            self.Receiver = json_content['Receiver']    # 被动接收对象
            self.Content = self.Mpq_base64_decode(json_content['Content'])      # 正文内容，需要 base64解码
            self.OrigMsg = json_content['OrigMsg']      # 原始内容，需要 base64解码
            self.Mpq_index = 1
        else:
            self.Robot = json_content['Robot']          # 机器人QQ
            self.MsgType = json_content['MsgType']      # 信息类型
            self.Source = json_content['Source']        # 信息来源
            self.Sender = json_content['Sender']        # 主动触发对象
            self.Receiver = json_content['Receiver']    # 被动接收对象
            self.Content = self.Mpq_base64_decode(json_content['Content'])      # 正文内容，需要 base64解码
        if (self.MsgType == "1"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print("来自好友的消息：", self.Content)  # 调试输出 解码后的信息正文
            return self.Mpq_ret("0")
        elif (self.MsgType == "2" and self.Source == "583"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print("来自群友的消息：", self.Content)  # 调试输出 解码后的信息正文
            if (self.Content == "测试回复"):
                self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "测试信息666",2)
            return self.Mpq_ret("0")
        else:
            return self.Mpq_msgtype(self.MsgType)
        return self.Mpq_ret("0")
    def Mpq_base64_decode(self,str):
        return base64.b64decode(str).decode()
    def Mpq_ret(self,ret,msg=None):
        """{
            "Ret": "10", // 返回值，10 = 默认确定\同意，20 = 默认取消\拒绝
            "Msg": "" // 返回信息，用于处理拒绝加群拒绝加好友的理由回传
            }"""
        txt = {"Ret":"", "Msg":""}
        txt["Ret"] = ret
        if ret=="10":
            self.Ret = 1
        else:
            self.Ret = 2
        if (msg!=None):
            txt["Msg"] = msg
        else:
            txt["Msg"] = ""
        return json.dumps(txt)
    def Mpq_msgtype(self,Msgtype):
        if (Msgtype == "1001" ):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print("验证消息", self.Content)  # 调试输出 解码后的信息正文
            print(self.Sender, "添加好友~~")  # 调试输出
            if (self.Content == "我是机器人"):
            #    self.Mpq_Api_HandleFriendRequestAsyncA(self.Robot, self.Source, "10", "")
                return self.Mpq_ret("10")
            return self.Mpq_ret("20")
            #self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "欢迎[name]加入[gname]\\n审批者："+self.Sender)
        elif (Msgtype == "2001" and self.Source == "583"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print(self.Sender, "申请入群~~")  # 调试输出
            self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "欢迎[name]加入[gname]\\n审批者："+self.Sender)
        elif (Msgtype == "2002" and self.Source == "561024983"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print(self.Receiver,"被邀请加入群~")  # 调试输出
            self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "[name]被邀请加入某群~~")
        elif (Msgtype == "2003" and self.Source == "583"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print(" 我被",self.Sender,"邀请加入群")  # 调试输出
            self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "[name]被邀请加入某群~~")
        elif (Msgtype == "2005" and self.Source == "583"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print(self.Receiver,"被批准加入了群~")  # 调试输出
            self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "[name]被管理员批准加入~~")
        elif (Msgtype == "2006" and self.Source == "583"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print(self.Sender," 退出群~")  # 调试输出
            self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "[name]退出本群~~")
        elif (Msgtype == "2007" and self.Source == "583"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print(self.Receiver," 被管理移除群~")  # 调试输出
            self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "[name]被移除本群~~")
        elif (Msgtype == "2008" and self.Source == "583"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print(self.Sender,"某群被解散~")  # 调试输出
            self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "[gname]被解散~~")
        elif (Msgtype == "2009" and self.Source == "583"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print(self.Sender," 成为管理员~")  # 调试输出
            self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "[name]和群主达成了不可告人的交易成为了本群管理员~~")
        elif(Msgtype == "2010" and self.Source == "583"):
            print('Robot：', self.Robot)  # 调试输出 机器人QQ
            print('MsgType：', self.MsgType)  # 调试输出 信息类型
            print('Source：', self.Source)  # 调试输出 信息来源
            print("Sender：", self.Sender)  # 调试输出 主动触发对象
            print("Receiver：", self.Receiver)  # 调试输出 被动接收对象
            print(self.Sender," 取消管理员权限~")  # 调试输出
            self.Mpq_Sendmsg(self.Robot, self.Source, self.Sender, "[name]和群主交易达成失败，被取消管理员权限~")
    def Mpq_Sendmsg(self,Robotqq,Source,Sender,text,mode=2):
        api_text = parse.quote("Api_SendMsg({},2,0,{},{},{})".format("'" + Robotqq + "'",
                                                                     "'" + Source + "'",
                                                                     "'" + Sender + "'",
                                                                     "'" + text + "'"))
        if (mode ==1):
            get_text = "/?QQ=" + Robotqq + "&API="
            tt = requests.get("http://127.0.0.1:8010" + get_text + api_text)
        else:
            get_text = "QQ=" + Robotqq + "&API="
            tt = requests.post("http://127.0.0.1:8010" ,data=get_text + api_text)
            print(tt.text)
        return self.Error(tt.text)
    #def start(self):

MPQ = Pympq()

async def read_body( receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b''
    more_body = True
    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)
    json = body.decode("utf-8")
    return json

async def app(scope, receive, send):
    """
    Echo the request body back in an HTTP response.
    """
    if (scope["method"]=="POST"):
        body = await read_body(receive)
        MPQ.Mpq_main(body)
        #print(send_body)
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'json/plain'],
        ]
    })
    if MPQ.Ret == 1 :
        await send({
            'type': 'http.response.body',
            'body': b'{"Ret":"10","Msg":""}'
        })
    else:
        await send({
            'type': 'http.response.body',
            'body': b'{"Ret":"0","Msg":""}'
        })

if __name__ == "__main__":
    #MPQ = Pympq()
    #MPQ.start()
    uvicorn.run("app:app", host="127.0.0.1", port=900, log_level="info")
