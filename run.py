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
# Handles all database related stuff.
###########################################
import model

###########################################
# For reading inputs from RaspberryPi I/O
# device, PiFace is default.
###########################################
import iocontrol
iOc = iocontrol.IO()

###########################################
# Opens web server for API calls to control
# RedAlert remotely with.
###########################################
# import httpapi
# httpapi.Server()


###########################################
# Runtime States Engine
###########################################
class State(object):
    def __init__(self):
        self.running = False
        self.zones = ZoneBuilder().zones

        self.active_output_pin = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False}
        self.trigger_time = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

        while True:
            time.sleep(float(config['poll_rate']))
            if self.running:
                time.sleep(float(config['poll_rate']))
                continue
            self.running = True
            iOc.controller(self)
            self.running = False


###########################################
# Controls and builds the ZONES_
###########################################
class ZoneBuilder():
    def __init__(self):
        self.zones = []

        default_zone = config['default_zone_state']

        db = model.Get()
        all_zones = db.zone(default_zone)

        z = []
        for z_cfg in all_zones:
            # Load input and output listeners
            inputs = db.input_cats(z_cfg['input_cat_id'])
            outputs = db.output_cats(z_cfg['output_cat_id'])

            z_cfg['inputs'] = inputs
            z_cfg['outputs'] = outputs

            z.append(z_cfg)

        if z:
            self.zones = z


###########################################
# Start the listener
###########################################
State()







