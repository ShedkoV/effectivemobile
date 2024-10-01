import uvicorn
from fastapi import FastAPI

from app.api.routes import setup_routes
from app.config.config import SERVICE_HOST, SERVICE_PORT


def prepare_app() -> FastAPI:
    """Подготовка приложения для его запуска."""
    app = FastAPI()
    setup_routes(app)

    return app


if __name__ == '__main__':
    app = prepare_app()
    uvicorn.run(
        app=app,
        host=SERVICE_HOST,
        port=SERVICE_PORT,
    )
