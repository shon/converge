.. contents::
.. sectnum::


What is it?
-----------

If you are a Python developer who likes to keep application configuration in simple Python modules and that your app have some default settings and production/dev/test setting files, **converge** can help you merge settings and load desired application settings.


Getting started
----------------

Easy to use
~~~~~~~~~~~~

.. code:: bash

    default_settings.py
    -------------------
    SERVER_PORT = 8000
    DOMAIN = 'example.com'
    ADMIN_EMAIL = 'admin@example.com'

    dev_settings.py
    ---------------
    SERVER_PORT = 9000

    
.. code:: python

    from converge import settings
    print(settings.SERVER_PORT)  # 9000
    print(settings.DOMAIN)  # example.com
    print(settings.get('VAR_THAT_DOESNT_EXIST'))  # None


Install
~~~~~~~

.. code:: bash

    pip install converge

.convergerc
------------

.convergerc file helps converge choose application mode and in turn load correct settings file. 

Supported directives
~~~~~~~~~~~~~~~~~~~~

**APP_MODE**

Valid values are

- prod
- dev
- test 
- staging

Based on ``mode`` appropriate settings module would be used (if available)

**SETTINGS_DIR**

If your settings files are in different directory, use SETTINGS_DIR to point converge to correct path.
You can also provide url in below format to fetch settings from git.

Pattern:  remote_repo_url#branch_name#settings_directory

Example
~~~~~~~

``SETTINGS_DIR = https://github.com/xxxxx/xxxxx.git#xxxxx#xxxxx``


.. note:: Remember to drop __init__.py in settings directory.

**Example**

::

    .convergerc
    -----------

    APP_MODE = 'test'
    SETTINGS_DIR = 'appsettings'

Supported settings files
-------------------------

-  Defaults: default_settings.py

-  Mode
    - production: prod_settings.py
    - development: dev_settings.py
    - test: test_settings.py
    - staging: staging_settings.py

- Deployment specific: site_settings.py


Guidelines
-----------

Settings files are usual Python files that can contain valid python code however here are some guidelines for user

- Use module variables for global application wide configuration
- Use UPPERCASE while naming settings variables
- For values prefer basic python datatypes usch as string, integer,
  tuples
- eg. ``SERVER_PORT = 1234``
- Avoid complex python operations
- Use simple classes for config sections
    .. code:: python

        class DB:
            HOST = 'db.example.com'
            PORT = 1234

-  Use simple string operations to avoid repeatation
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
In case if you want to keep all settings.py files in a directory. Use `SETTINGS_DIR` directive in .convergerc file.

Example
~~~~~~~


.. code:: bash
    
    >> cat .convergerc
    
    APP_MODE = 'prod'
    SETTINGS_DIR = 'settings/fat_server'

This is useful when you have to deply multiple instances of an app with different configs

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


For Contributors
----------------

Running tests
~~~~~~~~~~~~~

.. code:: bash

    git clone <repo>
    cd converge
    nosetests -xv tests.py
