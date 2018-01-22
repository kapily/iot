from secrets import MASTER_API_KEY, ADAFRUIT_KEY, BLYNK_TOKEN
from Adafruit_IO import Client, Feed
# from blynkapi import Blynk

"""
blink_objects = {
    'living-temp': Blynk(BLYNK_TOKEN, pin = "V0"),
    'bedroom-temp': Blynk(BLYNK_TOKEN, pin = "V1"),
    'balcony-temp': Blynk(BLYNK_TOKEN, pin = "V2"),
    'frontdoor-temp': Blynk(BLYNK_TOKEN, pin = "V3"),
}
"""

"""
# AT&T M2X Setup
from m2x.client import M2XClient
client = M2XClient(key=MASTER_API_KEY)

devices = {}
streams = {}

small_particles_stream = device.stream('small-particles')
large_particles_stream = device.stream('large-particles')
"""

# ADA Fruit
aio = Client(ADAFRUIT_KEY)

"""
class ATTM2XLogging(object):

    # TODO - keep track of rate-limiting here


    def get_device(device_id):
        global devices
        if device_id not in devices:
            devices[device_id] = client.device(device_id)
        return devices[device_id]

    def get_stream(device_id, stream):
        global devices
        global streams
        if device_id not in streams:
            streams[device_id] = {}

        if stream not in streams[device_id]:
            streams[device_id][stream] = devices[device_id].stream(stream)

        return streams[device_id][stream]


    def log_to_m2x(device_id, stream, value):
        get_stream(device_id, stream).add_value(value)
"""

def log_temperature(device_name, temperature, humidity):
    aio.send(device_name + '-temp', temperature)
    aio.send(device_name + '-humidity', humidity)
    # blink_objects[device_name + '-temp'].set_val(temperature)
