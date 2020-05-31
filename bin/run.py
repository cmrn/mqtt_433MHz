#!/usr/bin/python
import sys, os
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.append(parent_dir)


import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from mqtt_433MHz import MQTT433MHz
mqtt433MHz = MQTT433MHz()
mqtt433MHz.client.enable_logger(logger)
mqtt433MHz.client.connect("hearth.lan", 1883)
mqtt433MHz.client.loop_forever()
