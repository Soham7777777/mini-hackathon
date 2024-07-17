from flask import Flask
from werkzeug import exceptions
from instance import IApplicationConfiguration

def create_app(config: IApplicationConfiguration, /) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    import Application.error_handlers as errhndl
    app.register_error_handler(exceptions.HTTPException, errhndl.jsonify_default_errors)
    app.register_error_handler(exceptions.NotFound, errhndl.handle_notfound_errors)
    
    @app.get('/')
    def home():
        return "Hello, World!"

    if app.testing:
        @app.get('/throw_error/<value>')
        def simulate_internal_server_error(value):
            if value == 'single':
                raise Exception('Single arg')
            elif value == 'multi':
                raise Exception(*('Multi arg'.split()))
            elif value == 'none':
                raise Exception()
        
        @app.get('/badrequest')
        def bad_request():
            raise exceptions.BadRequest("Testing BadRequest")
            
    return app