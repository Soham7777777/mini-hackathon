from flask import Blueprint, request
from werkzeug import exceptions
from Application import db, CustomEmail, CustomString
from Application.models import User
from sqlalchemy.exc import IntegrityError
from icecream import ic
from marshmallow import Schema, fields, validates, ValidationError, pre_load, post_load
from enum import StrEnum



class UserSchema(Schema):
    name = CustomString(required=True)
    email = CustomEmail(required=True)
    password = CustomString(required=True)

    ## TODO: moving this to base schema
    @pre_load
    def preprocessor(self, data, **kwargs):
        if type(data) != dict : raise ValidationError('Object expected', 'schema')
        return data

    @post_load
    def postprocessor(self, data, **kwargs):
        return User(**data)

    @validates('name')
    def validate_name(self, value):
        if len(value) < 4 or len(value) > 30: raise ValidationError(UserSchema.NameFieldErrors.LENGTH.value)
        if value[0] in '1234567890_' : raise ValidationError(UserSchema.NameFieldErrors.STARTSWITH.value)
        for char in value:
            if not ((char.isalpha() and char.islower()) or (char in '1234567890_')): raise ValidationError(UserSchema.NameFieldErrors.CONTAIN.value)
    
    @validates('password')
    def validate_password(self, value):
        if len(value) < 8 or len(value) > 16 : raise ValidationError(UserSchema.PasswordFieldErrors.LENGTH.value)
        for char in value:
            if char.isspace() : raise ValidationError(UserSchema.PasswordFieldErrors.SPACE.value)
    
    class NameFieldErrors(StrEnum):
        LENGTH = 'Username must have minimum length of 4 and maximum of 30'
        STARTSWITH = 'Username cannot start with a digit or underscore'
        CONTAIN = 'Username can only contain lowercase characters or digits or underscores'

    class PasswordFieldErrors(StrEnum):
        LENGTH = 'Password must have minimum length of 8 and maximum of 16'
        SPACE = 'Password cannot contain any white space'

    class EmailFieldErrors(StrEnum):
        EXISTS = 'The email {email} already exists in database'



bp: Blueprint = Blueprint('User',__name__,url_prefix='/api')
schema = UserSchema()

@bp.get('/getAll')
def get_all():
    return schema.dump(db.session.query(User).all(), many=True)

@bp.post('/register')
def register():
    user = schema.load(request.get_json())
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        raise exceptions.BadRequest(UserSchema.EmailFieldErrors.EXISTS.value.format(email=user.email))
    else:
        return {}