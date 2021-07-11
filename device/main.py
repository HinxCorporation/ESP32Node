
from tool import *
import socket

welcome_html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> 
        <h1>ESP32</h1>
    </body>
</html>
"""

info = """
{"Node":"TestNode1"}
"""


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
    if request["path"] == "/":
      response = welcome_html
    elif request["path"] == "/info":
      response = info
    elif request["path"] == "/getPin":
      index = request["params"]["index"]
      response = '{"status":'+str(getPin(int(index)))+'}'
    elif request["path"] == "/setPin":
      index = request["params"]["index"]
      value = request["params"]["value"]
      setPin(int(index), int(value))
      response = '{"status":'+str(getPin(int(index)))+'}'
    elif request["path"] == "/getPins":
      response = "{"
      pins = getPins()
      rows = ['"%s":%d' % (str(p), p.value()) for p in pins]
      for row in rows:
        response = response + row + ','
      response = response[:-1]
      response = response + '}'
      print(response)
    else:
      response = welcome_html
    cl.send(response)
    cl.close()


