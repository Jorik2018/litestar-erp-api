from app.services.memgraph_service import MemgraphService


def provide_memgraph_service() -> MemgraphService:
    return MemgraphService()
