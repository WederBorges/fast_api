from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_api_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def html():
    return """<body> Olá mundo ! </body>"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        username=user.username,
        email=user.email,
        senha=user.senha,
        id=len(database) + 1,
    )
    database.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.get(
    '/users/{id_user}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_only(id_user: int):
    for i, exists in enumerate(database):
        print(exists.id)
        if exists.id == id_user:
            return exists
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
    )


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
def uptade_user(user_id: int, user: UserSchema, new_email: str):
    for i, exists_user in enumerate(database):
        if exists_user.id == user_id:
            user_with_id = UserDB(
                username=user.username,
                email=new_email,
                senha=user.senha,
                id=user_id,
            )
            database[i] = user_with_id
            return user_with_id

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Usuário não encontrado',
    )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):

    for i, exist_user in enumerate(database):
        if exist_user.id == user_id:
            del database[i]
            return exist_user
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
    )
