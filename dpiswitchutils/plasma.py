import configparser
import os
import subprocess

from .utils import display_get_scaling_str, output_list_names, scale_factor_to_font_dpi

CONFIG_KDEGLOBALS = os.path.expanduser('~/.config/kdeglobals')
CONFIG_KCMFONTS = os.path.expanduser('~/.config/kcmfonts')
CONFIG_KCMINPUT = os.path.expanduser('~/.config/kcminputrc')
CONFIG_SHELL = os.path.expanduser('~/.config/plasmashellrc')
CONFIG_APPLETS = os.path.expanduser('~/.config/plasma-org.kde.plasma.desktop-appletsrc')


def kconfig_generate_groups_params(group):
    if group is None:
        return []

    if isinstance(group, list):
        params = []

        for g in group:
            params.append('--group')
            params.append(str(g))

        return params

    return ['--group', str(group)]


def config_write_get_params(filename, group, key, value):
    params = ['kwriteconfig5', '--file', filename, '--key', key]
    params.extend(kconfig_generate_groups_params(group))
    params.append(str(value))

    return params


def config_write(filename, group, key, value):
    subprocess.call(config_write_get_params(filename, group, key, value))


def config_read_get_params(filename, group, key):
    params = ['kreadconfig5', '--file', filename, '--key', key]
    params.extend(kconfig_generate_groups_params(group))

    return params


def config_read(filename, group, key):
    try:
        return int(subprocess.check_output(config_read_get_params(filename, group, key)).splitlines()[0])
    except ValueError:
        return 0


def safe_read_ini(filename):
    contents = open(filename, 'r').read()

    # not fool-proof as the config may start with empty lines or comments
    # but for our purposes seems to work well enough as these files are not edited by hand
    if not contents.startswith('['):
        contents = '[__ROOT__]\n{}'.format(contents)

    config_parser = configparser.RawConfigParser()
    config_parser.read_string(contents)

    return config_parser


def session_end():
    subprocess.call(["qdbus", "org.kde.ksmserver", "/KSMServer", "logout", "0", "0", "0"])


def shell_kill():
    subprocess.call(['kquitapp5', 'plasmashell'])


def apply_profile(profile):
    scale_factors = display_get_scaling_str(output_list_names(), profile.scaling)

    shell_kill()

    config_write(CONFIG_KDEGLOBALS, "KScreen", "ScaleFactor", profile.scaling)
    config_write(CONFIG_KDEGLOBALS, "KScreen", "ScreenScaleFactors", scale_factors)
    config_write(CONFIG_KCMFONTS, "General", "forceFontDPI", scale_factor_to_font_dpi(profile.scaling))
    config_write(CONFIG_KCMINPUT, "Mouse", "cursorSize", profile.cursor.size)

    for panel in profile.panels:
        config_write(CONFIG_SHELL, panel.groups, "thickness", panel.thickness)

    for widget in profile.widgets:
        config_write(CONFIG_APPLETS, widget.groups, widget.key, widget.value)


def plasmashell_find_panel_groups():
    return[l.strip() for l in open(CONFIG_SHELL, 'r').readlines() if l.startswith('[PlasmaViews][Panel')]


def sections_to_array(sections):
    if isinstance(sections, str) and sections.startswith('[') and sections.endswith(']'):
        return sections[1:-1].split('][')

    raise Exception("'{}' does not contain any sections".format(sections))


def plasmashell_config_read_get_panel_info():
    panels = plasmashell_find_panel_groups()
    res = []

    for p in panels:
        groups = sections_to_array(p)

        res.append({
            "groups": groups,
            "thickness": config_read(CONFIG_SHELL, groups, 'thickness')
        })

    return res


def read_current_profile():
    return {
        "scaling": safe_read_ini(CONFIG_KDEGLOBALS).getfloat('KScreen', 'ScaleFactor', fallback=1),
        "cursor": {
            "size": safe_read_ini(CONFIG_KCMINPUT).getint('Mouse', 'cursorSize', fallback=24)
        },
        "panels": plasmashell_config_read_get_panel_info(),
        "widgets": []
    }
