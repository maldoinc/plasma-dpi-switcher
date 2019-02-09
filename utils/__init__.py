import json
from collections import namedtuple

from Xlib import display
from Xlib.ext import randr


def output_list_names():
    s = display.Display().screen()
    window = s.root.create_window(0, 0, 1, 1, 1, s.root_depth)
    outputs = randr.get_screen_resources(window).outputs

    return [randr.get_output_info(window, o, 0).name for o in outputs]


def display_get_scaling_str(displays, scaling):
    return ";".join(["{0}={1}".format(d, scaling) for d in displays])


def get_font_dpi(scaling):
    return int(96 * scaling)


def read_profile(filename, name):
    params = json.load(open(filename, 'r'), object_hook=lambda d: namedtuple('Profile', d.keys())(*d.values()))

    for profile in params.profiles:
        if profile.name == name:
            return profile

    return None
