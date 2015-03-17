import pifacedigitalio as pfio
import subprocess
pfd = pfio.PiFaceDigital()
from time import sleep

subprocess.check_output('echo "Red alert security system started" | festival --tts', shell=True)

while True:
    sleep(1)
    pfd.leds[0].toggle()
    sleep(1)
    pfd.leds[1].toggle()

# pfio.init()
# from time import sleep

# while True:
#        pfio.digital_write(0, 1)
#        sleep(1)
#        pfio.digital_write(0, 0)
#        sleep(1)
