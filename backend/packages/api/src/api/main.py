from fastapi import FastAPI

from api.docs import doc_router
from api.lifespan import lifespan
from api.routers import router

app = FastAPI(lifespan=lifespan, openapi_url=None)

app.include_router(router=router)
app.include_router(router=doc_router)
