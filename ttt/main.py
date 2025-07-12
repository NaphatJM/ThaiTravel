from fastapi import FastAPI
from . import routers

app = FastAPI()
app.include_router(routers.router)


@app.get("/")
async def root():
    return {"message": "Welcome to เที่ยวไทยคนละครึ่ง!"}
