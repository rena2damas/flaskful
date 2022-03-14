from flask import Blueprint, MethodView


class SwaggerUIView(MethodView):

    def __init__(self, *args, **kwargs):
        view_args = kwargs.pop('view_args', {})
        self.config = view_args.get('config')
        self.apispec = view_args.get('apispec')
        super(SwaggerUIView, self).__init__(*args, **kwargs)

    def get(self):
        apispec = self.apispec
        data = {
            "url": url_for("swagger.ui"),
            "title": apispec["info"]["title"],
            "version": apispec["info"]["version"],
            "description": apispec["info"]["description"],
            'favicon': self.config.get(
                'favicon',
                url_for('swagger.static', filename='favicon-32x32.png')
            )
        }
        return render_template(
            'swagger-ui/index.html',
            **data
        )


class Swagger:
    DEFAULT_CONFIG = {
        "headers": [],
        "apispec": {
            "endpoint": 'apispec',
            "route": '/specs.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        },
        "swaggerui": True,
        "swaggerui_static": "/swaggerui_static",
        "swaggerui_route": "/swaggerui/"
    }

    def __init__(
            self,
            apispec,
            app=None,
            config=None,
            merge=False
    ):
        self.apispec = apispec
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

    def register_swaggerui(self, app):
        if self.config["swaggerui"]:
            blueprint = Blueprint(
                "swagger",
                __name__,
                url_prefix=self.config.get('url_prefix', None)
            )

            blueprint.add_url_rule(
                rule=self.config["swaggerui_route"],
                endpoint='ui',
                view_func=SwaggerUIView().as_view(
                    name="swaggerui",
                    view_args=dict(config=self.config, apispec=self.apispec)
                )
            )

        else:
            blueprint = Blueprint('swagger', __name__)

        apispec = self.config.apispec
        blueprint.add_url_rule(
            rule=apispec['route'],
            endpoint=apispec['endpoint'],
            view_func=wrap_view(APISpecsView.as_view(
                name=apispec['endpoint'],
                view_args=self.apispec
            ))
        )

        app.register_blueprint(blueprint)
