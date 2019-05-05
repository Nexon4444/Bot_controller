import mraa
import time
import threading
from Queue import Queue

class Control(object):
    sensor_pin_id = 45
    def __init__(self):
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

    def forward_nonstop(self):
        print("driving forward")
        self.move_nonstop(1, 1, 1, 0, 1, 0)

    def back_nonstop(self):
        print("driving back")
        self.move_nonstop(1, 1, 0, 1, 0, 1)

    def lrotate_nonstop(self):
        print("lrotating")
        self.move_nonstop(1, 1, 0, 1, 1, 0)

    def rrotate_nonstop(self):
        print("rrotating")
        self.move_nonstop(1, 1, 1, 0, 0, 1)

    def lturn_nonstop(self):
        print("lturning")
        self.move_nonstop(0.5, 1, 1, 0, 1, 0)


    def rturn_nonstop(self):
        print ("rturning")
        self.move_nonstop(1, 0.5, 1, 0, 1, 0)



    def move_front_until_sensor_act(self):
        q = Queue()
        t_sensor = threading.Thread(target=self.get_sensor_info, args=[q])
        t_movement = threading.Thread(target=self.forward, args=[q])

        t_movement.start()
        t_sensor.start()


        t_sensor.join()
        t_movement.join()

    def get_sensor_info(self, q):
        gpio = mraa.Gpio(Control.sensor_pin_id)
        while (True):
            s = gpio.read()
            print s
            q.put(s)

    def movement_front(self, q):
        x = 0
        for i in range(0, 10):
            if q.get() is 0:
                exit()
            print "q: " + q.get()
            self.forward(float(1))
            print "x =" + str(x)
            x = x + 1

