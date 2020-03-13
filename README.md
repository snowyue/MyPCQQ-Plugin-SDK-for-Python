写个机器人的python版本插件，当作个人学习python的总结
（技术含量不高，请各位多多包涵。。。）
# 需求

1.python需求

python3.x+任意ide(不用也可以)
```
注意：run.py需要：wsgiref，urllib，json，base64，requests，
注意：uvicorn.py需要：uvicorn，urllib，json，base64，requests，
```
2.mypcqq框架需求
须打开转发接口，并设置set.ini
```
[tran]
enable=1				    			//开关
target=127.0.0.1:900					//转发目标，确保可信
whitelist=0.0.0.0 127.0.0.1				//IP白名单，添加后才能请求接口，以空格或逗号分割
```
# 运行
```
直接运行run.py或uvicorn.py，MPQ打开“使用转发接口”即可
```
#  文档与MPQ
```
MPQ下载 : http://t.cn/ROII2jI
文档目录：https://www.yuque.com/mpq/docs/transpond
```
# 更新记录
```
v1.02
添加获取名片和昵称api
v1.01
添加好友，
更换web框架为uvicorn，原始版本继续作为参考使用
v1.00
暂时只编写发送测试接口，其他未编写
```
# 演示
![image](https://github.com/snowyue/python-mypcqq/blob/master/image/调试截图_1.0.1.png?raw=true)
![image](https://github.com/snowyue/python-mypcqq/blob/master/image/框架测试截图_1.0.1.png?raw=true)
![image](https://github.com/snowyue/python-mypcqq/blob/master/image/群测试截图_1.0.1.png?raw=true)
