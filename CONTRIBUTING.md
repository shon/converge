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

## Build / Release

```
python setup.py build sdist
bumpversion --dry-run --verbose patch  # or major, minor
bumpversion run patch  # or major, minor
twine upload dist/*
```
