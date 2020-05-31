"""
* Usage:
*   markisol.sendMarkisolCommand(41-bit_binary_string)
*
* More info on the protocol can be found at akirjavainen/markisol
* Forked from https://github.com/akirjavainen/markisol
* by Cameron Moon <cameron@cameronmoon.com>
"""
import time
import os
import RPi.GPIO as GPIO

TRANSMIT_PIN = 16  # BCM PIN 23 (GPIO23, BOARD PIN 16)
REPEAT_COMMAND = 8

# Microseconds (us) converted to seconds for time.sleep() function:
MARKISOL_AGC1_PULSE = 0.004885
MARKISOL_AGC2_PULSE = 0.00245
MARKISOL_AGC3_PULSE = 0.0017
MARKISOL_RADIO_SILENCE = 0.005057
MARKISOL_PULSE_SHORT = 0.00034
MARKISOL_PULSE_LONG = 0.00068

MARKISOL_COMMAND_BIT_ARRAY_SIZE = 41

def sendMarkisolCommand(command):
    if len(str(command)) is not MARKISOL_COMMAND_BIT_ARRAY_SIZE:
        print(len(str(command)), "bits is not a valid command length.")

    # Prepare:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

    # Send command:
    for t in range(REPEAT_COMMAND):
        doMarkisolTribitSend(command)

    # Radio silence at the end of last command:
    transmitLow(MARKISOL_RADIO_SILENCE)

    # Disable output to transmitter and clean up:
    # exitProgram()
    GPIO.output(TRANSMIT_PIN, GPIO.LOW)
    GPIO.cleanup()

def doMarkisolTribitSend(command):
    # AGC bits:
    transmitHigh(MARKISOL_AGC1_PULSE)  # AGC 1
    transmitLow(MARKISOL_AGC2_PULSE)  # AGC 2
    transmitHigh(MARKISOL_AGC3_PULSE)  # AGC 3

    for i in command:

        if i == '0':  # LOW-HIGH-LOW
            transmitLow(MARKISOL_PULSE_SHORT)
            transmitHigh(MARKISOL_PULSE_SHORT)
            transmitLow(MARKISOL_PULSE_SHORT)

        elif i == '1':  # LOW-HIGH-HIGH
            transmitLow(MARKISOL_PULSE_SHORT)
            transmitHigh(MARKISOL_PULSE_LONG)

        else:
            print("Invalid character", i, "in command.")

def transmitHigh(delay):
    GPIO.output(TRANSMIT_PIN, GPIO.HIGH)
    time.sleep(delay)

def transmitLow(delay):
    GPIO.output(TRANSMIT_PIN, GPIO.LOW)
    time.sleep(delay)
