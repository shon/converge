# Refer settings.rst for details
import importlib
import importlib.util
import os
import sys
import tempfile

ns = locals()
get = ns.get

RC_FILENAME = ".convergerc"


def print_and_exit(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def run_command(cmd, ignore_failure=False):
    ret = os.system(cmd)
    if not ignore_failure and (ret != 0):
        print_and_exit(f"[{cmd}] exited with status {ret}")


def ensure_settings_dir(config):
    settings_dir = config["SETTINGS_DIR"]
    if not os.path.exists(settings_dir):
        raise Exception(f"SETTINGS_DIR: {repr(settings_dir)}: no such directory")


def parse_osenv(config):
    for directive in config:
        if directive in os.environ:
            config[directive] = os.environ[directive]

    return config


def import_settings(name, settings_dir=None, exit_on_err=False):
    name += "_settings"
    path = name + ".py"
    if settings_dir:
        path = os.path.join(settings_dir, path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        ns.update(
            dict(
                (name, getattr(mod, name))
                for name in dir(mod)
                if not name.startswith("_")
            )
        )
        print(f"[INFO] successfully imported: {name}")
    except Exception as err:
        level = "Error" if exit_on_err else "Warning"
        print(f'[level] Could not import "{path}": {err}')
        if exit_on_err:
            sys.exit(1)


def validate_mode(mode):
    supported_app_modes = ("prod", "test", "dev", "staging", "beta")
    if mode not in supported_app_modes:
        print_and_exit(f"ERROR: unsupported mode: {mode} not in {supported_app_modes}")
    print(f"INFO: APP will run in [{mode}] mode")
    return mode


def clone_git_repo(git_url, settings_dir, git_subdir=None):

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_cmd = f"git clone {git_url} {temp_dir}"
        src_dir = os.path.join(temp_dir, git_subdir) if git_subdir else temp_dir
        cp_cmd = f"cp -rvf {src_dir}/*_settings.py {settings_dir}"

        run_command(clone_cmd)
        run_command(cp_cmd)


def get_config():
    config_default = {
        "APP_MODE": "dev",
        "SETTINGS_DIR": "settings",
        "GIT_SETTINGS_REPO": None,
        "GIT_SETTINGS_SUBDIR": None,
    }
    return parse_osenv(config_default)


def fail_on_rc_file():
    if os.path.exists(RC_FILENAME):
        raise Exception(
            f"{repr(RC_FILENAME)} has been deprecated, use environment variables instead."
        )


def main():

    fail_on_rc_file()

    config = get_config()
    settings_dir = config["SETTINGS_DIR"]
    git_url = config["GIT_SETTINGS_REPO"]
    git_subdir = config["GIT_SETTINGS_SUBDIR"]
    ensure_settings_dir(config)

    if config["GIT_SETTINGS_REPO"]:
        if not os.path.exists(settings_dir):
            print(f"Creating directory: {settings_dir}")
            os.mkdir(settings_dir)
        clone_git_repo(git_url, settings_dir, git_subdir)

    ns["APP_MODE"] = config["APP_MODE"]
    for name in ("default", config["APP_MODE"], "site"):
        import_settings(name, settings_dir)


def reload():
    main()


main()
