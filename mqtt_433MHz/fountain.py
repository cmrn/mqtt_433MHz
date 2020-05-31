import subprocess
import os
import sys

def lib_dir():
  return os.path.join(os.path.dirname(os.path.realpath(__file__)), '../lib')


class Fountain:
  def attach(self, client, parent_topic):
    self.topic = parent_topic + "fountain"
    client.message_callback_add(str(self.topic + "set"), self.fountain_on)

  def fountain_on(self, client, userdata, msg):
    action = 'on' if bool(msg.payload) else 'off'
    output = self.send_fountain(action)
    success = action in output
    if success:
      client.publish(str(self.topic + "/status"), payload=msg.payload, qos=1, retain=True)

  def send_fountain(self, action):
    output = subprocess.check_output([lib_dir() + "/fountain", action])
    return output
