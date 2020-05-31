class MessageLogger(object):
  def log_message(self, client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

  def attach(self, client, parent_topic):
    self.topic = parent_topic + "#"
    client.message_callback_add(str(self.topic), self.log_message)
