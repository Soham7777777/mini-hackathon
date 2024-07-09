from Application.controller import UserSchema
from email_validator import validate_email
from icecream import ic
from Application.models import User

NameFieldErros = UserSchema.NameFieldErrors
PasswordFieldErrors = UserSchema.PasswordFieldErrors


inputUser = dict(name='soham', email='sohamjobanputra7@gmail.com', password='12345678')
schema = UserSchema()

def test_integration(client, database):
    res = client.get('/')
    assert res.status_code == 200
    assert res.json == []

    res = client.post('/api/register', json=inputUser)
    assert res.status_code == 200
    res = client.get('/')
    assert len(res.json) == 1
    assert res.json[0] == inputUser

    users = schema.dump(database.session.query(User).all(), many=True)
    assert len(users) == 1
    assert users[0] == inputUser

    res = client.post('/api/register', json=inputUser)
    assert res.status_code == 400
    assert res.json['description'] == UserSchema.EmailFieldErrors.EXISTS.value.format(email=inputUser['email'])

def test_validation_error_handler(client):
    badUser = dict(**inputUser)
    badUser['name'] = ['sdf', ['sdf']]
    res = client.post('/api/register', json=badUser)
    assert res.status_code == 422
    ic(res.json)
    assert res.json['description']['name'][0] == 'The type must be string'

def test_InternalServerError(client):
    response = client.get('/throw_error/single')
    assert response.status_code == 500
    assert len(response.json) == 1
    assert response.json['description'] == 'Single arg'

    response = client.get('/throw_error/multi')
    assert response.status_code == 500
    assert len(response.json) == 1
    assert response.json['description'] == 'Multi arg'.split()

    description = (
    "The server encountered an internal error and was unable to"
    " complete your request. Either the server is overloaded or"
    " there is an error in the application."
    )

    response = client.get('/throw_error/none')
    assert response.status_code == 500
    assert len(response.json) == 1
    assert response.json['description'] == ''.join(description)