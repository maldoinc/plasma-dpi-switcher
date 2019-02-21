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


def session_end():
    subprocess.call(["qdbus", "org.kde.ksmserver", "/KSMServer", "logout", "0", "0", "0"])


def kill():
    subprocess.call(['kquitapp5', 'plasmashell'])
