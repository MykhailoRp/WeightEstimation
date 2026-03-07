from fastapi import FastAPI

from api.lifespan import lifespan
from api.routers import router

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)
