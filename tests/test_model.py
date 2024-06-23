import pytest
from Application import ErrorMessage
from Application.models import User
from icecream import ic

NameFieldErrors = ErrorMessage.NameField
PasswordFieldErrors = ErrorMessage.PasswordField

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
    
    @staticmethod
    def testSerialization():
        original_user = dict(name='soham',email='sohamjobanputra7@gmail.com',password='12345678')
        user = User(**original_user).serialize()
        ic(user)
        assert type(user) == dict
        original_user['id'] = None
        assert original_user == user