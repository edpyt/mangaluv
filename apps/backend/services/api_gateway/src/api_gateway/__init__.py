from fastapi import FastAPI

from api_gateway.routes.healthcheck import router as health_router

# TODO: separate function to setup app
app = FastAPI()
app.include_router(health_router)
