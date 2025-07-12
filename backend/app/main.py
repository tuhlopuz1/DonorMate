from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.models.db_adapter import adapter
from app.core.routers_loader import include_all_routers


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    await adapter.initialize_tables()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="DonorMate FastAPI",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    include_all_routers(app)
    return app


app = create_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def redirect():
    return RedirectResponse("/docs")
