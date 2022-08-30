.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
.. image:: https://img.shields.io/pypi/v/pyhubctl.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/pyhubctl/
.. image:: https://img.shields.io/coveralls/github/DuraTech-Industries/pyhubctl/main.svg
    :alt: Coveralls
    :target: https://coveralls.io/r/DuraTech-Industries/pyhubctl


========
PyHubCtl
========


    Python wrapper for the uhubctl project.


===========
Quick Start
===========

Installation
------------

`pyhubctl` requires `uhubctl` to be installed and on PATH for your system. Follow the guide provided
by `uhubctl` here: https://github.com/mvp/uhubctl#compiling

Attempts to run this library without proper installation of `uhubctl` will result in errors being
thrown.

Install from PyPI::

    pip install pyhubctl

Install from source::

    git clone https://github.com/DuraTech-Industries/pyhubctl.git
    cd pyhubctl
    pip install .


Quick Start
-----------

`pyhubctl` has two main classes for use: `PyHubCtl` and `Configuration`. They're both pretty
self-explanatory, but `PyHubCtl` is what you use to run `uhubctl`, and `Configuration` is what you
use to configure how `uhubctl` runs.

`Configuration` contains attributes that correspond directly to the arguments `uhubctl` expects.
Pass an instance of this class to the run method of `PyHubCtl`. This run method will return what
`uhubctl` outputs, or raise an error if something went wrong.

As an example, here is how you might toggle all of the ports on a USB-hub::

    from pyhubctl import Configuration, PyHubCtl

    phc = PyHubCtl()
    phc.run(Configuration(location="1-4"))

Or a specific set of ports::

    from pyhubctl import Configuration, PyHubCtl

    phc = PyHubCtl()
    phc.run(Configuration(location="1-4", ports="3,4"))


Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd pyhubctl
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

.. _pre-commit: https://pre-commit.com/
