from fastapi import FastAPI
from fastapi_memgraph_crud.config import settings
from fastapi_memgraph_crud.routers.users import router as users_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)

app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
