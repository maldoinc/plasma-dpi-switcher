import configparser
import subprocess


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


def safe_read_ini(filename):
    contents = open(filename, 'r').read()

    if not contents.startswith('['):
        contents = '[__pytemp__]\n' + contents

    config_parser = configparser.RawConfigParser()
    config_parser.read_string(contents)

    return config_parser


def read_startup_script(filename):
    return dict(safe_read_ini(filename)['__pytemp__'])


def generate_startup_script(dst_filename, **kwargs):
    contents_startup = """! /bin/sh

    kcminputrc_mouse_cursortheme={kcminputrc_mouse_cursortheme}
    kcminputrc_mouse_cursorsize={kcminputrc_mouse_cursorsize}
    ksplashrc_ksplash_theme={ksplashrc_ksplash_theme}
    ksplashrc_ksplash_engine={ksplashrc_ksplash_engine}
    kdeglobals_kscreen_screenscalefactors='{kdeglobals_kscreen_screenscalefactors}'
    kcmfonts_general_forcefontdpi={kcmfonts_general_forcefontdpi}
    """.format(**kwargs)

    open(dst_filename, 'w').write(contents_startup)


def session_end():
    subprocess.call(["qdbus", "org.kde.ksmserver", "/KSMServer", "logout", "0", "0", "0"])


def kill():
    subprocess.call(['kquitapp5', 'plasmashell'])
