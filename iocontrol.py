"""
; RedAlert
; Started 2015-03-20
; Copyright (c) 2015 by Jason Schoeman
;
; InputListener can be changed to a custom version to support other IO devices by calling your file instead.
"""

###########################################
# General libraries
###########################################
import time

###########################################
# Handles all database related stuff.
###########################################
import model

###########################################
# Import PiFace 2 (Element4) API.
# Please see element14.com for installation
# instructions... its easy, quickly go read
# it. :p :p :D.... :| ..... :( .... :,( ...
###########################################
import pifacedigitalio
piFace = pifacedigitalio.PiFaceDigital()


###########################################
# Listens to ports being closed or opened.
# Easy.
###########################################
class IO:
    def __init__(self):
        self.io = []

    def controller(self, state):
        self.io = state
        if self.output_listen():
            if state.active_zone:
                if self.output_timeout():
                    if self.default_state():
                        if str(state.active_zone["output_timeout_nzone"]) != "null":
                            return int(state.active_zone["output_timeout_nzone"])
                if self.input_listen_reset():
                    if self.default_state():
                        if str(state.active_zone["output_cat_id_reset_nzone"]) != "null":
                            return int(state.active_zone["output_cat_id_reset_nzone"])

        elif self.zones():
            if state.active_zone:
                self.output()

        return None

    def default_state(self):
        output_pin = 0
        while output_pin < 8:
            model.Put.log("Turning off " + "output_" + str(output_pin), "off", "output_" + str(output_pin))
            piFace.output_pins[output_pin].turn_off()
            self.io.active_output_pin[output_pin] = False
            self.io.trigger_time[output_pin] = 0
            output_pin += 1
        return True

    def output(self):
        if self.io.active_zone and self.io.active_zone['outputs']:
            for outputs in self.io.active_zone['outputs']:
                model.Put.log("Turning on " + "output_" + str(outputs['output_pin']),
                              "on", "output_" + str(outputs['output_pin']))
                piFace.output_pins[int(outputs['output_pin'])].turn_on()
                self.io.active_output_pin[outputs['output_pin']] = True
                self.io.trigger_time[outputs['output_pin']] = time.time()

    def zones(self):
        if self.io.active_zone:
            return False
        if self.io.zones:
            for zzz in self.io.zones:
                return self.input_listen(zzz)
        else:
            return False

    def input_listen(self, zone):
        if zone['inputs']:
            inputs_trigger = []
            for inputs in zone['inputs']:
                i = int(inputs['input_pin'])
                if int(piFace.input_pins[i].value) == 0:
                    inputs_trigger.append(True if zone['input_nc'] else False)
                else:
                    inputs_trigger.append(False if zone['input_nc'] else True)

            if inputs_trigger:
                if False in inputs_trigger:
                    return False
                else:
                    model.Put.log("Triggered input category " + str(zone['inputs'][0]['input_cat_name']),
                                  "input_trigger", "input_cat_" + str(zone['inputs'][0]['input_cat_id']))
                    self.io.active_zone = zone
                    return True
        else:
            return False

    def input_listen_reset(self):
        if self.io.active_zone['inputs_reset']:
            az = self.io.active_zone
            inputs_trigger = []
            for inputs in az['inputs_reset']:
                i = int(inputs['input_pin'])
                if int(piFace.input_pins[i].value) == 0:
                    inputs_trigger.append(True if az['input_nc'] else False)
                else:
                    inputs_trigger.append(False if az['input_nc'] else True)

            if inputs_trigger:
                if False in inputs_trigger:
                    return False
                else:
                    model.Put.log("Reset from input category " + str(az['inputs'][0]['input_cat_name']),
                                  "input_reset", "input_cat_" + str(az['inputs'][0]['input_cat_id']))
                    return True
        else:
            return False

    def output_timeout(self):
        if self.io.active_zone and self.io.trigger_time:
            az = self.io.active_zone
            print(az["output_timeout"])
            for output_pin, active_output_time in self.io.trigger_time.items():
                if str(az["output_timeout"]) != "null" \
                        and float(az["output_timeout"]) > 0 \
                        and float(self.io.trigger_time[output_pin]) > 0:
                    model.Put.log("Ready timeout on output " + str(output_pin) +
                                  " at time " + str(self.io.trigger_time[output_pin]),
                                  "timeout_set", "output_" + str(self.io.trigger_time[output_pin]))
                    if float(az["output_timeout"]) <= (time.time() - int(self.io.trigger_time[output_pin])):
                        model.Put.log("Timeout reached on output " + str(output_pin),
                                      "timeout_reached", "output_" + str(output_pin))
                        return True

    def output_listen(self):
        output_pin = 0
        while output_pin < 8:
            if self.io.active_output_pin[output_pin]:
                model.Put.log("Status output on " + str(output_pin), "output_status", "output_" + str(output_pin))
                return True
            output_pin += 1