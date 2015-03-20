import pifacedigitalio as pfio
import subprocess
pfd = pfio.PiFaceDigital()
from time import sleep

subprocess.check_output('echo "1 2 3" | festival --tts', shell=True)

pfd.output_pins[0].value = 1


# while True:
#    sleep(1)
#    pfd.leds[0].toggle()
#    sleep(1)
#    pfd.leds[1].toggle()

# pfio.init()
# from time import sleep

# while True:
#        pfio.digital_write(0, 1)
#        sleep(1)
#        pfio.digital_write(0, 0)
#        sleep(1)

