# Refer settings.rst for details
import sys
import importlib


ns = locals()
get = ns.get


def import_settings(name, exit_on_err=False):
    global ns
    name += '_settings'
    try:
        mod = importlib.import_module(name)
        ns.update(dict((name, getattr(mod, name)) for name in dir(mod) if not name.startswith('_')))
    except ImportError as err:
        level = 'Error' if exit_on_err else 'Warning'
        print('[%s] Could not import "%s": %s' % (level, name, err))
        if exit_on_err:
            sys.exit(1)


def detect_mode():
    try:
        mode = open('.app_mode').read().strip().upper()
        if mode not in ('PROD', 'TEST', 'DEV', 'STAGING'):
            print('ERROR: unsupported mode: %s' % mode)
            sys.exit(1)
    except Exception as err:
        print('Warning: Could not read .app_mode')
        mode = 'DEV'
    print('INFO: APP will run in [%s] mode' % mode)
    return mode.lower()


import_settings('default')
import_settings(detect_mode())
import_settings('site')
