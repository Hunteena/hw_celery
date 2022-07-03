import pydantic

from db_models import Session, UserModel
from errors import HTTPError


class CreateUserValidator(pydantic.BaseModel):
    email: str
    password: str

    @pydantic.validator('email')
    def valid_email(cls, value):
        if '@' not in value:
            raise ValueError('email is not valid')
        name, domain = str(value).rsplit('@')
        if len(name) == 0 or len(domain) < 3 or '.' not in domain:
            raise ValueError('email is not valid')
        return value

    @pydantic.validator('email')
    def new_email(cls, value):
        with Session() as session:
            user = (
                session.query(UserModel).filter(
                    UserModel.email == value
                ).first()
            )
            if user is not None:
                raise HTTPError(401, f'user with email {value} already exists')
        return value

    @pydantic.validator('password')
    def strong_password(cls, value):
        if len(value) < 8:
            raise ValueError('password too easy')
        return value


class CreateAdvValidator(pydantic.BaseModel):
    title: str
    description: str
