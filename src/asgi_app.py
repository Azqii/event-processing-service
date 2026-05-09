from dishka.integrations.fastapi import setup_dishka
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

from infrastructure.config.app import AppSettings
from infrastructure.di.container import create_container
from presentation.api.routes.v1 import router as v1_router

settings = AppSettings()
container = create_container()

_bearer = HTTPBearer(auto_error=False)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    dependencies=[Depends(_bearer)],
)

app.include_router(v1_router)

setup_dishka(container, app)
