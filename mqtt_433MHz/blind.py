import bf_305_remote
import threading
from time import time

class BlindMovement(object):
  def __init__(self, blind):
    self.blind_id = blind.id
    self.start_position = blind.position
    self.target_position = blind.target
    self.topic = blind.topic
    self.client = blind.client
    self.distance = abs(self.start_position - self.target_position)
    self.travel_time = self.distance * (Blind.SPEED / 100.0)
    self.direction = 'up' if self.target_position >= self.start_position else 'down'
    self.timer = None
    self.started_at = None
    self.publish_position = blind.publish_position

  def start(self):
    if self.distance == 0:
      self.publish_position(self.target_position)
      return

    self.started_at = time()

    print("sending blind ", self.blind_id, " command ", self.direction, " (", self.start_position, "->", self.target_position, ")")
    bf_305_remote.send_command(self.blind_id, self.direction)

    print("waiting for ", self.travel_time, " seconds")
    self.timer = threading.Timer(self.travel_time, self.after_move)
    self.timer.start()

  def after_move(self):
    self.publish_position(self.target_position)

  def cancel(self):
    if not self.timer:
      return

    self.timer.cancel()
    time_elapsed = time() - self.started_at
    if time_elapsed < self.travel_time:
      position = round(self.distance * ((self.travel_time - time_elapsed) / self.travel_time))
      self.publish_position(position)


class Blind(object):
  SPEED = 40 # seconds to travel entire range

  def __init__(self, id):
    self.id = id

    self.position = 100 # 100 = raised, 0 = lowered
    self.target = 100
    self.last_move = None

  def attach(self, client, parent_topic):
    self.topic = parent_topic + "blinds/" + self.id
    self.client = client
    client.message_callback_add(str(self.topic + "set/target"), self.set_target)
    client.message_callback_add(str(self.topic + "status/position"), self.status_position)

  def set_target(self, client, userdata, msg):
    self.target = int(msg.payload)
    self.move()
    self.client.publish(str(self.topic + "status/target"), payload=self.target, qos=1, retain=True)

  def status_position(self, client, userdata, msg):
    self.position = int(msg.payload)

  def publish_position(self, position):
    self.position = int(position)
    self.client.publish(str(self.topic + "status/position"), payload=self.position, qos=1, retain=True)

  def move(self):
    if self.last_move:
      self.last_move.cancel()

    movement = BlindMovement(self)
    movement.start()
    self.last_move = movement
