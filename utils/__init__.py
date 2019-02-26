import json
import os
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


def get_default_config_filename(env):
    f = os.path.join(env.get("XDG_CONFIG_HOME", "~/.config"), "maldoinc/dpiswitch/profile.json")

    return os.path.expanduser(f)


def load_config_file(filename):
    return json.load(open(filename, 'r'), object_hook=lambda d: namedtuple('Profile', d.keys())(*d.values()))


def find_profile(config, name):
    for profile in config.profiles:
        if profile.name == name:
            return profile

    raise Exception("Unable to find profile {}".format(name))


def prompt_for_profile(config):
    print("DPISWITCH - Available profiles\n")
    print(" #  {:15} {}".format("Name", "Description"))

    for index, profile in enumerate(config.profiles):
        print("[{}] {:15} {}".format(index + 1, profile.name, profile.description))
    print()

    index = int(input("Choose a profile number: ")) - 1

    return config.profiles[index].name


def profile_save_to_file(profile, filename):
    c = json.load(open(filename, 'r'))
    c["profiles"].append(profile)

    open(filename, 'w').write(json.dumps(c))
