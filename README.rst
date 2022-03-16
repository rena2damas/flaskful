**********
apispec-ui
**********

.. image:: https://img.shields.io/pypi/v/apispec-ui
    :target: https://pypi.org/project/apispec-ui
    :alt: PyPI version
.. image:: https://github.com/rena2damas/apispec-ui/actions/workflows/ci.yaml/badge.svg
    :target: https://github.com/rena2damas/apispec-ui/actions/workflows/ci.yaml
    :alt: CI
.. image:: https://codecov.io/gh/rena2damas/apispec-ui/branch/master/graph/badge.svg
    :target: https://app.codecov.io/gh/rena2damas/apispec-ui/branch/master
    :alt: codecov
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: code style: black
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: license: MIT

A library to generate a UI interface from an `APISpec <https://github
.com/marshmallow-code/apispec>`_ specification. As per the APISpec initiative, it
currently supports `OpenAPI Specification <https://github
.com/OAI/OpenAPI-Specification>`_ (aka. Swagger specification) and `SwaggerUI
<https://swagger.io/tools/swagger-ui/>`_.

Features
========

* Supports the OpenAPI Specification (versions 2 and 3)
* Supports SwaggerUI for Swagger specifications (latest version - 4.0.0)
* Currently supported frameworks include:

  * Flask


Installation
============

Install the package directly from ``PyPI`` (recommended):

.. code-block:: bash

    $ pip install -U apispec-ui


Plugin dependencies like ``apispec`` and ``Flask`` are not installed with the package
by default. To have it installed, do like so:

.. code-block:: bash

    $ pip install -U apispec-ui[apispec,Flask]

Example usage
=============

A simple example on how to work with a ``Flask`` application:

.. code-block:: python

    from apispec import APISpec
    from apispec.ext.marshmallow import MarshmallowPlugin
    from apispec_plugins import FlaskPlugin
    from apispec_ui.flask import Swagger
    from flask import Flask

    app = Flask(__name__)
    apispec = APISpec(
        title="Test API",
        version="0.1.0",
        openapi_version="3.0.3",
        plugins=(FlaskPlugin(), MarshmallowPlugin()),  # optional
    )
    ...
    Swagger(app=app, apispec=apispec, config={})

With this example, the application contains 2 extra views:

- ``swagger.ui``: endpoint to serve ``SwaggerUI``
- ``swagger.specs``: endpoint to serve ``swagger`` specs, in ``yaml``

With ``configs`` parameter one can tweak some parameters:

.. code-block:: python

    config = {
        "swaggerui": True,  # enable/disable SwaggerUI
        "swagger_route": "/api/",  # change swagger routes
        "swagger_static": "/static/",  # change location for static files
        "swagger_favicon": "favicon.ico",  # change favicon
        "swagger_hide_bar": True,  # hide SwaggerUI top bar
    }

These settings can also be configured through the ``SWAGGER`` config variable that is
part of the app config.

In terms of precedence, the config that takes the most precedence is the ``config``
parameter from ``Swagger`` class, followed by the ``SWAGGER`` app config.

Tests & linting
===============

Run tests with ``tox``:

.. code-block:: bash

    # ensure tox is installed
    $ tox

Run linter only:

.. code-block:: bash

    $ tox -e lint

Optionally, run coverage as well with:

.. code-block:: bash

    $ tox -e coverage

License
=======

MIT licensed. See `LICENSE <LICENSE>`_.
