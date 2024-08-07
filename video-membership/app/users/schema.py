from pydantic import BaseModel, EmailStr, SecretStr, field_validator, model_validator, root_validator
from .models import User
from . import auth


class UserSignUpSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr

    @field_validator('password_confirm')
    def passwords_match(cls, v, values):
        if v != values.data.get('password'):
            raise ValueError('Passwords do not match')
        return v

    @field_validator('email')
    def email_match(cls, v):
        q = User.objects.filter(email=v)
        if q.count() > 0:
            raise ValueError('Email is not available')
        return v


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    session_id: str = None

    # @model_validator(mode='before')
    @root_validator(skip_on_failure=True)
    def validate_user(cls, values):
        err_msg = "Incorrect Credentials, please try again."
        email = values.get('email') or None
        password = values.get('password') or None
        print(email, password)
        if email is None or password is None:
            raise ValueError(err_msg)
        password = password.get_secret_value()
        user = auth.authenticate(email, password)
        if user is None:
            raise ValueError(err_msg)
        token = auth.login(user)
        return {'session_id': token}
