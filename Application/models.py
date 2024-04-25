from Application import db
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Annotated
from enum import StrEnum
from email_validator import validate_email, EmailNotValidError
from .views import UserView

Fields = UserView.Attribute

class User(db.Model): # type: ignore
    """A declarative mapped class represting the user model for sqlalchemy ORM.

    Fields:
        id: primary key for database, not needed for instantiating model class
        name: username within 4 to 30 characters containing lowercase characters or digits or underscores. username cannot start with a digit or underscore
        email: unique email
        password: password within 8 to 16 characters containing no spaces
    
    Methods:
        validator: validates the input data
    
    Classes:
        ExceptionStatements: A collection of StrEnum that represents appropriate exception messages 
    """
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[Annotated[str, 30]]
    email: Mapped[Annotated[str, 320]] = mapped_column(unique=True)
    password: Mapped[Annotated[str,16]]
    
    @validates(Fields.NAME,Fields.EMAIL,Fields.PASSWORD)
    def validator(self, key: str, value: str):
        # we can also put marshmellow logic here and add schema classes inside the User class
        # if the mapped class contais a lot of fields then we can create a dictionary of "field : validator" and call the appropriate validator for given field, we can directly use marshmellow as well
        ex = User.ExceptionStatements
        if key == Fields.NAME:
            value = value.strip()
            if value == '' : raise ValueError(ex.NameField.EMPTY)
            if len(value) < 4 or len(value) > 30: raise ValueError(ex.NameField.LENGTH)
            if value[0] in '1234567890_' : raise ValueError(ex.NameField.STARTSWITH)
            for char in value:
                if not ((char.isalpha() and char.islower()) or (char in '1234567890_')): raise ValueError(ex.NameField.CONTAIN)

        elif key == Fields.EMAIL:
            try:
                emailinfo = validate_email(value, check_deliverability=False)
                value = emailinfo.normalized
            except EmailNotValidError:
                raise ValueError(str(EmailNotValidError))

        elif key == Fields.PASSWORD:
            # we can use the third parth module named password-validator for strong password checking 
            value = value.strip()
            if value == '' : raise ValueError(ex.PasswordField.EMPTY)
            if len(value) < 8 or len(value) > 16 : raise ValueError(ex.PasswordField.LENGTH)
            for char in value:
                if char.isspace() : raise ValueError(ex.PasswordField.SPACE)      
                     
        return value
    
    class ExceptionStatements:
        class NameField(StrEnum):
            EMPTY = 'Username cannot be empty string'
            LENGTH = 'Username must have minimum length of 4 and maximum of 30'
            STARTSWITH = 'Username cannot start with a digit or underscore'
            CONTAIN = 'Username can only contain lowercase characters or digits or underscores'
        
        class PasswordField(StrEnum):
            EMPTY = 'Password cannot be empty string'
            LENGTH = 'Password must have minimum length of 8 and maximum of 16'
            SPACE = 'Password cannot contain any white space'