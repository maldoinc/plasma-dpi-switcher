import json
import sys
from collections import namedtuple
from json.decoder import JSONDecodeError

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


def load_config_file(filename):
    return json.load(open(filename, 'r'), object_hook=lambda d: namedtuple('Profile', d.keys())(*d.values()))


def find_profile(config, name):
    for profile in config.profiles:
        if profile.name == name:
            return profile

    return None


def load_profile(filename, profilename):
    try:
        config = load_config_file(filename)
        profile = find_profile(config, profilename)

        if profile is None:
            print("[ERR] Unable to find profile '{}'".format(profilename))

        return profile
    except JSONDecodeError as e:
        print("[ERR] [JSON Decode error] Unable to parse configuration file! {}".format(e), file=sys.stderr)
        return False
    except OSError as e:
        print("[ERR] [OS Error] {}".format(e), file=sys.stderr)
        return False
