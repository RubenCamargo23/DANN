from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse

from assembly import (
    build_authenticate_user_use_case,
    build_count_users_use_case,
    build_create_user_use_case,
    build_get_authenticated_user_use_case,
    build_reset_users_use_case,
    build_update_user_use_case,
)
from domain.models.user import User
from domain.use_cases.base_use_case import BaseUseCase
from entrypoints.api.schemas import (
    UserAuthRequest,
    UserCreateRequest,
    UserUpdateRequest,
)
from errors import InvalidCredentialsError, InvalidTokenError, UserAlreadyExistsError, UserNotFoundError

router = APIRouter(prefix="/users")

VALID_STATUSES = {"POR_VERIFICAR", "NO_VERIFICADO", "VERIFICADO"}


@router.get("/ping", response_class=PlainTextResponse)
def health_check():
    """Healthcheck endpoint."""
    return "pong"


@router.get("/count")
def count_users(use_case: BaseUseCase = Depends(build_count_users_use_case)):
    """Count stored users."""
    return {"count": use_case.execute()}


@router.post("/reset")
def reset_users(use_case: BaseUseCase = Depends(build_reset_users_use_case)):
    """Delete all users."""
    use_case.execute()
    return {"msg": "Todos los datos fueron eliminados"}


@router.post("", status_code=201, responses={412: {"description": "User already exists"}})
def create_user(
    payload: UserCreateRequest,
    use_case: BaseUseCase = Depends(build_create_user_use_case),
):
    """Create a new user."""
    user = User(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        dni=payload.dni,
        full_name=payload.fullName,
        phone_number=payload.phoneNumber,
    )
    try:
        created = use_case.execute(user)
    except UserAlreadyExistsError as err:
        raise HTTPException(status_code=412, detail=str(err))
    return {"id": created.id, "createdAt": created.created_at.isoformat()}


@router.patch("/{user_id}", responses={404: {"description": "User not found"}})
def update_user(
    user_id: str,
    payload: UserUpdateRequest,
    use_case: BaseUseCase = Depends(build_update_user_use_case),
):
    """Update fields of an existing user."""
    if all(
        v is None
        for v in [payload.status, payload.dni, payload.fullName, payload.phoneNumber]
    ):
        raise HTTPException(status_code=400, detail="No fields to update")

    if payload.status is not None and payload.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status")

    try:
        use_case.execute(
            user_id,
            status=payload.status,
            dni=payload.dni,
            full_name=payload.fullName,
            phone_number=payload.phoneNumber,
        )
    except UserNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return {"msg": "el usuario ha sido actualizado"}


@router.post("/auth", responses={404: {"description": "Invalid credentials"}})
def authenticate(
    payload: UserAuthRequest,
    use_case: BaseUseCase = Depends(build_authenticate_user_use_case),
):
    """Generate a new session token for valid credentials."""
    try:
        user = use_case.execute(payload.username, payload.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    return {
        "id": user.id,
        "token": user.token,
        "expireAt": user.expire_at.isoformat(),
    }


@router.get(
    "/me",
    responses={
        401: {"description": "Invalid or expired token"},
        403: {"description": "Missing authorization header"},
    },
)
def get_me(
    authorization: str = Header(default=None),
    use_case: BaseUseCase = Depends(build_get_authenticated_user_use_case),
):
    """Return the user that owns the given bearer token."""
    if authorization is None:
        raise HTTPException(status_code=403, detail="Missing authorization header")

    token = authorization.replace("Bearer ", "").strip()
    try:
        user = use_case.execute(token)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "fullName": user.full_name,
        "dni": user.dni,
        "phoneNumber": user.phone_number,
        "status": user.status,
    }
