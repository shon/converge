.. contents::
.. sectnum::


Getting started
----------------

Setup
~~~~~

.. code:: bash

    pip install converge


Usage example
~~~~~~~~~~~~~

.. code:: bash

    echo 'SERVER_PORT = 8000' > default_settings.py
    echo 'SERVER_PORT = 9000' > dev_settings.py
    echo 'SERVER_PORT = 80' > prod_settings.py

Python

.. code:: python

    from converge import settings
    print(settings.SERVER_PORT)

    settings.get('VAR_THAT_DOESNT_EXIST')  # returns None


Guidelines
-----------

Settings files are usual Python files that can contain valid python code however here are some guidelines for user

- Use module variables for global application wide configuration
- Use UPPERCASE while naming settings variables
- For values prefer basic python datatypes usch as string, integer,
  tuples
- eg. ``SERVER_PORT = 1234``
- Avoid logic
- Use simple classes for config sections
    .. code:: python

        class DB:
            HOST = 'db.example.com'
            PORT = 1234

-  Use simple string operations to avoid repeatation
    .. code:: python

        BASE_DOMAIN = 'example.com'
        API_URL = 'api.' + BASE_DOMAIN``

Supported settings files
-------------------------

-  Defaults: default_settings.py
-  Mode
    - Production: prod_settings.py
    - Development: dev_settings.py
    - Test: test_settings.py
    - Staging: staging_settings.py
- Deployment specific: site_settings.py

Setting mode
------------

Create a file .convergerc. This file supports a directive **APP_MODE**

Valid values are

- prod
- dev
- test 
- staging

Based on ``mode`` appropriate settings module would be used (if available)

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

For Contributors
----------------

Running tests
~~~~~~~~~~~~~

.. code:: bash

    git clone <repo>
    cd converge
    nosetests -xv tests.py
