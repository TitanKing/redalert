import pifacedigitalio as pfio
pfd = pfio.PiFaceDigital()

pfio.init()
from time import sleep

while True:
        pfio.digital_write(0, 1)
        sleep(1)
        pfio.digital_write(0, 0)
        sleep(1)
