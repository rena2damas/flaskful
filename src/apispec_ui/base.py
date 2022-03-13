from flask import Blueprint, MethodView


class SwaggerUIView(MethodView):
    """
    The /apidocs
    """

    def __init__(self, *args, **kwargs):
        view_args = kwargs.pop('view_args', {})
        self.config = view_args.get('config')
        super(APIDocsView, self).__init__(*args, **kwargs)

    def get(self):
        """
        The data under /apidocs
        json or Swagger UI
        """
        base_endpoint = self.config.get('endpoint', 'flasgger')
        specs = [
            {
                "url": url_for("swagger.ui"),
                "title": spec.get('title', 'API Spec 1'),
                "version": spec.get("version", '0.0.1'),
                "endpoint": spec.get("ui")
            }
        ]
        data = {
            "specs": specs,
            "title": self.config.get('title', 'Swagger')
            'flasgger_config': self.config,
            'json': json,
            'flasgger_version': __version__,
            'favicon': self.config.get(
                'favicon',
                url_for('swagger.static', filename='favicon-32x32.png')
            ),
            'swagger_ui_bundle_js': url_for(
                'swagger.static',
                filename='swagger-ui-bundle.js'
            ),
            'swagger_ui_standalone_preset_js': url_for(
                'swagger.static',
                filename='swagger-ui-standalone-preset.js'
            ),
            'jquery_js': url_for(
                'swagger.static',
                filename='lib/jquery.min.js'
            ),
            'swagger_ui_css': url_for(
                'swagger.static',
                filename='swagger-ui.css'
            )
        }
        return render_template(
            'swagger-ui/index.html',
            **data
        )


class Swagger:
    DEFAULT_CONFIG = {
        "headers": [],
        "apispecs": {
            "endpoint": 'specs',
            "route": '/swagger.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        },
        "swaggerui": True,
        "swaggerui_static": "/swaggerui_static",
        "swaggerui_route": "/swaggerui/"
    }

    def __init__(
            self,
            apispecs,
            app=None,
            config=None,
            merge=False
    ):
        self.apispecs = apispecs
        self._init_config(config, merge)
        if app:
            self.init_app(app)

    def _init_config(self, config, merge):
        if config and merge:
            self.config = dict(self.DEFAULT_CONFIG.copy(), **config)
        elif config and not merge:
            self.config = config
        elif not config:
            self.config = self.DEFAULT_CONFIG.copy()
        self.config.update(app.config.get('SWAGGER', {}))

    def init_app(self, app):
        self.app = app

        # self.load_apispec(app)
        self.register_swagger(app)
        self.add_headers(app)

        if self.parse:
            if RequestParser is None:
                raise RuntimeError('Please install flask_restful')
            self.parsers = {}
            self.schemas = {}
            self.parse_request(app)

        self._configured = True
        app.swag = self

    def register_views(self, app):
        """Register API ."""

        if self.config["swaggerui"]:
            blueprint = Blueprint(
                "swagger",
                __name__,
                url_prefix=self.config.get('url_prefix', None),
                template_folder="swagger-ui/templates",
                static_folder="swagger-ui/static",
                static_url_path=self.config.get('static_url_path', None)
            )

            blueprint.add_url_rule(
                rule=self.config["swaggerui_route"],
                endpoint='ui',
                view_func=wrap_view(SwaggerUIView().as_view(
                    name="swaggerui",
                    view_args=dict(config=self.config)
                ))
            )

        else:
            blueprint = Blueprint('swagger', __name__)

        for spec in self.config['specs']:
            self.endpoints.append(spec['endpoint'])
            blueprint.add_url_rule(
                spec['route'],
                spec['endpoint'],
                view_func=wrap_view(APISpecsView.as_view(
                    spec['endpoint'],
                    loader=partial(
                        self.get_apispecs, endpoint=spec['endpoint'])
                ))
            )

        app.register_blueprint(blueprint)
