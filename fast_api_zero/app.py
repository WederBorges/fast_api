from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fast_api_zero.database import get_session
from fast_api_zero.models import User
from fast_api_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def html():
    return """<body> Olá mundo ! </body>"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Já tem um mano com esse nick   ',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Já tem um mano com esse email',
            )

    db_user = User(
        username=user.username, email=user.email, password=user.senha
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(session=Depends(get_session), limit: int = 10, offset: int = 0):

    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get(
    '/users/{id_user}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_only(id_user: int, session=Depends(get_session)):
    users = session.scalar(select(User).where(User.id == id_user))
    if users:
        return users
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
    )


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def uptade_user(
    user_id: int,
    user: UserSchema,
    session=Depends(get_session),
):

    user_db = session.scalar(select(User).where(User.id == user_id))
    email_exists = session.scalar(select(User).where(User.email == user.email))
    user_exists = session.scalar(
        select(User).where(User.username == user.username)
    )

    if email_exists:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Já existe esse e-mail cadastrado',
        )

    if user_exists:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Já existe esse nome de usuário cadastrado',
        )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Num existe esse usuário meu amigo',
        )
    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.senha

        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(HTTPStatus.CONFLICT)


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session=Depends(get_session)):

    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Esse usuário num tem não, hein',
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'Usuário EXCLUIDO'}
