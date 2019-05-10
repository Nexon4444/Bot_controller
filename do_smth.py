# from controller.robot import Control
#
#
# con = Control()
# con.calibrate()


from shapely.geometry import Point, Polygon

poly = Polygon([(3, 0), (2, 0), (2, 1), (3, 1)])
p = Point(3, 0)

x = poly.boundary
print str(x.contains(p))