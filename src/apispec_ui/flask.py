from flask import Blueprint, jsonify, render_template, url_for
from flask.views import MethodView


class SwaggerUIView(MethodView):

    def __init__(self, *args, **kwargs):
        view_args = kwargs.pop('view_args', {})
        self.config = view_args.get('config')
        self.apispecs = view_args.get('apispecs')
        super(SwaggerUIView, self).__init__(*args, **kwargs)

    def get(self):
        specs = self.apispecs.to_dict()
        data = {
            "url": url_for("swagger.specs"),
            "title": specs["info"]["title"],
            "version": specs["info"]["version"],
            "description": specs["info"]["description"],
            "favicon": self.config.get(
                'favicon',
                url_for('swagger.static', filename='favicon-32x32.png')
            ),
            **self.config
        }
        return render_template("index.html", **data)


class SwaggerSpecsView(MethodView):

    def __init__(self, *args, **kwargs):
        view_args = kwargs.pop('view_args', {})
        self.apispecs = view_args['apispecs']
        super(SwaggerSpecsView, self).__init__(*args, **kwargs)

    def get(self):
        return jsonify(self.apispecs.to_dict())


class Swagger:
    DEFAULT_CONFIG = {
        "swaggerui": True,
        "swagger_static": "/swagger_static/",
        "swagger_route": "/swagger/"
    }

    def __init__(
            self,
            apispecs,
            app=None,
            config=None
    ):
        self.apispecs = apispecs
        self.app = app
        default_config = self.DEFAULT_CONFIG.copy()
        self.config = dict(default_config, **config) if config else default_config
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        # use SWAGGER as environment variable for configs
        self.config.update(app.config.get('SWAGGER', {}))

        self.register_swagger(app)

    def register_swagger(self, app):
        if self.config["swaggerui"]:
            blueprint = Blueprint(
                "swagger",
                __name__,
                url_prefix=self.config.get('url_prefix', ""),
                template_folder="swagger-ui/",
                static_folder="swagger-ui/",
                static_url_path=self.config["swagger_static"]
            )

            blueprint.add_url_rule(
                rule=self.config["swagger_route"],
                endpoint='ui',
                view_func=SwaggerUIView().as_view(
                    name="swaggerui",
                    view_args=dict(config=self.config, apispecs=self.apispecs)
                )
            )

        else:
            blueprint = Blueprint('swagger', __name__)

        # add rule for swagger specs
        blueprint.add_url_rule(
            rule=f"{self.config['swagger_route']}/specs.json",
            view_func=SwaggerSpecsView.as_view(
                name="specs",
                view_args=dict(apispecs=self.apispecs)
            )
        )

        app.register_blueprint(blueprint)
