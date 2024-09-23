from fastapi import FastAPI

from app.api.routes import setup_routes

app = FastAPI()
setup_routes(app)
