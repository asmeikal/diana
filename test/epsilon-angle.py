from math import radians, degrees, cos, sin, acos, asin, sqrt, pi

def sgn(x):
    if x < 0:
        return -1
    return 1

def sgn_quad(x):
    if abs(x) < pi/2:
        return 1
    return -1

def convert(func):
    '''Converts function arguments to radians
    and the function return to degrees'''
    def inner(*args):
        a,b,dist = args
        a = radians(a)
        b = radians(b)
        d,z,b1,a1 = func(a,b,dist)
        return degrees(d), z, degrees(a1), degrees(b1)
    return inner

def prettyprinter(func):
    def inner(*args):
        # print args
        angle, radius, new_a, new_b = func(*args)
        # print 'Radius = {0:.2f}'.format(radius)
        print 'Epsilon = {0:.2f}'.format(angle)
        print 'New alpha = {0:.2f}'.format(new_a)
        print 'New beta = {0:.2f}'.format(new_b)
        print
        return new_a, new_b
    return inner

@prettyprinter
@convert
def epsilon_analysis(a,b,dist):
    if abs(b) == pi/2:
        a = 0
    x = sin(b) * dist
    y = cos(b) * dist * sin(a)
    radius = sqrt(x**2 + y**2)
    def epsilon():
        if a == 0 or b == 0:
            return b
        elif abs(a) == pi/2:
            return pi/2 * sgn(b)
        return asin(x/radius)
    def epsilon_increase():
        _d = epsilon() + radians(1) * sgn(a)
        _c = 1
        if abs(_d) >= pi/2:
            _d = abs(pi - abs(_d)) * sgn(_d)
            _c = -1
        _x = (radius * sin(_d))/dist
        if _x > -1.0:
            _new_b = asin((radius * sin(_d))/dist)
        else:
            _new_b = -pi/2
        _c2 = _c
        if abs(_new_b) >= pi/2:
            _c2 *= -1
        if a not in (-pi,0,pi):
            _new_a = (asin((cos(_d)*radius)/(cos(_new_b)*dist))*sgn(a))*_c*sgn(a)
        else:
            _new_a = a
        if _c2 < 0:
            _new_a = abs(pi - abs(_new_a)) * (-sgn(_new_a))
        return _new_b, _new_a, _d
    new_a, new_b, _epsilon = epsilon_increase()
    return _epsilon, radius, new_a, new_b

a,b = 45, 0

for _ in range(360):
    a, b = epsilon_analysis(a, b, 100)