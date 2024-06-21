import pytest
from Application import EnumStore
from Application.models import User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

NameFieldErrors = EnumStore.NameField
PasswordFieldErrors = EnumStore.PasswordField

class TestUserModel:   
    @staticmethod
    def testNameValidation(nameTestCase):
        username, errorMessage = nameTestCase
        obj = dict(email='example123@gmail.com',password='12345678')
        obj['name'] = username
        with pytest.raises(User.ValidationError) as err:
            User(**obj)
        assert str(err.value) == errorMessage
    
        
    @staticmethod
    def testPasswordValidation(passwordTestCase):
        password, errorMessage = passwordTestCase
        obj = dict(email='example123@gmail.com', name='username123')
        obj['password'] = password
        with pytest.raises(User.ValidationError) as err:
            User(**obj)
        assert str(err.value) == errorMessage
    
    @staticmethod
    def testEmailValidationWorks():
        obj = dict(password='12345678', name='username123')
        obj['email'] = 'bad email @example.com'
        with pytest.raises(User.ValidationError):
            User(**obj)