from fastapi_memgraph_crud.config import settings
from gqlalchemy import Memgraph

def get_memgraph() -> Memgraph:
    return Memgraph(
        host=settings.memgraph_host,
        port=settings.memgraph_port,
        username=settings.memgraph_username or None,
        password=settings.memgraph_password or None,
    )
