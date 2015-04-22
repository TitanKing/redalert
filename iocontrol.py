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
                if self.input_listen_reset():
                    if self.default_state():
                        if str(state.active_zone["output_cat_id_reset_nzone"]) != "null":
                            return int(state.active_zone["output_cat_id_reset_nzone"])
                else:
                    print("Active State Reached")
                    print(state.active_zone)
        elif self.zones():
            if state.active_zone:
                print(state.active_zone)
                self.output()

        return None

        """
        if self.output_listen(state):
            if self.input_listen_reset(state) or self.output_timeout_reset(state):
                self.output_controller_disengage(state)
        elif self.input_listen_combo(state):
            self.output_controller(state)
        else:
            if self.input_listen(state):
                self.output_controller(state)
        """

    def default_state(self):
        output_pin = 0
        while output_pin < 8:
            print("Turning off " + "output_" + str(output_pin))
            piFace.output_pins[output_pin].turn_off()
            self.io.active_output_pin[output_pin] = False
            output_pin += 1
        return True

    def output(self):
        if self.io.active_zone and self.io.active_zone['outputs']:
            for outputs in self.io.active_zone['outputs']:
                print("Turning on " + "output_" + str(outputs['output_pin']))
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
                    print("Input Triggered:" + str(zone['inputs'][0]['input_cat_name']))
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
                    print("Input Reset Triggered:" + str(az['inputs'][0]['input_cat_name']))
                    return True
        else:
            return False

    def output_listen(self):
        output_pin = 0
        while output_pin < 8:
            if int(self.io.active_output_pin[output_pin]):
                print("Output on " + "output_" + str(output_pin))
                return True
            output_pin += 1

    """
    Old Code ------------------ Old Code ------------------ Old Code
    """

    @staticmethod
    def input_listen_combo(state):
        input_pin_a = 0
        input_pin_b = 1
        while input_pin_a < 8:
            if int(state.config["input_" + str(input_pin_a) + "_" + str(input_pin_b)]):
                if int(piFace.input_pins[input_pin_a].value) and int(piFace.input_pins[input_pin_b].value):
                    print("Input on " + "input_" + str(input_pin_a) + "_" + str(input_pin_b))
                    return True
            if input_pin_a == 6 and input_pin_b == 7:
                return
            input_pin_b += 1
            if input_pin_b == 8:
                input_pin_a += 1
                input_pin_b = input_pin_a + 1

    @staticmethod
    def input_listen_(state):
        input_pin = 0
        while input_pin < 8:
            if int(state.config["input_" + str(input_pin)]) and int(piFace.input_pins[input_pin].value):
                print("Input on " + "input_" + str(input_pin))
                return True
            input_pin += 1

    @staticmethod
    def input_listen_reset_(state):
        input_pin = 0
        print("Listening to reset...")
        while input_pin < 8:
            if int(state.config["input_can_reset_" + str(input_pin)]) and int(piFace.input_pins[input_pin].value):
                print("Reset on " + "input_" + str(input_pin))
                return True
            input_pin += 1

    @staticmethod
    def output_timeout_reset(state):
        output_pin = 0
        print("Listening to timeout:" + str(time.time() - int(state.trigger_time[output_pin])))
        while output_pin < 8:
            if state.active_output_pin[output_pin] and float(state.config["timeout_output_" + str(output_pin)]) > 0:
                if float(state.config["timeout_output_" + str(output_pin)]) <= (time.time() - int(state.trigger_time[output_pin])):
                    print("Timeout on " + "output_" + str(output_pin))
                    return True
            output_pin += 1

    @staticmethod
    def output_controller_disengage(state):
        output_pin = 0
        while output_pin < 8:
            if int(state.active_output_pin[output_pin]):
                print("Turning off " + "output_" + str(output_pin))
                piFace.output_pins[output_pin].turn_off()
                state.active_output_pin[output_pin] = False
                state.trigger_time[output_pin] = 0
            output_pin += 1

    @staticmethod
    def output_controller(state):
        output_pin = 0
        while output_pin < 8:
            if int(state.config["output_" + str(output_pin)]):
                print("Turning on " + "output_" + str(output_pin))
                piFace.output_pins[output_pin].turn_on()
                state.active_output_pin[output_pin] = True
                state.trigger_time[output_pin] = time.time()
            output_pin += 1