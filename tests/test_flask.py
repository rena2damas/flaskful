import pytest

from apispec import APISpec
from flask import Flask, url_for

from apispec_ui.flask import Swagger


@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    with app.test_request_context():
        yield app


@pytest.fixture(scope="class", params=("2.0", "3.0.0"))
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
        client = app.test_client()

        assert url_for("swagger.ui") == "/swagger/"
        assert url_for("swagger.specs") == "/swagger/specs.json"
        assert client.get(url_for("swagger.specs")).json == spec.to_dict()

    def test_lazy_init_app(self, spec):
        app = Flask(__name__)
        swagger = Swagger(
            apispec=spec,
            config={}
        )
        swagger.init_app(app)

        with app.test_request_context():
            assert url_for("swagger.ui") == "/swagger/"
            assert url_for("swagger.specs") == "/swagger/specs.json"

