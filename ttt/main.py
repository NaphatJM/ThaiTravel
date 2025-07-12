from fastapi import FastAPI
from . import routers
from . import models

app = FastAPI()
app.include_router(routers.router)

models.create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Welcome to เที่ยวไทยคนละครึ่ง!"}
