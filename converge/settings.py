# Refer settings.rst for details
import importlib
import importlib.util
import os
import sys
import tempfile


ns = locals()
get = ns.get

RC_FILENAME = '.convergerc'


def print_and_exit(msg):
    print('ERROR: ' + msg)
    sys.exit(1)


def run_command(cmd, ignore_failure=False):
    ret = os.system(cmd)
    if not ignore_failure and (ret != 0):
        print_and_exit('[%s] exited with status %s' % (cmd, ret))


def extract_directive(line):
    try:
        key, value = (s.strip() for s in line.split('='))
        value = value[1:-1]
    except Exception as err:
        rc_path = os.path.abspath(RC_FILENAME)
        print('ERROR: parsing line: ' + line)
        print_and_exit('failed to parse %s correctly: %s' % (rc_path, err))
    return key, value


def parse_rc(rc_config):
    if os.path.isfile(RC_FILENAME):
        supported_directives = tuple(rc_config.keys())
        lines = [line.strip()
                 for line in open(RC_FILENAME).readlines()
                 if line.strip()]
        for directive in supported_directives:
            for line in lines:
                if directive in line:
                    key, value = extract_directive(line)
                    if directive == 'APP_MODE':
                        validate_mode(value)
                        ns['APP_MODE'] = value
                    rc_config[key] = value
    else:
        print('INFO: rc file not found: %s' % os.path.abspath(RC_FILENAME))
    return rc_config


def parse_osenv(rc_config):
    for directive in rc_config:
        if directive in os.environ:
            rc_config[directive] = os.environ[directive]


def import_settings(name, settings_dir=None, exit_on_err=False):
    name += '_settings'
    path = name + '.py'
    if settings_dir:
        path = os.path.join(settings_dir, path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        ns.update(dict((name, getattr(mod, name))
                  for name in dir(mod) if not name.startswith('_')))
        print('[INFO] successfully imported: %s' % name)
    except Exception as err:
        level = 'Error' if exit_on_err else 'Warning'
        print('[%s] Could not import "%s": %s' % (level, path, err))
        if exit_on_err:
            sys.exit(1)


def validate_mode(mode):
    supported_app_modes = ('prod', 'test', 'dev', 'staging', 'beta')
    if mode not in supported_app_modes:
        print_and_exit('ERROR: unsupported mode: %s not in %s' %
                       (mode, supported_app_modes))
    print('INFO: APP will run in [%s] mode' % mode)
    return mode


def clone_git_repo(git_url, settings_dir, git_subdir=None):

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_cmd = 'git clone %s %s' % (git_url, temp_dir)
        src_dir = os.path.join(temp_dir, git_subdir) if git_subdir \
            else temp_dir
        cp_cmd = 'cp -rvf %s/*_settings.py %s' % (src_dir, settings_dir)

        run_command(clone_cmd)
        run_command(cp_cmd)


def get_rc_config():
    rc_config_default = {'APP_MODE': 'dev',
                         'SETTINGS_DIR': None,
                         'GIT_SETTINGS_REPO': None,
                         'GIT_SETTINGS_SUBDIR': None}
    rc_config = parse_osenv(rc_config_default)
    rc_config = parse_rc(rc_config_default)
    return rc_config


def main():
    rc_config = get_rc_config()
    settings_dir = rc_config['SETTINGS_DIR']
    git_url = rc_config['GIT_SETTINGS_REPO']
    git_subdir = rc_config['GIT_SETTINGS_SUBDIR']

    if rc_config['GIT_SETTINGS_REPO']:
        if not os.path.exists(settings_dir):
            print('Creating directory: %s' % settings_dir)
            os.mkdir(settings_dir)
        clone_git_repo(git_url, settings_dir, git_subdir)

    for name in ('default', rc_config['APP_MODE'], 'site'):
        import_settings(name, settings_dir)


def reload():
    main()


main()
