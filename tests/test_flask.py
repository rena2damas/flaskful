import pytest

from apispec import APISpec
from flask import Flask, url_for
from werkzeug.routing import BuildError

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
        assert "text/html" in client.get(url_for("swagger.ui")).headers["content-type"]
        assert "application/json" in client.get(url_for("swagger.specs")).headers[
            "content-type"]

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

    def test_custom_configs(self, app, spec):
        Swagger(
            app=app,
            apispec=spec,
            config={
                "swaggerui": True,
                "swagger_static": "/test_static/",
                "swagger_route": "/test/docs/"
            }
        )

        assert url_for("swagger.ui") == "/test/docs/"
        assert url_for("swagger.specs") == "/test/docs/specs.json"

    def test_no_swagger_ui(self, app, spec):
        Swagger(
            app=app,
            apispec=spec,
            config={"swaggerui": False}
        )

        assert url_for("swagger.specs") == "/swagger/specs.json"
        with pytest.raises(BuildError):
            url_for("swagger.ui")
