# /// script
# dependencies = [
#     "api",
# ]
#
# [tool.uv.sources]
# api = { path = "../packages/api" }
#
# ///

import os

os.environ["JWT_SECRET_KEY"] = "0"

import json

from fastapi.openapi.utils import get_openapi

from api.main import app

with open("openapi.json", "w") as outfile:
    json.dump(
        get_openapi(
            title="Public API",
            version="1.0",
            routes=app.routes,
        ),
        outfile,
        indent=3,
    )
