from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr  # validacao email
    senha: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
