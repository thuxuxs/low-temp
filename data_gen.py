from pylab import *


def gen(shape):
    # num_point is the total number of points
    num_point = 2000
    t = array(range(num_point))

    # the wave is restricted in one period
    if shape == 'SIN':
        # SINe
        data = sin(2 * pi / num_point * t)

    if shape == 'SQU':
        # SQUare
        data = ones(num_point)
        data[int(num_point) / 2:] = -1.0

    if shape == 'RAMP':
        # RAMP
        data = linspace(0, 4, num_point)
        data[int(num_point / 4):] = 2 - data[int(num_point / 4):]
        data[int(3 * num_point / 4):] = -2 - data[int(3 * num_point / 4):]
    return data
