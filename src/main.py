from contextlib import asynccontextmanager


from fastapi import FastAPI, APIRouter


from .hex.infrastructure.routers.rest import router as rest_router
from .hex.infrastructure.repository.sqlite3 import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


router = APIRouter(prefix="/api")
router.include_router(rest_router)


app = FastAPI(lifespan=lifespan, docs_url="/")
app.include_router(router)
