## General Purpose Low Level Redis Interface
class Data:
  import redis
  import cPickle as pickle


  ## Settings
  host = '127.0.0.1'
  port = 6379
  channel = 0
  coalesce = False
  namespace = 'default'


  ## Constructor
  def __init__(self):
    self.r = self.redis.StrictRedis(host=self.host, port=self.port, db=self.channel)


  ## Key/Val
  def set(self,key,value,expire=False):
    payload = self.pickle.dumps(value)
    self.r.set('%s::%s'%(self.namespace,key),payload)
    if expire:
      self.r.expire('%s::%s'%(self.namespace,key),expire)
  def get(self,key):
    payload = self.r.get('%s::%s'%(self.namespace,key))
    try:
      return(self.pickle.loads(payload))
    except:
      return(None)
  def list(self,term='*'):
    clean = []
    for i in self.r.keys('%s::%s'%(self.namespace,term)):
      clean.append(i.split('%s::'%(self.namespace))[-1])
    return(clean)


  ## Queues
  def push(self,queue,data):
    payload = self.pickle.dumps(data)
    if self.coalesce:
      self.r.sadd('%s::%s'%(self.namespace,queue),payload)
    else:
      self.r.lpush('%s::%s'%(self.namespace,queue),payload)
  def pop(self,queue):
    if self.coalesce:
      payload = self.r.spop('%s::%s'%(self.namespace,queue))
    else:
      payload = self.r.rpop('%s::%s'%(self.namespace,queue))
    try:
      return(self.pickle.loads(payload))
    except:
      return(None)






## Scatter/gather class
class ScatterGather:
  '''
   /--scatter>>>>block---\
client                handler
   \--gather<<<callback--/ 
  '''
  import time
  import uuid
  import redis
  import socket
  from multiprocessing import Process
  poll = 1
  r = None
  id = None
  keepalive = 30
  namespace = 'default'
  name = None
  verbose = True
  def warmup(self):
    self.id = str(self.uuid.uuid1())
    self.data = Data()
    self.data.namespace = self.namespace
  def test(self):
    k = self.uuid.uuid4()
    v = self.uuid.uuid4()
    self.data.set(k,v,5)
    if self.data.get(k) == v:
      return(True)
    else:
      return(False)
  def scatter(self,name,message,user=False):
    payload = {'message':message,'user':user}
    self.data.push('%s::scatter'%(name),payload)
  def gather(self,name):
    message = None
    while message == None:
      message = self.data.pop('%s::callback'%(name))
      self.time.sleep(self.poll)
    return(message)    
  def block(self):
    payload = None
    while payload == None:
      if not self.test():
        print('Cannot communicate with data backend!')
      payload = self.data.pop('%s::scatter'%(self.name))
      self.time.sleep(self.poll)
    return(payload)
  def callback(self,payload):
    return(self.data.push('%s::callback'%(self.name),payload))
  def heartbeat(self):
    while True:
      payload = {}
      payload['id'] = self.id
      payload['name'] = self.name
      payload['host'] = self.socket.gethostname()
      self.data.set('instance::%s'%(self.id),payload,self.keepalive)
      self.time.sleep(self.poll)
  def listRelays(self):
    instances = []
    for i in self.data.list('instance::*'):
      instances.append(self.data.get('%s'%(i)))
    return(instances)
  def run(self,handler):
    self.warmup()
    heartbeat = self.Process(target=self.heartbeat)
    heartbeat.start()
    while True:
      payload = self.block()
      answer = handler(payload)
      self.callback(answer)


