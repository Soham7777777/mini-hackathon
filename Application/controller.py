from flask import Blueprint, request, jsonify, Response
from werkzeug import exceptions
from Application import db, models, get_expected_keys, EnumStore
from sqlalchemy.exc import IntegrityError

EmaiFieldErrors = EnumStore.EmailField

bp: Blueprint = Blueprint('User',__name__,url_prefix='/api')

@bp.route('/users',methods=('GET', 'POST'))
def getAll() -> Response:
    if request.method == 'GET':
        users = db.session.query(models.User).all()
        return jsonify(users)
    
    name, email, password = get_expected_keys('name', 'email', 'password', json_request=request.json)
        
    try:
        newUser = models.User(name=name,email=email,password=password)
        db.session.add(newUser)
        db.session.commit()
    except IntegrityError as e:
        raise exceptions.BadRequest(EmaiFieldErrors.EXISTS.value.format(email=email))
    else:
        return Response(status=200)