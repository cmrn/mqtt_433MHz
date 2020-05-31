import paho.mqtt.client as mqtt
from topic import Topic

BASE_TOPIC = Topic("433MHz")

from blind import Blind
from fountain import Fountain
from message_logger import MessageLogger
listeners = [Blind('inner'), Blind('outer'), Fountain(), MessageLogger()]

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(str(BASE_TOPIC + "#"))

class MQTT433MHz(object):
  def __init__(self, *argv):
    self.client = mqtt.Client(*argv)
    self.client.on_connect = on_connect
    for listener in listeners:
      listener.attach(self.client, BASE_TOPIC)
