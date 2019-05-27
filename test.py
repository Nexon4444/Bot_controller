from controller.hardware import Control
from threading import Thread
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
import mraa
from Queue import Queue

def movement_front_until_sensor(self, e):
    # print "q: " + str(q.get())
    logging.log(logging.DEBUG, "before wait")
    self.forward_nonstop()
    e.wait()
    self.stop()
    logging.log(logging.DEBUG, "after stop")

def get_sensor_info(e):
    # e = threading.Event()
    gpio = mraa.Gpio(Control.sensor_pin_id)
    while (True):
        s = gpio.read()
        logging.log(logging.DEBUG, "s: " + str(s))
        if s == 0:
            e.set()
            break

e = threading.Event()
con = Control()
# q = Queue()
# q.put(1)
# con.forward_nonstop()
# time.sleep(1)
# con.stop()
t = Thread(target=movement_front, args=[con, e])
t2 = Thread(target=get_sensor_info, args=[e])
t.start()
t2.start()

t.join()
t2.join()