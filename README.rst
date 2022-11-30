.. contents::
.. sectnum::


What is it?
-----------

If you are a Python developer who likes to keep application configuration in simple Python modules and that your app have some default settings and production/dev/test setting files, **converge** can help you merge settings and start the application with desired settings based on environment variables.


Getting started
----------------

Easy to use
~~~~~~~~~~~~

.. code:: bash

    ./settings/default_settings.py
    -------------------
    SERVER_PORT = 8000
    DOMAIN = 'example.com'
    ADMIN_EMAIL = 'admin@example.com'

    ./settings/dev_settings.py
    ---------------
    SERVER_PORT = 9000


.. code:: python

    import settings
    print(settings.SERVER_PORT)  # 9000
    print(settings.DOMAIN)  # example.com
    print(settings.get('VAR_THAT_DOESNT_EXIST'))  # None


Install
~~~~~~~

.. code:: bash

    pip install converge

Supported environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_All directives are optional._

**APP_MODE**

Valid values are

- dev (default)
- test
- staging
- beta
- prod

Based on ``mode`` appropriate settings module would be used (if available)

**SETTINGS_DIR**

Defaults to "settings".

If your settings files are in different directory, use SETTINGS_DIR to point converge to correct path.

.. note:: Remember to drop __init__.py in settings directory.


**GIT_SETTINGS_REPO**

Fetching application settings from a git repository is supported too. If such configuration is specified, git repository is cloned into `SETTINGS_DIR`.

**GIT_SETTINGS_SUBDIR**

In case you 
- use same git repository to host configurations of more than one applications and
- say settings files are in different subdirectories

Example

::

  my-git-repo/
    |
    |- myapp1
    |    |
    |    |- default_settings.py
    |    |- prod_settings.py
    |
    |
    |- myapp2

::

    export SETTINGS_DIR='appsettings'
    export GIT_SETTINGS_REPO='git@github.com:shon/converge-test-settings.git'
    export GIT_SETTINGS_SUBDIR='myapp1'

In this case all \*_settings.py files in myapp1/ would be copied to appsettings.


**Example**

::

    export APP_MODE='test'
    export SETTINGS_DIR='settings'
    export GIT_SETTINGS_REPO='git@github.com:shon/converge-test-settings.git'
    export GIT_SETTINGS_SUBDIR='myapp1'


Supported settings files
-------------------------

-  Defaults: default_settings.py

-  Mode
    - production: prod_settings.py
    - development: dev_settings.py
    - test: test_settings.py
    - staging: staging_settings.py
    - beta: beta_settings.py

- Deployment specific: site_settings.py


Guidelines
-----------

Settings files are usual Python files that can contain valid python code however here are some guidelines for user

- Use module variables for global application wide configuration
- Use UPPERCASE while naming settings variables
- For values prefer basic python datatypes such as string, integer,
  tuples
- eg. ``SERVER_PORT = 1234``
- Avoid complex python operations
- Use simple classes for config sections
    .. code:: python

        class DB:
            HOST = 'db.example.com'
            PORT = 1234

-  Use simple string operations to avoid repetition
    .. code:: python

        BASE_DOMAIN = 'example.com'
        API_URL = 'api.' + BASE_DOMAIN``

Overriding settings
-------------------

Defining module veriables in site_settings.py

Example
~~~~~~~

**default_settings.py**

``SERVER_PORT = 9999``

**site_settings.py**

``SERVER_PORT = 8888``

Overriding partial settings
---------------------------

Example:

**default_settings.py**

.. code:: python

    class DB:
        HOST = 'db.example.com'
        PORT = 1234

**site_settings.py**

.. code:: python

    DB.PORT = 1111

(Slightly) Advanced usage
---------------------------
In case if you want to keep all settings.py files in a directory. Use `SETTINGS_DIR` environment variable.

Using SETTINGS_DIR
~~~~~~~~~~~~~~~~~~


.. code:: bash

    export APP_MODE='prod'
    export SETTINGS_DIR='settings/fat_server'

This is useful when you have to deploy multiple instances of an app with different configs

::

    `-- settings/
         |
         |-- server1/
         |      |
         |      |--default_settings.py
         |      |--prod_settings.py
         |
         |-- server2/
         |      |--default_settings.py
         |      |--prod_settings.py
         |
         |
