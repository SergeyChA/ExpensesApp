from fastapi import (
    APIRouter,
    Depends,
)


from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.auth import (
    User,
    UserCreate,
    Token,
)


from ..services.auth import (
    AuthService,
    get_current_user,
)


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/reg', response_model=Token)
def reg_user(
        user_data: UserCreate,
        service: AuthService = Depends(),
):
    return service.register_new_user(user_data)


@router.post('/login', response_model=Token)
def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
):
    return service.authenticate_user(
        form_data.username,
        form_data.password,
    )


@router.get('/user', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user