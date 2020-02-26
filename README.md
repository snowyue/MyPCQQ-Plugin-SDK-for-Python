# # python-mypcqq


闲来无事，想写个爬虫，然后写崩了 还是写个机器人的python插件算了，当个人学习python的总结


# # 需求
# 1.python需求
from wsgiref.simple_server import make_server

from urllib import parse

import json,base64,requests

# 2.mypcqq框架需求
须打开转发接口，并设置set.ini

[tran]
enable=1															//开关
target=https://www.baidu.com					//转发目标，确保可信
whitelist=0.0.0.0 127.0.0.1						//IP白名单，添加后才能请求接口，以空格或逗号分割

文档：https://www.yuque.com/mpq/docs/transpond

# # API接口

暂时只编写发送测试接口，因原理过于简单，其他未编写
