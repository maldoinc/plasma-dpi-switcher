import json

from Xlib import display
from Xlib.ext import randr

from dpiswitchutils.config import save_config
from dpiswitchutils.exceptions import ProfileNotFoundException


def output_list_names():
    s = display.Display().screen()
    window = s.root.create_window(0, 0, 1, 1, 1, s.root_depth)
    outputs = randr.get_screen_resources(window).outputs

    return [randr.get_output_info(window, o, 0).name for o in outputs]


def display_get_scaling_str(displays, scaling):
    return ";".join(["{0}={1}".format(d, scaling) for d in displays])


def scale_factor_to_font_dpi(scaling):
    return int(96 * scaling)


def font_dpi_to_scale_factor(dpi):
    if dpi == 0:
        return 1

    return dpi / 96


def find_profile(config, name):
    for profile in config.profiles:
        if profile.name == name:
            return profile

    raise ProfileNotFoundException("Unable to find profile {}".format(name))


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

    save_config(c, filename)


def profile_remove(profile, filename):
    c = json.load(open(filename, 'r'))
    c["profiles"] = [p for p in c["profiles"] if p["name"] != profile]

    save_config(c, filename)


def try_parse_int(val, default=None):
    try:
        return int(val)
    except ValueError:
        return default
