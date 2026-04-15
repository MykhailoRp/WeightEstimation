from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.openapi.docs import (
    get_swagger_ui_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from api.dependencies import docs_authenticate
from api.routers import router as app_router

doc_router = APIRouter(prefix="/docs", include_in_schema=False)


def get_public_openapi() -> dict[str, Any]:
    routes = [r for r in app_router.routes if "public" in r.__getattribute__("tags")]
    return get_openapi(
        title="Public API",
        version="1.0",
        routes=routes,
    )


def get_internal_openapi() -> dict[str, Any]:
    return get_openapi(
        title="Internal API",
        version="1.0",
        routes=app_router.routes,
    )


@doc_router.get("/openapi-public.json")
def openapi_public() -> dict[str, Any]:
    return get_public_openapi()


@doc_router.get("/openapi-internal.json")
def openapi_internal(_: Annotated[str, Depends(docs_authenticate)]) -> dict[str, Any]:
    return get_internal_openapi()


@doc_router.get("/")
def public_docs() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/docs/openapi-public.json",
        title="Public Docs",
    )


@doc_router.get("/internal")
def internal_docs() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/docs/openapi-internal.json",
        title="Internal Docs",
    )
