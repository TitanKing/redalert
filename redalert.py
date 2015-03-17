import pifacedigitalio as pfio
pfd = pfio.PiFaceDigital()
from time import sleep

while True:
    sleep(1)
    pfd.leds[1].toggle()
    sleep(1)
    pfd.leds[2].toggle()
    sleep(1)
    pfd.leds[3].toggle()

# pfio.init()
# from time import sleep

# while True:
#        pfio.digital_write(0, 1)
#        sleep(1)
#        pfio.digital_write(0, 0)
#        sleep(1)
