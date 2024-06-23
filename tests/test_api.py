from Application import ErrorMessage
from email_validator import validate_email, EmailNotValidError
from icecream import ic

NameFieldErros = ErrorMessage.NameField
PasswordFieldErrors = ErrorMessage.PasswordField

class TestAPI:
    @staticmethod
    def testGetAllRoute(client):
        inputUser = dict(name='soham', email='sohamjobanputra7@gmail.com', password='12345678')
        
        response = client.get('/', follow_redirects=True)
        assert response.request.path == '/api/users'
        
        response = client.post('http://127.0.0.1:5000/api/users', json=inputUser)
        assert response.status_code == 200
        
        response = client.get('http://127.0.0.1:5000/api/users')
        ic(response.json)
        assert response.status_code == 200

        assert len(response.json) == 1

        for key,val in inputUser.items():
            assert response.json[0][key] == val

        assert 'id' in response.json[0]
        assert type(response.json[0]['id']) == int
    
    
    @staticmethod
    def testNameErrors(nameTestCase: tuple[str,str], client):
        username, errorMessage = nameTestCase
        inputUser = dict(name=username, email='sohamjobanputra7@gmail.com', password='12345678')
        response = client.post('http://127.0.0.1:5000/api/users', json=inputUser)
        assert response.status_code == 400
        assert response.json['description'] == errorMessage
    
    
    @staticmethod
    def testPasswordErrors(passwordTestCase: tuple[str,str], client):
        password, errorMessage = passwordTestCase
        inputUser = dict(name='soham', email='sohamjobanputra7@gmail.com', password=password)   
        response = client.post('http://127.0.0.1:5000/api/users', json=inputUser)
        assert response.status_code == 400
        assert response.json['description'] == errorMessage
    
    
    @staticmethod
    def testEmailErrors(client):
        testEmail = "bad email@gmail.com"
        inputUser = dict(name='soham', email=testEmail, password='12345678')

        try:
            validate_email(testEmail,check_deliverability=False)
        except EmailNotValidError as e:
            expectedDescription = str(e)
            
        response = client.post('http://127.0.0.1:5000/api/users', json=inputUser)
        assert response.status_code == 400
        assert response.json['description'] == expectedDescription


    @staticmethod
    def testUniqueEmail(client):
        user1 = dict(name='xyz123', email='sameemail@gmail.com', password='12345678')
        user2 = dict(name='abc123', email='sameemail@gmail.com', password='aaaaaaaaa')
        client.post('/api/users', json=user1)
        response = client.post('/api/users', json=user2)
        assert response.status_code == 400
    
    
    @staticmethod
    def testKeyError(client):
        inputUser = dict(name='soham', email='sohamjobanputra7@gmail.com')
        response = client.post('/api/users', json=inputUser)
        assert response.status_code == 400
        assert response.json['description'] == ErrorMessage.General.REQUIRED.value.format(key='password')
    

    @staticmethod
    def testInternalServerError(client):
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