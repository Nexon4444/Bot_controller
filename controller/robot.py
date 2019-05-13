import mraa
import time
import threading
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
from Queue import Queue

class Control(object):
    sensor_pin_id = 45
    program_on_bot = False

    def __init__(self):
        if Control.program_on_bot:
            mraa.pwma = mraa.Pwm(20)
            mraa.pwma.period_us(1000)
            mraa.pwma.enable(True)

            mraa.pwmb = mraa.Pwm(14)
            mraa.pwmb.period_us(1000)
            mraa.pwmb.enable(True)

            mraa.a1 = mraa.Gpio(33)
            mraa.a1.dir(mraa.DIR_OUT)
            mraa.a2 = mraa.Gpio(46)
            mraa.a2.dir(mraa.DIR_OUT)

            mraa.b1 = mraa.Gpio(48)
            mraa.b1.dir(mraa.DIR_OUT)
            mraa.b2 = mraa.Gpio(36)
            mraa.b2.dir(mraa.DIR_OUT)

    def move(self, xpa, xpb, xa1, xa2, xb1, xb2, t):
        # time.sleep(0.1)
        mraa.pwma.write(xpa)
        mraa.pwmb.write(xpb)
        mraa.a1.write(xa1)
        mraa.b1.write(xb1)
        mraa.a2.write(xa2)
        mraa.b2.write(xb2)

        time.sleep(t)
        mraa.a1.write(0)
        mraa.b1.write(0)
        mraa.a2.write(0)
        mraa.b2.write(0)
        mraa.pwma.write(0)
        mraa.pwma.write(0)
        # time.sleep(0.1)

    def forward(self, tide):
        print("driving forward")
        self.move(1, 1, 1, 0, 1, 0, tide)

    def back(self, tide):
        print("driving back")
        self.move(1, 1, 0, 1, 0, 1, tide)

    def lrotate(self, tide):
        print("lrotating")
        self.move(1, 1, 0, 1, 1, 0, tide)

    def rrotate(self, tide):
        print("rrotating")
        self.move(1, 1, 1, 0, 0, 1, tide)

    def lturn(self, tide):
        print("lturning")
        self.move(0.5, 1, 1, 0, 1, 0, tide)

    def rturn(self, tide):
        print ("rturning")
        self.move(1, 0.5, 1, 0, 1, 0, tide)

    def movement_front_until_event(self, e):
        # print "q: " + str(q.get())
        logging.log(logging.DEBUG, "before wait")
        self.forward_nonstop()
        e.wait()
        self.stop()
        logging.log(logging.DEBUG, "after stop")

    def get_sensor_info(self, e, switching_to):
        # e = threading.Event()
        gpio = mraa.Gpio(Control.sensor_pin_id)
        prev_switch = gpio.read()
        while (True):
            switch = gpio.read()
            # logging.log(logging.DEBUG, "switch: " + str(switch))
            if switch != prev_switch and switch == switching_to:
                logging.log(logging.DEBUG, "switch: " + str(switch))
                logging.log(logging.DEBUG, "event before: " + str(e.is_set()))
                e.set()
                logging.log(logging.DEBUG, "event after: " + str(e.is_set()))
            prev_switch = switch

    def move_nonstop(self, xpa, xpb, xa1, xa2, xb1, xb2):
        mraa.pwma.write(xpa)
        mraa.pwmb.write(xpb)
        mraa.a1.write(xa1)
        mraa.b1.write(xb1)
        mraa.a2.write(xa2)
        mraa.b2.write(xb2)

    def stop(self):
        mraa.a1.write(0)
        mraa.b1.write(0)
        mraa.a2.write(0)
        mraa.b2.write(0)
        mraa.pwma.write(0)
        mraa.pwma.write(0)

    def forward_nonstop(self, speed):
        print("driving forward")
        self.move_nonstop(speed, speed, 1, 0, 1, 0)

    def back_nonstop(self, speed):
        print("driving back")
        self.move_nonstop(speed, speed, 0, 1, 0, 1)

    def lrotate_nonstop(self, speed):
        print("lrotating")
        self.move_nonstop(speed, speed, 0, 1, 1, 0)

    def rrotate_nonstop(self, speed):
        print("rrotating")
        self.move_nonstop(speed, speed, 1, 0, 0, 1)

    def lturn_nonstop(self, speed):
        print("lturning")
        self.move_nonstop(0.5, 1, 1, 0, 1, 0)

    def rturn_nonstop(self, speed):
        print ("rturning")
        self.move_nonstop(1, 0.5, 1, 0, 1, 0)

    # def move_front_until_sensor_act(self):
    #     e = threading.Event()
    #     con = Control()
    #     # q = Queue()
    #     # q.put(1)
    #     # con.forward_nonstop()
    #     # time.sleep(1)
    #     # con.stop()
    #     t = threading.Thread(target=self.movement_front_until_event, args=[con, e])
    #     t2 = threading.Thread(target=self.get_sensor_info, args=[e])
    #     t.start()
    #     t2.start()
    #
    #     t.join()
    #     t2.join()

    def measure_turn_rate(self, e, speed):
        # e = threading.Event()
        number_of_turns = 5
        start = time.time()

        for i in range(0, number_of_turns):
            self.rrotate_nonstop(speed)
            logging.log(logging.DEBUG, "i: " + str(i))

            e.wait()
            e.clear()
            logging.log(logging.DEBUG, "stopped waiting")

        self.stop()
        end = time.time()
        time_of_turns = end - start
        print (time_of_turns)

    def measure_moving_speed(self, e, speed):
        number_of_lines = 1
        start = time.time()

        for i in range(0, number_of_lines):
            self.forward_nonstop(speed)
            logging.log(logging.DEBUG, "i: " + str(i))

            e.wait()
            e.clear()
            logging.log(logging.DEBUG, "stopped waiting")

        self.stop()
        end = time.time()
        time_of_movement = end - start
        logging.log(logging.DEBUG, "movement time: " + str(time_of_movement))

    def calibrate(self):
        print ("put robot on a calibration sheet, enter '1' to continue")
        entered = input("put robot on a calibration sheet, enter '1' to continue: ")
        while (entered is not 1):
            entered = input("put robot on a calibration sheet, enter '1' to continue: ")

        e = threading.Event()
        pwm = 0.65
        t_measure_speed = threading.Thread(target=self.measure_moving_speed, args=[e, pwm])
        # t_measure = threading.Thread(target=self.measure_turn_rate, args=[e, speed])
        t_sensor = threading.Thread(target=self.get_sensor_info, args=[e, 0])

        t_measure_speed.start()
        # t_measure.start()
        t_sensor.start()

        t_measure_speed.join()
        # t_measure.join()
        t_sensor.join()

    # def get_sensor_info(self, q):
    #     gpio = mraa.Gpio(Control.sensor_pin_id)
    #     while (True):
    #         s = gpio.read()
    #         print s
    #         q.put(s)
    #
    # def movement_front(self, q):
    #     x = 0
    #     for i in range(0, 10):
    #         if q.get() is 0:
    #             exit()
    #         print "q: " + q.get()
    #         self.forward(float(1))
    #         print "x =" + str(x)
    #         x = x + 1

