
#!/usr/bin/python

import serial
import time
from secrets import MASTER_API_KEY, DEVICE_ID
from m2x.client import M2XClient

# rate limiting
MIN_SECS_BEFORE_UPDATE = 60

def average(l):
    # integer (rounded) average of all numbers in a list
    return int(round(float(sum(l)) / max(len(l), 1)))

# read this:
# https://stackoverflow.com/questions/17553543/pyserial-non-blocking-read-loop
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=60)

# AT&T M2X Setup
client = M2XClient(key=MASTER_API_KEY)
device = client.device(DEVICE_ID)
small_particles_stream = device.stream('small-particles')
large_particles_stream = device.stream('large-particles')

last_updated = 0
collected_large = []
collected_small = []
while True:
    if ser.inWaiting() > 0:
        line = ser.readline()
        small, large = [int(x) for x in line.split(',')]
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print "%s small: %i large: %i" % (now, small, large)
        collected_large.append(large)
        collected_small.append(small)

        # This is rate-limiting because to be under-quota for AT&T, we need to post
        # every 60 seconds or less, but the sensor pushes data every 59 seconds
        if time.time() - last_updated >= MIN_SECS_BEFORE_UPDATE:
            # Compute the average of particle sizes (if we have more than 1 queued entriy)
            small_avg = average(collected_small)
            large_avg = average(collected_large)

            # Post Results to AT&T
            small_particles_stream.add_value(small_avg)
            large_particles_stream.add_value(large_avg)

            # Reset State
            collected_small = []
            collected_large = []
            last_updated = time.time()
    else:
        time.sleep(0.5)
    
ser.close()
