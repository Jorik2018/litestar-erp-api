from litestar import Litestar
from app.controllers.people import PeopleController


app = Litestar(route_handlers=[PeopleController])
