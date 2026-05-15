from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_api_zero.database import get_session
from fast_api_zero.models import User
from fast_api_zero.schemas import (
    Message,
    Token,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_api_zero.security import (
    create_acess_token,
    get_current_user,
    get_password_hash,
    verify_password,
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
        username=user.username,
        email=user.email,
        password=get_password_hash(user.senha),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session=Depends(get_session),
    current_user=Depends(get_current_user),
    limit: int = 10,
    offset: int = 0,
):

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
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='vc n pode faze isso ! ox'
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.senha)

        session.commit()
        session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(HTTPStatus.CONFLICT)


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(
    user_id: int,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):

    session.delete(current_user)
    session.commit()

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='vc n pode faze isso ! ox'
        )
    return {'message': 'Usuário EXCLUIDO'}


@app.post('/token', response_model=Token)
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user_db = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Usuário não existe, ou email tá errado pae',
        )

    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Senha ta errada em pae',
        )

    acess_token = create_acess_token(data={'sub': user_db.email})
    return {'acess_token': acess_token, 'token_type': 'Bearer'}
