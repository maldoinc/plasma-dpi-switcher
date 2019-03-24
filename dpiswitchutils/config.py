import json
import os
from collections import namedtuple


def get_default_config_filename(env):
    f = os.path.join(env.get("XDG_CONFIG_HOME", "~/.config"), "maldoinc/dpiswitch/profile.json")

    return os.path.expanduser(f)


def load_config_file(filename):
    return json.load(open(filename, 'r'), object_hook=lambda d: namedtuple('Profile', d.keys())(*d.values()))


def save_config(c, filename):
    open(filename, 'w').write(json.dumps(c, indent=4))


def get_default_config():
    return {
        "version": "1.0",
        "profiles": []
    }


def generate_default_config(fn):
    os.makedirs(os.path.dirname(fn))
    open(fn, 'w').write(json.dumps(get_default_config(), indent=4))


def get_default_config_filename_assert_exists(env):
    """
    Returns the default config filename and generates it with default
    settings if it does not exist
    """
    fn = get_default_config_filename(env)

    if not os.path.exists(fn):
        generate_default_config(fn)

    return fn
