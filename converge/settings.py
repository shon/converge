# Refer settings.rst for details
import importlib
import os
import sys


ns = locals()
get = ns.get

rc_filename = '.convergerc'
rc_config = {'APP_MODE': 'dev', 'SETTINGS_DIR': None}


def print_and_exit(msg):
    print('ERROR: ' + msg)
    sys.exit(1)


def extract_directive(line):
    try:
        key, value = (s.strip() for s in line.split('='))
        value = value[1:-1]
    except Exception as err:
        rc_path = os.path.abspath(rc_filename)
        print('ERROR: parsing line: ' + line)
        print_and_exit('failed to parse %s correctly: %s' % (rc_path, err))
    return key, value


def parse_rc():
    if os.path.isfile(rc_filename):
        supported_directives = tuple(rc_config.keys())
        lines = [line.strip() for line in open(rc_filename).readlines() if line.strip()]
        for directive in supported_directives:
            for line in lines:
                if directive in line:
                    key, value = extract_directive(line)
                    if directive == 'APP_MODE':
                        validate_mode(value)
                    rc_config[key] = value
    else:
        print('INFO: rc file not found: %s' % os.path.abspath(rc_filename))
    return rc_config


def import_settings(name, settings_dir=None, exit_on_err=False):
    name += '_settings'
    path = name + '.py'
    if settings_dir:
        path = os.path.join(settings_dir, path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        ns.update(dict((name, getattr(mod, name)) for name in dir(mod) if not name.startswith('_')))
        print('[INFO] successfully imported: %s' % name)
    except Exception as err:
        level = 'Error' if exit_on_err else 'Warning'
        print('[%s] Could not import "%s": %s' % (level, path, err))
        if exit_on_err:
            sys.exit(1)


if sys.version_info.major == 2:

    def import_settings(name, settings_dir=None, exit_on_err=False):
        name += '_settings'
        if settings_dir:
            name = '.'.join((settings_dir, name))
        try:
            mod = importlib.import_module(name)
            ns.update(dict((name, getattr(mod, name)) for name in dir(mod) if not name.startswith('_')))
            print('[INFO] successfully imported: %s' % name)
        except Exception as err:
            level = 'Error' if exit_on_err else 'Warning'
            print('[%s] Could not import "%s": %s' % (level, name, err))
            if exit_on_err:
                sys.exit(1)


def validate_mode(mode):
    supported_app_modes = ('prod', 'test', 'dev', 'staging')
    if mode not in supported_app_modes:
        print_and_exit('ERROR: unsupported mode: %s not in %s' % (mode, supported_app_modes))
    print('INFO: APP will run in [%s] mode' % mode)
    return mode


def main():
    parse_rc()
    for name in ('default', rc_config['APP_MODE'], 'site'):
        import_settings(name, rc_config['SETTINGS_DIR'])


def reload():
    main()

main()
