from gqlalchemy import Memgraph
from fastapi_memgraph_crud.schemas import UserCreate, UserUpdate


def create_user_query(db: Memgraph, user: UserCreate):
    query = """
    CREATE (u:User {id: $id, name: $name, email: $email})
    RETURN u.id AS id, u.name AS name, u.email AS email
    """
    result = list(
        db.execute_and_fetch(
            query,
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            },
        )
    )
    return result[0] if result else None


def get_users_query(db: Memgraph):
    query = """
    MATCH (u:User)
    RETURN u.id AS id, u.name AS name, u.email AS email
    ORDER BY u.name
    """
    return list(db.execute_and_fetch(query))


def get_user_by_id_query(db: Memgraph, user_id: str):
    query = """
    MATCH (u:User {id: $id})
    RETURN u.id AS id, u.name AS name, u.email AS email
    LIMIT 1
    """
    result = list(db.execute_and_fetch(query, {"id": user_id}))
    return result[0] if result else None


def update_user_query(db: Memgraph, user_id: str, payload: UserUpdate):
    updates = []
    params = {"id": user_id}

    if payload.name is not None:
        updates.append("u.name = $name")
        params["name"] = payload.name

    if payload.email is not None:
        updates.append("u.email = $email")
        params["email"] = payload.email

    if not updates:
        return get_user_by_id_query(db, user_id)

    query = f"""
    MATCH (u:User {{id: $id}})
    SET {", ".join(updates)}
    RETURN u.id AS id, u.name AS name, u.email AS email
    """

    result = list(db.execute_and_fetch(query, params))
    return result[0] if result else None


def delete_user_query(db: Memgraph, user_id: str):
    query = """
    MATCH (u:User {id: $id})
    WITH u, u.id AS id, u.name AS name, u.email AS email
    DETACH DELETE u
    RETURN id, name, email
    """
    result = list(db.execute_and_fetch(query, {"id": user_id}))
    return result[0] if result else None
