## Setup development environment

.. code:: bash

    git clone <converge-repo-url>
    cd converge

    python -m venv .venv
    source ./.venv/bin/activate

## Running tests

.. code:: bash

    pip install pytest
    pytest tests.py
