"""FastAPI ana uygulama giris noktasi."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from uygulama.api import api_router
from uygulama.cekirdek.ayarlar import ayarlari_yukle
from uygulama.semalar.dogrulamalar import dogrulama_hatalarini_ozetle


APP_KLASORU = Path(__file__).resolve().parent
STATIK_KLASORU = APP_KLASORU / "statik"


def uygulama_olustur() -> FastAPI:
    ayarlar = ayarlari_yukle()

    app = FastAPI(
        title=ayarlar.app_adi,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.mount("/statik", StaticFiles(directory=str(STATIK_KLASORU)), name="statik")
    app.include_router(api_router)

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"detail": dogrulama_hatalarini_ozetle(exc.errors())},
        )

    return app


app = uygulama_olustur()
