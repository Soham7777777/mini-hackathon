from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from werkzeug import exceptions
from enum import StrEnum

class Base(MappedAsDataclass, DeclarativeBase):
    def serialize(self) -> dict:
        table = self.__table__
        result = {}
        for col in table.columns:
            col_name = str(col).split('.')[-1]
            result[col_name] = getattr(self, col_name)
        # return json.dumps(result, default=str) # for stringification
        return result

db: SQLAlchemy = SQLAlchemy(model_class=Base)

def create_app(*,configClass: type) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(configClass())

    import Application.errorhandler as errhndl
    import Application.models as models
    app.register_error_handler(exceptions.HTTPException, errhndl.jsonify_default_errors)
    app.register_error_handler(models.User.ValidationError, errhndl.handle_validation_errors)

    db.init_app(app)
    with app.app_context():
        db.create_all()    

    from Application.controller import bp
    app.register_blueprint(bp)
    
    @app.route('/')
    def home():
        return redirect(url_for('User.getAll'))
    
    if app.testing:
        @app.route('/throw_error/<value>')
        def simulate_internal_server_error(value):
            if value == 'single':
                raise Exception('Single arg')
            elif value == 'multi':
                raise Exception(*('Multi arg'.split()))
            elif value == 'none':
                raise Exception()

    
    return app


class ErrorMessage:
    class General(StrEnum):
        REQUIRED = 'The key {key} is required'

    class NameField(StrEnum):
        EMPTY = 'Username cannot be empty string'
        LENGTH = 'Username must have minimum length of 4 and maximum of 30'
        STARTSWITH = 'Username cannot start with a digit or underscore'
        CONTAIN = 'Username can only contain lowercase characters or digits or underscores'
    
    class PasswordField(StrEnum):
        EMPTY = 'Password cannot be empty string'
        LENGTH = 'Password must have minimum length of 8 and maximum of 16'
        SPACE = 'Password cannot contain any white space'
    
    class EmailField(StrEnum):
        EXISTS = 'The email {email} already exists in database'


def get_expected_keys(*keys: str, json_request = {}) -> list[str]:
    vals = []
    for key in keys:
        try:
            vals.append(json_request[key])
        except KeyError:
            raise exceptions.BadRequest(ErrorMessage.General.REQUIRED.value.format(key=key))
    return vals if len(vals) > 1 else vals[0]

