import sys
import subprocess
import http.server
import urllib.parse
import time
import pifacedigitalio as pifaceapi
import redModel


piFaceO = pifaceapi.PiFaceDigital()


"""
    REDALERT SETTINGS
"""
redalert_alarm_on_count = 5

"""
    HTTP SERVER SETTINGS
"""
JSON_FORMAT = "{{'input_port': {input}, 'output_port': {output}}}"
DEFAULT_PORT = 8000
OUTPUT_PORT_GET_STRING = "output_port"
GET_IP_CMD = "hostname -I"


class PiFaceWebHandler(http.server.BaseHTTPRequestHandler):
    """Handles PiFace web control requests"""
    def do_GET(self):
        output_value = self.pifacedigital.output_port.value
        input_value = self.pifacedigital.input_port.value

        # parse the query string
        qs = urllib.parse.urlparse(self.path).query
        query_components = urllib.parse.parse_qs(qs)

        # set the output
        if OUTPUT_PORT_GET_STRING in query_components:
            new_output_value = query_components["output_port"][0]
            output_value = self.set_output_port(new_output_value, output_value)

        # reply with JSON
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(JSON_FORMAT.format(
            input=input_value,
            output=output_value,
        ), 'UTF-8'))

    def set_output_port(self, new_value, old_value=0):
        """Sets the output port value to new_value, defaults to old_value."""
        print("Setting output port to {}.".format(new_value))
        port_value = old_value
        try:
            port_value = int(new_value)  # dec
        except ValueError:
            port_value = int(new_value, 16)  # hex
        finally:
            self.pifacedigital.output_port.value = port_value
            return port_value


def get_my_ip():
    """Returns this computers IP address as a string."""
    ip = subprocess.check_output(GET_IP_CMD, shell=True).decode('utf-8')[:-1]
    return ip.strip()

class RedAlert:
    def __init__(self, toggle_delay_time=None):
        if toggle_delay_time is None:
            toggle_delay_time = 0

        self.log("Starting RedAlert V0.1-1")
        # self.start_web_server()
        self.listener = pifaceapi.InputEventListener(chip=piFaceO)
        self.alarm_trigger_count = 0
        self.alarm_activated_timestamp = 0

    def start_web_server(self):
        self.log("Started Web Server")
        # get the port
        if len(sys.argv) > 1:
            port = int(sys.argv[1])
        else:
            port = DEFAULT_PORT

        # set up PiFace Digital
        PiFaceWebHandler.pifacedigital = piFaceO

        self.log("Starting simple PiFace web control at:\n\n"
                 "\thttp://{addr}:{port}\n\n"
                 "Change the output_port with:\n\n"
                 "\thttp://{addr}:{port}?output_port=0xAA\n"
                 .format(addr=get_my_ip(), port=port))

        # run the server
        server_address = ('', port)
        try:
            httpd = http.server.HTTPServer(server_address, PiFaceWebHandler)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('^C received, shutting down server')
            httpd.socket.close()

    def input_listen0(self, action_type=None):
        if action_type is None:
            action_type = "toggle"

        if action_type == "toggle":
            self.listener.register(0, pifaceapi.IODIR_FALLING_EDGE, self.toggle_output0)
        elif action_type == "timer":
            self.listener.register(0, pifaceapi.IODIR_FALLING_EDGE, self.output_on_delay_of0)


    def input_listen1(self):
        self.listener.register(1, pifaceapi.IODIR_FALLING_EDGE, self.toggle_output1)

    def input_listen2(self):
        self.listener.register(2, pifaceapi.IODIR_FALLING_EDGE, self.toggle_output2)

    def input_listen3(self):
        self.listener.register(3, pifaceapi.IODIR_FALLING_EDGE, self.toggle_output3)

    def input_listen4(self):
        self.listener.register(4, pifaceapi.IODIR_FALLING_EDGE, self.toggle_output4)

    def input_listen5(self):
        self.listener.register(5, pifaceapi.IODIR_FALLING_EDGE, self.toggle_output5)

    def input_listen6(self):
        self.listener.register(6, pifaceapi.IODIR_FALLING_EDGE, self.toggle_output6)

    def input_listen7(self):
        self.listener.register(7, pifaceapi.IODIR_FALLING_EDGE, self.output_on_delay_of0)

    def output_on_delay_of0(self, event):
        self.alarm_trigger_count += 1

        if event.chip.relays[0].value == 0:
            self.alarm_activated_timestamp = time.time()
            event.chip.relays[0].turn_on()
            self.log("Relay 0 switched ON")
        else:
            self.log("Relay 0 already ON")

        if redalert_alarm_on_count == self.alarm_trigger_count or (time.time() - self.alarm_activated_timestamp) > 10:
            self.log("Alarm counter " + str(self.alarm_trigger_count))
            event.chip.relays[0].turn_off()
            self.log("Relay 0 switched OFF")
            self.alarm_trigger_count = 0
            self.alarm_activated_timestamp = 0

    def toggle_output0(self, event):
        event.chip.relays[0].toggle()

    def toggle_output1(self, event):
        event.chip.relays[1].toggle()

    def start_listener(self):
        self.listener.activate()

    @staticmethod
    def log(message):
        print(str(message))