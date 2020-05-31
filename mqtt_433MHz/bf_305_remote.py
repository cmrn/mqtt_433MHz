from markisol import sendMarkisolCommand

# * Command is as follows:
# * 16 bits for (unique) remote control ID, hard coded in remotes
# * 4 bits for channel ID: 1 = 1000 (also used by BF-301), 2 = 0100 (also used by BF-101), 3 = 1100, 4 = 0010, 5 = 1010, ALL = 1111
# * 4 bits for command: DOWN = 1000, UP = 0011, STOP = 1010, CONFIRM/PAIR = 0010, LIMITS = 0100, ROTATION DIRECTION = 0001
# * 8 bits for remote control model: BF-305 multi = 10000110, BF-101 single = 00000011, BF-301 single = 10000011
# * 9 bits for something? I have yet to figure out how this is formed, but most motors simply do not seem to care (others do)
# *
# * = 41 bits in total

commands = {
  "outer": { # Example channel
    "up": "10111011111011111000001110000011110101011",
    "down": "10111011111011111000100010000011110110101",
    "stop": "10111011111011111000101010000011110110001",
    "pair": "10111011111011111000001010000011110101001",
  },
  "inner": { # Channel 5
    "up": "00010000011011011010001110000110101110001",
    "down": "00010000011011011010100010000110101100111",
    "stop": "00010000011011011010101010000110101100011",
    "pair": "00010000011011011010001010000110101110011"
  },
}

def send_command(channel, action):
  sendMarkisolCommand(commands[channel][action])