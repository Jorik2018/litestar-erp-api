from fastapi import APIRouter, HTTPException, status
from fastapi_memgraph_crud.db import get_memgraph
from fastapi_memgraph_crud.queries import (
    create_user_query,
    delete_user_query,
    get_user_by_id_query,
    get_users_query,
    update_user_query,
)
from fastapi_memgraph_crud.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    db = get_memgraph()

    existing = get_user_by_id_query(db, user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya existe",
        )

    created = create_user_query(db, user)
    return created


@router.get("", response_model=list[UserResponse])
def list_users():
    db = get_memgraph()
    return get_users_query(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    db = get_memgraph()
    user = get_user_by_id_query(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, payload: UserUpdate):
    db = get_memgraph()
    existing = get_user_by_id_query(db, user_id)

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    updated = update_user_query(db, user_id, payload)
    return updated


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: str):
    db = get_memgraph()
    deleted = delete_user_query(db, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return deleted
