import os
import glob
import importlib
import shutil

from converge import settings

settings_dir = 'fortest'
default_config = {'config': 'default'}
dev_config = {'config': 'dev'}
prod_config = {'config': 'prod'}
site_config = {'config': 'site'}


def create_config_lines(config):
    lines = []
    for kv in config.items():
        lines.append('%s = "%s"' % kv)
    return lines


def create_config_file(path, config):
    f = open(path, 'w')
    f.writelines(create_config_lines(config))
    f.flush()
    os.fsync(f)
    f.close()


def test_no_settings_dir():
    assert settings.get('config') is None, settings.get('config')
    create_config_file('default_settings.py', default_config)
    settings.reload()
    assert settings.get('config') == 'default', settings.get('config')


def test_rc():
    rc_lines = [('SETTINGS_DIR = "%s"\n' % settings_dir), 'APP_MODE = "dev"\n']
    f = open('.convergerc', 'w')
    f.writelines(rc_lines)
    f.flush()
    os.fsync(f)
    f.close()
    import time
    time.sleep(1)

    os.mkdir(settings_dir)
    open(os.path.join(settings_dir, '__init__.py'), 'w').close()

    config_path = os.path.join(settings_dir, 'default_settings.py')
    create_config_file(config_path, default_config)
    settings.reload()
    assert settings.config == 'default'

    config_path = os.path.join(settings_dir, 'dev_settings.py')
    create_config_file(config_path, dev_config)
    settings.reload()
    assert settings.config == 'dev'

    config_path = os.path.join(settings_dir, 'prod_settings.py')
    create_config_file(config_path, prod_config)
    settings.reload()
    assert settings.config == 'dev'

    config_path = os.path.join(settings_dir, 'site_settings.py')
    create_config_file(config_path, site_config)
    settings.reload()
    assert settings.config == 'site'


def teardown_module():
    py_path = 'default_settings.py'
    pyc_path = py_path + 'c'
    for path in (py_path, pyc_path):
        if os.path.exists(path):
            os.remove(path)
    if glob.glob(os.path.join(settings_dir, '__init__.py')):  # playing safe
        shutil.rmtree(settings_dir)
    if os.path.exists('.convergerc'):
        os.remove('.convergerc')
