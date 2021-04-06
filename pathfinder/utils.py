"""This module contains various utility functions"""
import functools
import time

from numpy import average

from .constants import GRID_X, GRID_Y, OFFSET, XGR, YGR


def logger(fn):
    """decorator name to log method calls from classes"""

    @functools.wraps(fn)
    def func(class_obj, *args, **kwargs):
        """logs method calls from classes"""
        print(f'{class_obj.__class__.__name__}.{fn.__name__} was run with "{args}" args and {kwargs} kwargs')
        return fn(class_obj, *args, **kwargs)

    return func


times = []


def timer(fn):
    """decorator name to log method calls from classes"""

    @functools.wraps(fn)
    def func(class_obj, *args, **kwargs):
        """logs method calls from classes"""

        start = time.perf_counter()
        result = fn(class_obj, *args, **kwargs)
        end = time.perf_counter()
        print(f'{fn.__name__} was run in {round(end - start, 6)} seconds')
        times.append(round(end - start, 6))
        print('Average:', average(times))
        return result

    return func


def cache(fn):
    """decorator to cache inputs to functions"""
    _cache = []
    _results = []

    @functools.wraps(fn)
    def func(*args):
        """cache stuff"""
        if len(_cache) > 1000:
            _cache.clear()
            _results.clear()
        if args not in _cache:
            result = fn(*args)
            _cache.append(args)
            _results.append(result)
        else:
            return _results[_cache.index(args)]

        return result

    return func


def constrain(val, min_val, max_val) -> int:
    """keeps val in the range of min_val and max_val"""
    return min(max_val, max(min_val, val))


def remap(x, in_min, in_max, out_min, out_max) -> int:
    """Given an input range and output range, maps the value x to the output range.
        eg x=3, in_min=0, in_max=10, out_min=0, out_max=100 returns 30.
        Answer will always be truncated.
    """
    return constrain((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min, 0, out_max - 1)


def get_node_pos(node, mouse):
    """API to remap the value of mouse to an index tuple to access the correct grid member"""
    cur_node_x = remap(mouse[0], OFFSET, node.grid[XGR].x + node.grid[XGR].width, 0, GRID_X)
    cur_node_y = remap(mouse[1], OFFSET, node.grid[YGR].y + node.grid[YGR].height, 0, GRID_Y)
    return cur_node_x, cur_node_y
