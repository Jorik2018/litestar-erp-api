from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.exceptions import HTTPException
import traceback
from app.schemas.person import PersonCreate, PersonUpdate
from app.services.memgraph_service import MemgraphService
from app.dependencies import provide_memgraph_service


class PeopleController(Controller):
    path = "/people"
    dependencies = {
        "memgraph_service": Provide(provide_memgraph_service)
    }

    @get("/memgraph/test")
    async def test_memgraph(self, memgraph_service: MemgraphService) -> dict[str, str]:
        try:
            return memgraph_service.test_connection()
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    @get("/")
    async def list_people(self, memgraph_service: MemgraphService) -> list[dict]:
        try:
            return memgraph_service.list_people()
        except Exception as exc:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(exc))

    @get("/{person_id:int}")
    async def get_person(self, person_id: int, memgraph_service: MemgraphService) -> dict:
        try:
            person = memgraph_service.get_person(person_id)
            if not person:
                raise HTTPException(status_code=404, detail="Persona no encontrada")
            return person
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    @post("/")
    async def create_person(self, data: PersonCreate, memgraph_service: MemgraphService) -> dict:
        try:
            return memgraph_service.create_person(data.id, data.name, data.age)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    @patch("/{person_id:int}")
    async def update_person(
        self,
        person_id: int,
        data: PersonUpdate,
        memgraph_service: MemgraphService,
    ) -> dict:
        try:
            person = memgraph_service.update_person(
                person_id=person_id,
                name=data.name,
                age=data.age,
            )
            if not person:
                raise HTTPException(status_code=404, detail="Persona no encontrada")
            return person
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    @delete("/{person_id:int}", status_code=200)
    async def delete_person(
        self,
        person_id: int,
        memgraph_service: MemgraphService,
    ) -> dict[str, str]:
        try:
            deleted = memgraph_service.delete_person(person_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Persona no encontrada")
            return {"message": "Persona eliminada correctamente"}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
