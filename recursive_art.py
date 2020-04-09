"""
This program generates colorful, randomly generated computational art that is saved as
image files.

@author: Alana Huitric
"""

import random
import math
from collections.abc import Iterable
from PIL import Image

def prod(a,b):
    """ Returns product of a and b """
    return a*b

def avg(a,b):
    """ Returns average of a and b """
    return 0.5*(a+b)

def cos_pi(a):
    """ Returns cosine(a) """
    return math.cos(math.pi*a)

def sin_pi(a):
    """ Returns sine(a) """
    return math.sin(math.pi*a)

def x(a,b):
    """ Returns the first parameter """
    return a

def y(a,b):
    """ Returns the second parameter """
    return b

def square(a):
    """ Returns a squared """
    return a*a

def div(a,b):
    """ If possible, returns a divided by b, otherwise returns a """
    if b != 0:
        return a/b
    else:
        return a

def mult_random_factorial(a):
    """ Returns a multiplied by the factorial of a random number between 3 and 6 """
    i = random.randint(3,6)
    while i > 0:
        a *= i
        i-=1
    return a

def build_random_function(min_depth, max_depth):
    """Build a random function.
    Builds a random function of depth at least min_depth and depth at most
    max_depth.
    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
    Returns:
        The randomly generated function represented as a nested list.
    """
    rand = random.randint(1,9)
    f = []
    if max_depth >= 1:
        if min_depth >= 1:
            if rand == 1:
                f = ["prod", build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth - 1)]
            elif rand == 2:
                f = ["avg", build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth - 1)]
            elif rand == 3:
                f = ["cos_pi", build_random_function(min_depth - 1, max_depth - 1)]
            elif rand == 4:
                f = ["sin_pi", build_random_function(min_depth - 1, max_depth - 1)]
            elif rand == 5:
                f = ["x",build_random_function(min_depth - 1, max_depth - 1)]
            elif rand == 6:
                f = ["y", build_random_function(min_depth - 1, max_depth - 1)]
            elif rand == 7:
                f = ["square", build_random_function(min_depth - 1, max_depth - 1)]
            elif rand == 8:
                f = ["mult_random_factorial", build_random_function(min_depth - 1, max_depth - 1)]
            else:
                f = ["div", build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth - 1)]
        else:
            if random.randint(0,1) == 1:
                if random.randint(0,1) == 1:
                    return ["x"]
                else:
                    return ["y"]
    return f


def evaluate_random_function(f, x, y):
    """Evaluate the random function f with inputs x,y.
    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
    Returns:
        The function value
    Examples:
        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 'prod':
        fun = prod(evaluate_random_function(f[1], x, y),evaluate_random_function(f[2], x, y))
    elif f[0] == 'avg':
        fun = avg(evaluate_random_function(f[1], x, y),evaluate_random_function(f[2], x, y))
    elif f[0] == 'cos_pi':
        fun = cos_pi(evaluate_random_function(f[1], x, y))
    elif f[0] == 'sin_pi':
        fun = sin_pi(evaluate_random_function(f[1], x, y))
    elif f[0] == 'square':
        fun = square(evaluate_random_function(f[1], x, y))
    elif f[0] == 'mult_random_factorial':
        fun = mult_random_factorial(evaluate_random_function(f[1],x,y))
    else:
        fun = div(evaluate_random_function(f[1], x, y),evaluate_random_function(f[2], x, y))
    return fun


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.
    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
    Returns:
        The value remapped from the input to the output interval

    Examples:
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    p = (val-input_interval_start)/(input_interval_end - input_interval_start)
    n = p*(output_interval_end - output_interval_start) + output_interval_start
    return n


def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.
    Args:
        val: value to remap, must be a float in the interval [-1, 1]
    Returns:
        An integer in the interval [0,255]
    Examples:
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=500, y_size=500):
    """Generate a test image with random pixels and save as an image file.
    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=500, y_size=500):
    """Generates computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels
    red_function = build_random_function(25, 35)
    green_function = build_random_function(25, 35)
    blue_function = build_random_function(25, 35)
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
            )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
