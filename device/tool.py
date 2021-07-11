
import machine

def getRequestInfo(line):
    """
    将Request第一行信息拆分【NC】
    :param line:
    :return:
    """
    result = {}
    # 将字节转码转为str
    line = str(line)
    if line == "b''":
      return result
    # 替换无用字符
    info = line.replace("\\r\\n", "")
    info = info.replace("b'", "")
    # 使用空格对请求信息分段
    info = info.split(" ")
    result["method"] = info[0]
    result["protocol"] = info[2]
    result["params"] = {}
    # 使用?对路径及参数分段
    pathAndParams = info[1].split("?")
    result["path"] = pathAndParams[0]
    # 使用&对参数进行分段并建立字典
    if len(pathAndParams) > 1:
        params = pathAndParams[1].split("&")
        for param in params:
            terms = param.split("=")
            result["params"][terms[0]] = terms[1]
    return result

    
def getPin(index):
  """
  获取指定引脚的状态【NC】
  :index:获取状态的引脚标号
  :return:
  """
  pin = machine.Pin(index)

  return pin.value() 

 

def setPin(index, value):

  """

  设置指定引脚的状态【NC】

  :index:获取状态的引脚标号

  :value:[0: off, 1: on]

  :return:

  """

  print(index)

  print(value)

  pin = machine.Pin(index, machine.Pin.IN, machine.Pin.PULL_UP)
  pin.value(value) 
 
def getPins():
  """
  获取各个引脚的状态【NC】
  :return:
  """
  return [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33, 34, 35, 36, 39)]

def getConfig(key):
  """
  获取配置文件中指定key的信息【NC】
  :param key:
  :return:
  """
  config = open('config.txt', 'r')
  data = config.read()
  for line in data.split('\r'):
    if line == "":
        continue
    item = line.split("::")
    if item[0] == key:
        config.close()
        return item[1]
  config.close()
  return None


def setConfig(key, value):
  """
  设置一个key::value到配置文件【NC】
  :param key:
  :param value:
  :return:
  """
  config = open('config.txt', 'r+')
  data = config.read()
  configItem = {}
  change = False
  for line in data.split('\r'):
    if line == "":
        continue
    item = line.split("::")
    if item[0] == key:
        item[1] = value
        change = True
    configItem[item[0]] = item[1]
  if not change:
      configItem[key] = value
  config.close()
  config = open('config.txt', 'w')
  for key in configItem:
      config.write(str(key)+"::"+str(configItem[key])+"\r")
  config.close()
