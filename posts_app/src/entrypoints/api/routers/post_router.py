from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse

from assembly import (
    build_count_posts_use_case,
    build_create_post_use_case,
    build_delete_post_use_case,
    build_get_post_use_case,
    build_list_posts_use_case,
    build_reset_posts_use_case,
)
from domain.models.post import Post
from domain.use_cases.base_use_case import BaseUseCase
from entrypoints.api.schemas import PostCreateRequest
from errors import InvalidExpirationDateError, PostNotFoundError

router = APIRouter(prefix="/posts")


def _serialize(post: Post) -> dict:
    return {
        "id": post.id,
        "routeId": post.route_id,
        "userId": post.user_id,
        "expireAt": post.expire_at.isoformat(),
        "createdAt": post.created_at.isoformat(),
    }


@router.get("/ping", response_class=PlainTextResponse)
def health_check():
    """Healthcheck endpoint."""
    return "pong"


@router.get("/count")
def count_posts(use_case: BaseUseCase = Depends(build_count_posts_use_case)):
    """Count stored posts."""
    return {"count": use_case.execute()}


@router.post("/reset")
def reset_posts(use_case: BaseUseCase = Depends(build_reset_posts_use_case)):
    """Delete all posts."""
    use_case.execute()
    return {"msg": "Todos los datos fueron eliminados"}


@router.post("", status_code=201)
def create_post(
    payload: PostCreateRequest,
    use_case: BaseUseCase = Depends(build_create_post_use_case),
):
    """Create a new post."""
    post = Post(
        route_id=payload.routeId,
        user_id=payload.userId,
        expire_at=payload.expireAt,
    )
    try:
        created = use_case.execute(post)
    except InvalidExpirationDateError as err:
        raise HTTPException(status_code=412, detail=str(err))
    return {
        "id": created.id,
        "userId": created.user_id,
        "createdAt": created.created_at.isoformat(),
    }


@router.get("")
def list_posts(
    expire: Optional[bool] = None,
    route: Optional[str] = None,
    owner: Optional[str] = None,
    use_case: BaseUseCase = Depends(build_list_posts_use_case),
):
    """List/filter posts."""
    posts = use_case.execute(expire=expire, route_id=route, owner_id=owner)
    return [_serialize(p) for p in posts]


@router.get("/{post_id}")
def get_post(
    post_id: str, use_case: BaseUseCase = Depends(build_get_post_use_case)
):
    """Get a post by id."""
    try:
        post = use_case.execute(post_id)
    except PostNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return _serialize(post)


@router.delete("/{post_id}")
def delete_post(
    post_id: str, use_case: BaseUseCase = Depends(build_delete_post_use_case)
):
    """Delete a post by id."""
    try:
        use_case.execute(post_id)
    except PostNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return {"msg": "la publicación fue eliminada"}
