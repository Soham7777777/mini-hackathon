from Application import ErrorMessage

NameFieldErrors = ErrorMessage.NameField
PasswordFieldErrors = ErrorMessage.PasswordField

nameValidationTestCases: dict = {
    '  ' : NameFieldErrors.EMPTY.value,
    ' l' : NameFieldErrors.LENGTH.value,
    'xyz' : NameFieldErrors.LENGTH.value,
    'x'*31 : NameFieldErrors.LENGTH.value,
    'usernamewith$pecia|c@racter' : NameFieldErrors.CONTAIN.value,
    'contains\n\tcannotstrip' : NameFieldErrors.CONTAIN.value,
    '_private': NameFieldErrors.STARTSWITH.value,
    '1stprime': NameFieldErrors.STARTSWITH.value
}

passwordValidationTestCases: dict = {
    '' : PasswordFieldErrors.EMPTY,
    '  ' : PasswordFieldErrors.EMPTY,
    '123' : PasswordFieldErrors.LENGTH,
    '12345678901234567' : PasswordFieldErrors.LENGTH,
    'contains space' : PasswordFieldErrors.SPACE
}