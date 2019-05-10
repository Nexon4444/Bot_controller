import threading
from threading import Lock
import time
import math
from numpy import arcsin, arccos, sin, cos
from shapely import geometry
# import OrderedSet
from shapely.geometry import Point, Polygon
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
# class Position:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def move(self, x, y):
#         return Position(self.x + x, self.y + y)

class Simulation:
    def __init__(self):
        self.sig0 = Lock()
        self.sig1 = Lock()

        self.sensor0 = 0
        self.sensor1 = 0

    def simulate(self):
        t_sensor0 = threading.Thread(target=self.sensor, args=[0, 1, 1])
        t_sensor1 = threading.Thread(target=self.sensor, args=[1, 1, 1])
        t_read = threading.Thread(target=self.read)

        t_sensor0.start()
        t_sensor1.start()
        t_read.start()

        t_sensor0.join()
        t_sensor1.join()
        t_read.join()

    def sensor(self, sensor_id, sensor_time, wait_time):
        for i in range(0, 1000):
            if sensor_id is 0:
                self.sig0.acquire()
                self.sensor0 = 1
                self.sig0.release()
                time.sleep(sensor_time)

                self.sig0.acquire()
                self.sensor0 = 0
                self.sig0.release()
                time.sleep(wait_time)

            else:
                self.sig1.acquire()
                # self.sig1.sig1
                self.sensor1 = 1
                self.sig1.release()
                time.sleep(sensor_time)

                self.sig1.acquire()
                self.sensor1 = 0
                self.sig1.release()
                time.sleep(wait_time)

    def read(self):
        for i in range(0, 1000):
            self.sig1.acquire()
            self.sig0.acquire()

            # logging.l
            # print "sensor0: " + str(self.sensor0) + " sensor1: " + str(self.sensor1)
            logging.log(logging.DEBUG, "sensor0: " + str(self.sensor0) + " sensor1: " + str(self.sensor1))

            self.sig0.release()
            self.sig1.release()
            time.sleep(0.25)

    def find_positions(self, r, a):
        r = float(r)
        a = float(a)

        for l in range(0, 4):
            h = r * sin(arccos(l/r))
            print h

        for h in range(3, -1, -1):
            l = r * sin(arccos(h/r))
            print l

        # for s in range(0, 4):
        #     t = float(s*a/r)
        #     print t
        #     h = r * (1 - cos(float(arcsin(t))))
        #     print "h: " + str(h)
        #
        # for s in range(0, 4):
        #     t = float((s*a)/r)
        #     # print t
        #     l = r * (sin(float(arccos(t))))
        #     print "l: " + str(l)

    def check_if_between(self, last_poz, r, a):
        next_up = last_poz + Vector(0, 1)
        next_left = last_poz + Vector(-1, 0)

        if self.is_possible_point(next_up):
            print str("next_up")


        # square_up = self.square(next_up)

        # next_left = (last_poz[0]-1, last_poz[1])
        # check up
        # check(next_up)

    # def check_square(self, center, next, a):
    #     to_check = next - center
    #     point = Vector(next.y +)



    def is_possible_point(self, l, h, r):
        # if pow(l, 2)
        x1 = r * cos(arcsin(h/r))
        p1 = Point(x1, h)

        x2 = r * cos(arcsin((h+1)/r))
        p2 = Point(x2, h)
        poly = self.square(Point(l, h))
        line = poly.boundary

        if (poly.within(p1) or line.contains(p1)):
            return True
        else:
            return False
        # math.pow()

    def square(self,  position):
        return [Vector(position.x, position.y), Vector(position.x, position.y + 1), Vector(position.x - 1, position.y), Vector(position.x - 1, position.y + 1)]

    def find_next_square(self, zero_poz, start_poz,  r):
        pow(r, 2) - pow()
        vec_act = zero_poz-start_poz
        for vec in self.four_square_starting(vec_act):
            square = self.square(vec)
            if not square[2].x < vec.x < square[0].x:
                continue
            if not square[4].y < vec.y < square[3].y:
                continue
            return square

    def four_square_starting(self, pos):
        return [pos+Vector(1, 0), pos+Vector(0, 1), pos+Vector(-1, 0), pos+Vector(0, -1)]

    def circle(self, center, r, a):
        y = 0
        x = 0
        list_vectors = list()

        while (y < r):
            x_sqr = pow(r, 2) - pow(y, 2)
            y_sqr = pow(r, 2) - pow(x, 2)

            p1 = Vector(center.x - math.sqrt(x_sqr), center.y + y)
            if p1 not in list_vectors:
                list_vectors.append(p1)

            p2 = Vector(center.x + math.sqrt(x_sqr), center.y + y)
            if p2 not in list_vectors:
                list_vectors.append(p2)

            p3 = Vector(center.x - math.sqrt(x_sqr), center.y - y)
            if p3 not in list_vectors:
                list_vectors.append(p3)

            p4 = Vector(center.x + math.sqrt(x_sqr), center.y - y)
            if p4 not in list_vectors:
                list_vectors.append(p4)

            p5 = Vector(center.x + x, center.y - math.sqrt(y_sqr))
            if p5 not in list_vectors:
                list_vectors.append(p5)

            p6 = Vector(center.x + x, center.y + math.sqrt(y_sqr))
            if p6 not in list_vectors:
                list_vectors.append(p6)

            p7 = Vector(center.x - x, center.y - math.sqrt(y_sqr))
            if p7 not in list_vectors:
                list_vectors.append(p7)

            p8 = Vector(center.x - x, center.y + math.sqrt(y_sqr))
            if p8 not in list_vectors:
                list_vectors.append(p8)

            y = y + a
            x = x + a

        # for vec in list_vectors:
        #     print (vec)

        return list_vectors

    def list_close(self, list_closed, list_to_close):
        if len(list_to_close) is 0:
            return list_closed

        print "list_closed: "
        for el in list_closed:
            print str(el)

        print "-------------"
        for element in list_to_close:
            vec1 = list_closed[0] - element
            vec2 = list_closed[-1] - element

            if vec1.magnitude() == 1:
                list_closed = list_closed + [element]
                list_to_close.remove(element)
                continue

            if vec2.magnitude() == 1:
                list_closed = [element] + list_closed
                list_to_close.remove(element)
                continue

        return self.list_close(list_closed, list_to_close)

    def find_right_corner(self, vec, a):
        xa = 0
        ya = 0
        # if vec.x % a > 0:
        #     xa = 1
        # if vec.y % a > 0:
        #     ya = 1
        return Vector(((math.floor(vec.x/a) + xa) * a), math.floor((vec.y/a) + ya) * a)

    def alignment(self, vec, a):
        if vec.x >= vec.y:
            next_vec = Vector(None, None)
            if vec.x % a == 0:
                next_vec.x = vec.x
            else:
                next_vec.x = (math.floor(vec.x / a) + 1) * a

            if vec.y % a == 0:
                next_vec.y = vec.y
            else:
                next_vec.y = (math.floor(vec.y / a)) * a

        elif vec.y >= vec.x:
            next_vec = Vector(None, None)
            if vec.y % a == 0:
                next_vec.y = vec.y
            else:
                next_vec.y = (math.floor(vec.y / a) + 1) * a

            if vec.x % a == 0:
                next_vec.x = vec.x
            else:
                next_vec.x = (math.floor(vec.x / a)) * a

            return next_vec
    def align(self, vec, a):
        aux_vec = Vector(vec.x/a, vec.y/a)
        next_vec = Vector(0,0)
        if aux_vec.x >= aux_vec.y:



    def make_square_poz(self, list_of_vectors, a):
        return [self.find_right_corner(vec, a) for vec in list_of_vectors]


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self.y = y

    def div_scalar(self, scalar):
        self.x = self.x / scalar
        self.y = self.y / scalar
        # , self.vec.y / scalar)

    def add_vector(self, vec):
        self.x = self.x + vec.x
        self.y = self.y + vec.y

    def normalize(self):
        m = self.magnitude()

        if m > 0:
            self.x = self.x / m
            self.y = self.y / m
        else:
            self.x = 0
            self.y = 0

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def mul_vector(self, vec):
        self.x = self.x * vec.x
        self.y = self.y * vec.y

    def mul_scalar(self, scalar):
        self.x = self.x * scalar
        self.y = self.y * scalar

    def invert(self):
        self.x = -self.x
        self.y = -self.y

    def sub_vector(self, vec):
        self.x = self.x - vec.x
        self.y = self.y - vec.y

    def limit(self, max):
        size = self.magnitude()

        if size is 0:
            return

        if size > max:
            self.x = self.x / size
            self.y = self.y / size

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def get_angle(self):
        return math.atan2(self.x, self.y)

    def sub2Vector(self, vec1, vec2):
        return Vector(vec1.x-vec2.x, vec1.y-vec2.y)

    def distance(self, vec):
        return math.sqrt(math.pow(vec.x-self.x, 2) + math.pow(vec.y-self.y, 2))

    def in_borders(self, border):
        if self.x < 0:
            return False
        elif self.y < 0:
            return False
        elif self.x > border.x:
            return False
        elif self.y > border.y:
            return False
        else:
            return True

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '[' + str(self.x) + ", " + str(self.y) + ']'

s = Simulation()
# s.circle(Vector(0, 0), 3, 0.5)
# print str(s.find_right_corner(Vector(3, -0.5), 3, 0.7))
lista = s.circle(Vector(0, 0), 3, 1)
# print s.find_right_corner(Vector(3, 0), 1)

list_to_close = s.make_square_poz(lista, 1)
list_first = [list_to_close[1]]
list_to_close.remove(list_to_close[1])
# print str(vec3)
#
#
list_a = [Vector(0, 1), Vector(0, 0), Vector(0, -1)]
list_b = [Vector(1, 0)]
# p = s.list_close(list_b, list_a)
p = s.list_close(list_first, list_to_close)

for el in p:
    print str(el)
# for vec in s.make_square_poz(lista, 1):
#     print str(vec)


#
# print str(s.find_next_square(Vector(0, 0), Vector(3, 0), 3))
# print s.is_possible_point(3, 0, 3)
# print s.is_possible_point(3, 1, 2)
# s.find_positions(3, 1)
# s.simulate()