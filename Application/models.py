from Application import db, EnumStore
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Annotated, Type
from email_validator import validate_email, EmailNotValidError

NameFieldErrors = EnumStore.NameField
PasswordFieldErrors = EnumStore.PasswordField


class User(db.Model): # type: ignore
    class ValidationError(Exception):
        pass

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[Annotated[str, 30]]
    email: Mapped[Annotated[str, 320]] = mapped_column(unique=True)
    password: Mapped[Annotated[str,16]]
    
    @validates('name', 'email', 'password')
    def validator(self, key: str, value: str):
        if key == 'name':
            value = value.strip()
            if value == '' : raise User.ValidationError(NameFieldErrors.EMPTY.value)
            if len(value) < 4 or len(value) > 30: raise User.ValidationError(NameFieldErrors.LENGTH.value)
            if value[0] in '1234567890_' : raise User.ValidationError(NameFieldErrors.STARTSWITH.value)
            for char in value:
                if not ((char.isalpha() and char.islower()) or (char in '1234567890_')): raise User.ValidationError(NameFieldErrors.CONTAIN.value)

        elif key == 'email':
            try:
                emailinfo = validate_email(value, check_deliverability=False)
                value = emailinfo.normalized
            except EmailNotValidError as e:
                raise User.ValidationError(str(e))  

        elif key == 'password':
            value = value.strip()
            if value == '' : raise User.ValidationError(PasswordFieldErrors.EMPTY.value)
            if len(value) < 8 or len(value) > 16 : raise User.ValidationError(PasswordFieldErrors.LENGTH.value)
            for char in value:
                if char.isspace() : raise User.ValidationError(PasswordFieldErrors.SPACE.value)      
                     
        return value
    
    