import glob
import os
import shutil
from unittest.mock import patch

import pytest

import settings

settings_dir = "fortest/server1"
default_config = {"config": "default"}
dev_config = {"config": "dev"}
prod_config = {"config": "prod"}
site_config = {"config": "site"}
repo_dir = "/tmp/settings-repo"
git_settings_subdir = repo_dir + "/myapp1"


def setup_module():
    cmds = [
        "mkdir -p %s" % git_settings_subdir,
        "git init %s" % repo_dir,
        'echo "PROD = True" > %s/prod_settings.py' % git_settings_subdir,
        'echo "PROD = False" > %s/dev_settings.py' % git_settings_subdir,
    ]
    for cmd in cmds:
        ret = os.system(cmd)
        if ret != 0:
            raise Exception("failed: %s" % cmd)


def create_config_lines(config):
    lines = []
    for kv in config.items():
        lines.append('%s = "%s"' % kv)
    return lines


def create_config_file(path, config):
    open(path, 'w').writelines(create_config_lines(config))


def test_no_settings_dir():
    settings_file = "settings/default_settings.py"
    try:
        assert settings.get("config") is None, settings.get("config")
        create_config_file(settings_file, default_config)
        settings.reload()
        assert settings.get("config") == "default", settings.get("config")
    finally:
        os.remove(settings_file)


@patch.dict(os.environ, {"SETTINGS_DIR": settings_dir, "APP_MODE": "dev"}, clear=True)
def test_rc():

    os.makedirs(settings_dir)
    open(os.path.join(settings_dir, "__init__.py"), "w").close()
    open(os.path.join(settings_dir, "../", "__init__.py"), "w").close()

    config_path = os.path.join(settings_dir, "default_settings.py")
    create_config_file(config_path, default_config)
    settings.reload()
    assert settings.config == "default"

    config_path = os.path.join(settings_dir, "dev_settings.py")
    create_config_file(config_path, dev_config)
    settings.reload()
    assert settings.config == "dev"

    config_path = os.path.join(settings_dir, "prod_settings.py")
    create_config_file(config_path, prod_config)
    settings.reload()
    assert settings.config == "dev"

    config_path = os.path.join(settings_dir, "site_settings.py")
    create_config_file(config_path, site_config)
    settings.reload()
    assert settings.config == "site"


def test_backward_compatibility():
    from converge import settings


def test_env_vars():
    config = {"SETTINGS_DIR": "settings"}

    os.environ["SETTINGS_DIR"] = "settings/site1"
    settings.parse_osenv(config)
    assert config["SETTINGS_DIR"] == os.environ["SETTINGS_DIR"]

    os.environ["SETTINGS_DIR"] = "settings/site2"
    settings.parse_osenv(config)
    assert config["SETTINGS_DIR"] == os.environ["SETTINGS_DIR"]


@patch.dict(
    os.environ,
    {
        "SETTINGS_DIR": settings_dir,
        "APP_MODE": "prod",
        "GIT_SETTINGS_REPO": repo_dir,
        "GIT_SETTINGS_SUBDIR": git_settings_subdir,
        "PATH": os.environ["PATH"],
    },
    clear=True,
)
def test_git_settings():
    settings.reload()
    assert settings.PROD is True


def test_rc_file_deprecated():

    convergerc = ".convergerc"
    open(convergerc, "w").write("")

    try:
        with pytest.raises(Exception):
            settings.reload()
    finally:
        os.remove(convergerc)

def test_ensure_settings_dir():
    shutil.rmtree(settings_dir)

    with pytest.raises(Exception, match="no such directory"):
        settings.reload()



def teardown_module():
    py_path = "default_settings.py"
    pyc_path = py_path + "c"
    for path in (py_path, pyc_path):
        if os.path.exists(path):
            os.remove(path)
    if glob.glob(os.path.join(settings_dir, "__init__.py")):  # playing safe
        shutil.rmtree(settings_dir)
    if repo_dir.startswith("/tmp"):  # playing safe
        shutil.rmtree(repo_dir)

