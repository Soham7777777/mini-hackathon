import pytest
from Application.controller import schema
from icecream import ic
from marshmallow import ValidationError


def test_name(nameTestCase):
    username, errorMessage = nameTestCase
    obj = dict(email='example123@gmail.com',password='12345678')
    obj['name'] = username
    with pytest.raises(ValidationError) as err:
        schema.load(obj)
    assert err.value.messages['name'][0] == errorMessage

def test_password(passwordTestCase):
    password, errorMessage = passwordTestCase
    obj = dict(email='example123@gmail.com', name='username123')
    obj['password'] = password
    with pytest.raises(ValidationError) as err:
        schema.load(obj)
    assert err.value.messages['password'][0] == errorMessage

def test_custom_email_fields():
    normalized_form = "sohamjobanputra7@gmail.com"
    obj = dict(name="soham", email="   sohamjobanputra7@GMAIL.com  ", password='12346789')
    dumped = schema.dump(schema.load(obj))
    assert dumped['email'] == normalized_form
    with pytest.raises(ValidationError) as err:
        obj['email'] = 'bad email@gmail.com'
        schema.load(obj)
    
def test_schema():
    with pytest.raises(ValidationError) as err:
        obj = ['dsf', 'sfsfs', 'sdfsdf']
        schema.load(obj)
    errors = err.value.messages['schema'] == 'Object expected'

