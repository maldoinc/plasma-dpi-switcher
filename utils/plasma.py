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


def config_read(filename, group, key):
    safe_read_ini(filename).get(group, key)


def generate_startup_script(dst_filename, cursor_theme, screen_scale_factors,
                            font_dpi, cursor_size, ksplash_engine,
                            ksplash_theme):
    contents_startup = """! /bin/sh

    kcminputrc_mouse_cursortheme={cursor_theme}
    kcminputrc_mouse_cursorsize={cursor_size}
    ksplashrc_ksplash_theme={ksplash_theme}
    ksplashrc_ksplash_engine={ksplash_engine}
    kdeglobals_kscreen_screenscalefactors='{screen_scale_factors}'
    kcmfonts_general_forcefontdpi={font_dpi}
    """.format(cursor_theme=cursor_theme,
               screen_scale_factors=screen_scale_factors,
               font_dpi=font_dpi,
               cursor_size=cursor_size,
               ksplash_engine=ksplash_engine,
               ksplash_theme=ksplash_theme)

    open(dst_filename, 'w').write(contents_startup)


def session_end():
    subprocess.call(["qdbus", "org.kde.ksmserver",
                    "/KSMServer", "logout", "0", "0", "0"])


def kill():
    subprocess.call(['kquitapp5', 'plasmashell'])
