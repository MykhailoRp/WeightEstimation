from fastapi import FastAPI

from api.model.basic import HealthCheck

app = FastAPI()


@app.get("/health/", status_code=200, include_in_schema=False)
def health_check() -> HealthCheck:
    return HealthCheck()
