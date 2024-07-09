from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from werkzeug import exceptions
from marshmallow import ValidationError, fields
import email_validator

class Base(MappedAsDataclass, DeclarativeBase):
    pass

db: SQLAlchemy = SQLAlchemy(model_class=Base)

def create_app(*,configClass: type) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(configClass())

    import Application.errorhandler as errhndl
    app.register_error_handler(exceptions.HTTPException, errhndl.jsonify_default_errors)
    app.register_error_handler(ValidationError, errhndl.handle_validation_errors)

    import Application.models
    db.init_app(app)
    with app.app_context():
        db.create_all()    

    from Application.controller import bp
    app.register_blueprint(bp)
    
    
    if app.testing:
        @app.route('/throw_error/<value>')
        def simulate_internal_server_error(value):
            if value == 'single':
                raise Exception('Single arg')
            elif value == 'multi':
                raise Exception(*('Multi arg'.split()))
            elif value == 'none':
                raise Exception()
            
    app.add_url_rule('/', endpoint='User.get_all')
    
    return app

# TODO: adding length support: flask-wtf type validation and processing
class CustomString(fields.String):
    def _serialize(self, value, attr, obj, **kwargs):
        return super()._serialize(value, attr, obj, **kwargs)
    
    def _deserialize(self, value, attr, data, **kwargs):
        if type(value) != str: raise ValidationError('The type must be string', attr)
        return value.strip()

class CustomEmail(CustomString):
    def _serialize(self, value, attr, obj, **kwargs):
        return super()._serialize(value, attr, obj, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        try:
            emailinfo = email_validator.validate_email(value)
            return emailinfo.normalized
        except email_validator.EmailNotValidError as e:
            raise ValidationError(str(e)) from e 