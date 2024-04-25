from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from werkzeug import exceptions
from typing import cast

def create_app(*,configClass: type) -> Flask:
    """Create WSGI application instance, apply given configuration. Initialize extensions and create database from models then register blueprints and a generic error handler to jsonify any defalut errors. Return app instance.

    Args:
        config (type): A class that represents app configurations. This class is instantiated and passed to Flask.config.from_object method.

    Returns:
        Flask: The WSGI application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(configClass())
    db.init_app(app)

    import Application.models as models
    with app.app_context():
        db.create_all()
    
    import Application.views as views
    app.register_blueprint(views.UserView.blueprint)
    
    @app.route('/')
    def home():
        return redirect(url_for('User.getAll'))
    
    # This will only capture all subclasses of HTTPException, which means that other errors will be caught by flask and generate default 500 Internal server error which results in HTTPException, the original error will be available via e.original_exception
    @app.errorhandler(exceptions.HTTPException)
    def jsonify_default_errors(e: exceptions.HTTPException):
        """Convert the default error pages to json with three fields: code, name and description. Use args as description, if InternalServerError is handled then description is set to original error's args if it exists. Code and name is set to error's default code and name. 

        Args:
            e (HTTPException): Error to handle 

        Returns:
            (data, code) (tuple): tuple of error as dictionary and HTTP status code 
        """
        code: int
        name: str
        description: str | list
        
        if issubclass(type(e), exceptions.InternalServerError):
            UnhandledException = cast(exceptions.InternalServerError, e)
            if UnhandledException.original_exception is not None and any(args:=UnhandledException.original_exception.args):
                description = args[0] if len(args)==1 else list(args)
            else:
                description = UnhandledException.description
            
            name = UnhandledException.name
            code = UnhandledException.code
                
            # the below is an example of arrogent programmer's bad code with same logic as above if-else
            # description = UnhandledException.description if UnhandledException.original_exception is None or not any(args:=UnhandledException.original_exception.args) else (args[0] if len(args)==1 else list(args))
        else:
            description = e.description # type: ignore            
            name = e.name
            code = e.code # type: ignore
                    
        data = dict(code=code, name=name, description=description)
        return data, code
    
    return app


class Base(MappedAsDataclass, DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)