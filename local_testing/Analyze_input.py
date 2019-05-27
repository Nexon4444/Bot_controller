import threading
import time


class SensorAnalyzer():
    board_size = [800, 600]

    def __init__(self):
        self.c1 = threading.Condition()
        self.c2 = threading.Condition()
        self.sig1 = 0
        self.sig2 = 0

        self.whl_left_dir
        self.simulate()
        # self.read_signals()

    def read_signals(self):
        while(True):
            print ("sig1 = " + str(self.sig1) + " sig2 = " + str(self.sig2))
            time.sleep(0.05)


    def simulate(self):
            t1 = threading.Thread(target=self.produce_signal, args=[1, 10])
            t2 = threading.Thread(target=self.produce_signal, args=[0, 1])
            t_read = threading.Thread(target=self.read_signals)

            t1.start()
            t2.start()
            t_read.start()

            t1.join()
            t2.join()
            t_read.join()

    def produce_signal(self, which, speed):
        if which is 1:
            while True:
                self.c1.acquire()
                self.sig1 = 1
                self.c1.release()
                time.sleep(1)

                self.c1.acquire()
                self.sig1 = 0
                self.c1.release()
                time.sleep(speed)
        else:
            while True:
                self.c2.acquire()
                self.sig2 = 1
                self.c2.release()
                time.sleep(1)

                self.c2.acquire()
                self.sig2 = 0
                self.c2.release()
                time.sleep(speed)

    def localise(self):

    # def simulate_signal(self, sig):
        sa = SensorAnalyzer()