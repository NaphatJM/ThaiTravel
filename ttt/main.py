from fastapi import FastAPI
from contextlib import asynccontextmanager

from . import routers
from . import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await models.init_db()
    yield
    # Shutdown
    await models.close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(routers.router)


@app.get("/hello")
def read_root() -> dict:
    return {"msg": "Hello World"}
