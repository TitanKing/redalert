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
        self.zb = ZoneBuilder()
        self.zones = self.zb.zones

        # If zone is triggered
        self.active_zone = []
        self.active_output_pin = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False}
        self.trigger_time = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

        while True:
            time.sleep(float(config['poll_rate']))
            if self.running:
                time.sleep(float(config['poll_rate']))
                continue
            self.running = True
            new_zone = iOc.controller(self)
            if new_zone is not None and int(new_zone):
                self.select_zone(new_zone)
            self.running = False

    def select_zone(self, zone):
        zone = int(zone)
        self.zb = ZoneBuilder(zone)
        self.zones = self.zb.zones


###########################################
# Controls and builds zones.
###########################################
class ZoneBuilder():
    def __init__(self, selected_zone=None):
        self.zones = []

        if selected_zone is not None:
            default_zone = selected_zone
        else:
            default_zone = config['default_zone_state']

        db = model.Get()
        all_zones = db.zone(default_zone)

        print("Zone Category (" + str(default_zone) + ") Loaded")

        z = []
        for z_cfg in all_zones:
            # Load input and output listeners
            inputs = db.input_cats(z_cfg['input_cat_id'])
            outputs = db.output_cats(z_cfg['output_cat_id'])
            inputs_reset = db.input_cats(z_cfg['output_cat_id_reset'])

            z_cfg['inputs'] = inputs
            z_cfg['outputs'] = outputs
            z_cfg['inputs_reset'] = inputs_reset

            z.append(z_cfg)

        if z:
            self.zones = z

###########################################
# Start the listener
###########################################
State()







