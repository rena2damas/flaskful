from flask import Blueprint, jsonify, render_template, url_for
from flask.views import MethodView


class SwaggerUIView(MethodView):
    def __init__(self, *args, **kwargs):
        view_args = kwargs.pop("view_args", {})
        self.apispec = view_args.get("apispec")
        self.config = view_args.get("config")
        super().__init__(*args, **kwargs)

    def get(self):
        specs = self.apispec.to_dict()
        data = {
            "url": url_for("swagger.specs"),
            "title": specs["info"]["title"],
            "version": specs["info"]["version"],
            "description": specs["info"].get("description"),
            "favicon": self.config.get(
                "favicon", url_for("swagger.static", filename="favicon-32x32.png")
            ),
            **self.config,
        }
        return render_template("index.html", **data)


class SwaggerSpecsView(MethodView):
    def __init__(self, *args, **kwargs):
        view_args = kwargs.pop("view_args", {})
        self.apispec = view_args["apispec"]
        super().__init__(*args, **kwargs)

    def get(self):
        return jsonify(self.apispec.to_dict())


class Swagger:
    DEFAULT_CONFIG = {
        "swaggerui": True,
        "swagger_route": "/swagger/",
        "swagger_static": "/swagger_static/",
    }

    def __init__(self, apispec, app=None, config=None):
        self.apispec = apispec
        self.app = app
        self.config = config
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.init_config()
        self.register_swagger(app)

    def init_config(self):
        param_config = dict(**self.config or {})
        default_config = self.DEFAULT_CONFIG.copy()
        env_config = self.app.config.get("SWAGGER", {})
        self.config = default_config
        self.config.update(env_config)
        self.config.update(param_config)

    def register_swagger(self, app):
        if self.config["swaggerui"]:
            blueprint = Blueprint(
                "swagger",
                __name__,
                url_prefix=self.config.get("url_prefix", ""),
                template_folder="swagger-ui/",
                static_folder="swagger-ui/",
                static_url_path=self.config["swagger_static"],
            )

            blueprint.add_url_rule(
                rule=self.config["swagger_route"],
                endpoint="ui",
                view_func=SwaggerUIView().as_view(
                    name="swaggerui",
                    view_args={"config": self.config, "apispec": self.apispec},
                ),
            )

        else:
            blueprint = Blueprint("swagger", __name__)

        # add rule for swagger specs
        blueprint.add_url_rule(
            rule=f"{self.config['swagger_route']}/specs.json",
            view_func=SwaggerSpecsView.as_view(
                name="specs", view_args={"apispec": self.apispec}
            ),
        )

        app.register_blueprint(blueprint)
