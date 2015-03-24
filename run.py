"""
; RedAlert
; Started 2015-03-20
; Copyright (c) 2015 by Jason Schoeman
;
; Whats This? This file should be executed, eg: python3 run.py
"""

###########################################
# General libraries
###########################################
import time

###########################################
# For parsing the configuration file
###########################################
import configparser
iniCfg = configparser.ConfigParser()
iniCfg.sections()
iniCfg.read('config.ini')
config = iniCfg['DEFAULT']

###########################################
# For reading inputs from RaspberryPi I/O
# device, PiFace is default.
###########################################
import IO
iOc = IO.IO()


###########################################
# Runtime States Engine
###########################################
class State(object):
    def __init__(self):
        self.armed = False
        self.trigger = False
        self.alarm = False
        self.running = False
        self.config = ZoneBuilder().zone_config
        self.active_output_pin = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False}
        self.trigger_time = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

        while True:
            time.sleep(float(config["poll_rate"]))
            if self.running:
                time.sleep(float(config["poll_rate"]))
                continue
            self.running = True
            iOc.controller(self)
            self.running = False


###########################################
# Controls and builds the ZONES_
###########################################
class ZoneBuilder():
    def __init__(self, set_zone=None):
        if set_zone is None:
            set_zone = 'ZONE_0'
        self.zone_config = iniCfg[set_zone]


###########################################
# Start the listener
###########################################
State()







