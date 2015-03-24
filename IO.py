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
import pifacedigitalio as piFaceApi
piFace = piFaceApi.PiFaceDigital()


###########################################
# Listens to ports being closed or opened.
# Easy.
###########################################
class IO:
    def controller(self, state):
        if self.output_listen(state):
            if self.input_listen_reset(state) or self.output_timeout_reset(state):
                self.output_controller_disengage(state)
        else:
            if self.input_listen(state):
                self.output_controller(state)

    @staticmethod
    def input_listen(state):
        input_pin = 0
        while input_pin < 8:
            if int(state.config["input_" + str(input_pin)]) == 1 and int(piFace.input_pins[input_pin].value) == 1:
                print("Input on " + "input_" + str(input_pin))
                return True
            input_pin += 1

    @staticmethod
    def input_listen_reset(state):
        input_pin = 0
        print("Listening to reset...")
        while input_pin < 8:
            if int(state.config["input_can_reset_" + str(input_pin)]) == 1 and int(piFace.input_pins[input_pin].value) == 1:
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
    def output_listen(state):
        output_pin = 0
        while output_pin < 8:
            if int(state.active_output_pin[output_pin]) == 1:
                print("Output on " + "output_" + str(output_pin))
                return True
            output_pin += 1

    @staticmethod
    def output_controller_disengage(state):
        output_pin = 0
        while output_pin < 8:
            if int(state.active_output_pin[output_pin]) == 1:
                print("Turning off " + "output_" + str(output_pin))
                piFace.output_pins[output_pin].turn_off()
                state.active_output_pin[output_pin] = False
                state.trigger_time[output_pin] = 0
            output_pin += 1

    @staticmethod
    def output_controller(state):
        output_pin = 0
        while output_pin < 8:
            if int(state.config["output_" + str(output_pin)]) == 1:
                print("Turning on " + "output_" + str(output_pin))
                piFace.output_pins[output_pin].turn_on()
                state.active_output_pin[output_pin] = True
                state.trigger_time[output_pin] = time.time()
            output_pin += 1