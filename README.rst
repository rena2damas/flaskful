**********
apispec-ui
**********

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: license: MIT

A library to generate a UI interface from an `APISpec <https://github
.com/marshmallow-code/apispec>`_ specification. As defined in the APISpec iniciative,
it currently supports `OpenAPI Specification <https://github
.com/OAI/OpenAPI-Specification>`_ (f.k.a. the Swagger specification).

Features
========

- Supports the OpenAPI Specification (versions 2 and 3)
- Currently supported frameworks include:

  - Flask

Installation
============

Install the package directly from ``PyPI`` (recommended):

.. code::

    pip install -U apispec-ui


Plugin dependencies like ``apispec`` and ``Flask`` are not installed with the package
by default. To have it installed, do like so:

.. code::

    pip install -U apispec-ui[apispec,Flask]

License
=======

MIT licensed. See `LICENSE <LICENSE>`_.
