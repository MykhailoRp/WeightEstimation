from fastapi import FastAPI

from api.model.basic import HealthCheck

app = FastAPI()


@app.get("/", status_code=200)
def health_check() -> HealthCheck:
    return HealthCheck()
