import pytest

from apispec import APISpec
from flask import Flask, url_for

from apispec_ui.flask import Swagger


@pytest.fixture()
def app():
    app = Flask(__name__)
    with app.test_request_context():
        yield app


@pytest.fixture(scope="function", params=("2.0", "3.0.0"))
def spec(request):
    return APISpec(
        title="Test Suite",
        version="1.0.0",
        openapi_version=request.param,
        plugins=(),
    )


class TestFlask:

    def test_simple_app(self, app, spec):
        Swagger(
            app=app,
            apispec=spec,
            config={}
        )

        assert url_for("swagger.ui") == "/swagger/"
        assert url_for("swagger.specs") == "/swagger/specs.json"

    def test_lazy_init_app(self, app, spec):
        swagger = Swagger(
            apispec=spec,
            config={}
        )
        swagger.init_app(app)

        assert url_for("swagger.ui") == "/swagger/"
        assert url_for("swagger.specs") == "/swagger/specs.json"

