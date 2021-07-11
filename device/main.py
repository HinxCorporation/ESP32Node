

from tool import *
import socket
import json

welcome_html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> 
        <h1>ESP32</h1>
    </body>
</html>
"""

info = {
  "NodeName":"TestNode",
  "function":{
    "/":"welcome page",
    "/info":"get node info",
    "/getPin":"get specified pin state",
    "/setPin":"Set one pin as the output pin and set its state",
    "/getPins":"get all pin state",
    "/restart":"restart node",
  }
}

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    # 只获取request请求的第一行信息用于请求判断
    line = cl_file.readline()
    # 通过request第一行获取请求路径与参数
    request = getRequestInfo(line)
    # 后面的信息直接读取完，不使用
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
          break
    # 根据path参数进入不同的流程
    print(request);
    # =================================
    # 访问欢迎界面
    # =================================
    if request["path"] == "/":
      response = welcome_html
    # =================================
    # 获取节点信息
    # =================================
    elif request["path"] == "/info":
      response = json.dumps(info)
    # =================================
    # 获取指定引脚状态
    # =================================
    elif request["path"] == "/getPin":
      index = request["params"]["index"]
      response = '{"status":'+str(getPin(int(index)))+'}'
    # =================================
    # 设置指定引脚状态
    # =================================
    elif request["path"] == "/setPin":
      index = request["params"]["index"]
      value = request["params"]["value"]
      setPin(int(index), int(value))
      response = '{"status":'+str(getPin(int(index)))+'}'
    # =================================
    # 获取所有引脚状态
    # =================================
    elif request["path"] == "/getPins":
      pins = getPins()
      rows = {}
      for p in pins:
        rows[str(p)] = p.value()
      response = json.dumps(rows)
    # =================================
    # 其它访问情况均按照欢迎界面处理
    # =================================
    else:
      response = welcome_html
    cl.send(response)
    cl.close()



