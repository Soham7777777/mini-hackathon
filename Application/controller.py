from flask import Blueprint, request, Response
from werkzeug import exceptions
from Application import db, models, get_expected_keys, ErrorMessage
from sqlalchemy.exc import IntegrityError
from icecream import ic

EmaiFieldErrors = ErrorMessage.EmailField

bp: Blueprint = Blueprint('User',__name__,url_prefix='/api')

@bp.route('/users',methods=('GET', 'POST'))
def getAll() -> Response:
    if request.method == 'GET':
        users = db.session.query(models.User).all()
        return [user.serialize() for user in users] # type: ignore
    
    name, email, password = get_expected_keys('name', 'email', 'password', json_request=request.get_json())
        
    try:
        newUser = models.User(name=name,email=email,password=password)
        db.session.add(newUser)
        db.session.commit()
    except IntegrityError as e:
        raise exceptions.BadRequest(EmaiFieldErrors.EXISTS.value.format(email=email))
    else:
        return Response(status=200)