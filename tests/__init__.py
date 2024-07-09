from Application.controller import UserSchema

NameFieldErrors = UserSchema.NameFieldErrors
PasswordFieldErrors = UserSchema.PasswordFieldErrors

nameValidationTestCases: dict = {
    '       ' : NameFieldErrors.LENGTH.value,
    '       l  ' : NameFieldErrors.LENGTH.value,
    'xyz' : NameFieldErrors.LENGTH.value,
    'x'*31 : NameFieldErrors.LENGTH.value,
    'usernamewith$pecia|c@racter' : NameFieldErrors.CONTAIN.value,
    'contains\n\tcannotstrip' : NameFieldErrors.CONTAIN.value,
    '_private': NameFieldErrors.STARTSWITH.value,
    '1stprime': NameFieldErrors.STARTSWITH.value
}

passwordValidationTestCases: dict = {
    '' : PasswordFieldErrors.LENGTH.value,
    '    ' : PasswordFieldErrors.LENGTH.value,
    '   123   ' : PasswordFieldErrors.LENGTH.value,
    '12345678901234567' : PasswordFieldErrors.LENGTH.value,
    'contains space' : PasswordFieldErrors.SPACE.value
}