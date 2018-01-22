import json
import subprocess
import time

from collections import defaultdict
from log import log_temperature
from secrets import device_mapping


# helper for timeouts
# https://stackoverflow.com/a/601168
import signal
from contextlib import contextmanager

class TimeoutException(Exception):
    pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


last_processed = defaultdict(str)



def process_entry(entry):
    global last_processed

    # Check if we've processed this before
    device_id = int(entry['id'])
    if last_processed[device_id] == entry['time']:
        #print "already seen: ", entry
        return
    #else:
    #    print "first time seeing: ", entry
    last_processed[device_id] = entry['time']

    # process this here
    temperature_celsius = entry['temperature_C']
    temperature = 1.8 * temperature_celsius + 32
    humidity = entry['humidity']

    device_name = device_mapping[device_id]

    # Log it
    log_temperature(device_name, temperature, humidity)


def main():
    proc = subprocess.Popen(['rtl_433', '-F', 'json', '-R', '40'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10) # let rtl_433 initialize
    while True:
        try:
            #print "waiting to read input"
            with time_limit(30):
                #print "trying to read with limit"
                input_ = proc.stdout.readline()
                #print "input_ = ", input_
            # print "poll: ", proc.poll()
            if proc.poll():
                print "subprocess has returned"
                break
                #print "stderr: "
                #print proc.stderr.read()
            # print "input: ", input_
            # print "input_:", input_
            payload = json.loads(input_.decode("utf-8"))
            #print "payload = ", payload
            process_entry(payload)
        except ValueError:
            # bad json value
            break
            # print "bad json value: ", input_, "\nignoring"
            # continue
        except KeyboardInterrupt:
            break
        except TimeoutException:
            print "timout exception reached, exiting"
            break
        except Exception:
            # any exception, we want to kill the process
            print "warning: random exception caught and exiting"
            break
    print "Going to exit now"
    proc.kill()

if __name__ == '__main__':
    main()
