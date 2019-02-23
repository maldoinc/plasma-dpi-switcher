import configparser
import os
import subprocess

from utils import display_get_scaling_str, output_list_names, get_font_dpi

CONFIG_KDEGLOBALS = os.path.expanduser('~/.config/kdeglobals')
CONFIG_KCMFONTS = os.path.expanduser('~/.config/kcmfonts')
CONFIG_KCMINPUT = os.path.expanduser('~/.config/kcminputrc')
CONFIG_STARTUP = os.path.expanduser('~/.config/startupconfig')
CONFIG_SHELL = os.path.expanduser('~/.config/plasmashellrc')
CONFIG_APPLETS = os.path.expanduser('~/.config/plasma-org.kde.plasma.desktop-appletsrc')

SECTION_ROOT = 'root'


def config_write(filename, group, key, value):
    params = ['kwriteconfig5', '--file', filename, '--key', key]

    if isinstance(group, list):
        for g in group:
            params.append('--group')
            params.append(str(g))
    else:
        params.append('--group')
        params.append(str(group))

    params.append(str(value))

    subprocess.call(params)


def config_read(filename, group, key):
    params = ['kreadconfig5', '--file', filename, '--key', key]

    if isinstance(group, list):
        for g in group:
            params.append('--group')
            params.append(str(g))
    else:
        params.append('--group')
        params.append(str(group))

    try:
        return int(subprocess.check_output(params).splitlines()[0])
    except ValueError:
        return 0


def safe_read_ini(filename):
    contents = open(filename, 'r').read()

    if not contents.startswith('['):
        contents = '[{}]\n{}'.format(SECTION_ROOT, contents)

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
    config_write(CONFIG_KCMFONTS, "General", "forceFontDPI", get_font_dpi(profile.scaling))
    config_write(CONFIG_KCMINPUT, "Mouse", "cursorSize", profile.cursor.size)

    if os.path.isfile(CONFIG_STARTUP):
        os.remove(CONFIG_STARTUP)

    for panel in profile.panels:
        config_write(CONFIG_SHELL, panel.groups, "thickness", panel.thickness)

    for widget in profile.widgets:
        config_write(CONFIG_APPLETS, widget.groups, widget.key, widget.value)


def plasmashell_find_panel_groups():
    return[l.strip() for l in open(CONFIG_SHELL, 'r').readlines() if l.startswith('[PlasmaViews][Panel')]


def sections_to_array(sections):
    return sections[1:-1].split('][')


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
    conf = safe_read_ini(CONFIG_STARTUP)

    return {
        "scaling": int(conf.get(SECTION_ROOT, 'kcmfonts_general_forcefontdpi')) / 96,
        "cursor": {
            "size": conf.get(SECTION_ROOT, 'kcminputrc_mouse_cursorsize')
        },
        "panels": plasmashell_config_read_get_panel_info(),
        "widgets": {}
    }
