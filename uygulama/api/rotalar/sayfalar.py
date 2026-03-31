"""Sayfa tabanli endpointler."""

from pathlib import Path

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from uygulama.semalar.cikti_semalari import TahminCiktisi
from uygulama.semalar.girdi_semalari import TahminGirdisi
from uygulama.servisler.tahmin_servisi import tek_ornek_tahmin_uret


router = APIRouter(prefix="", tags=["sayfalar"])
SABLON_KLASORU = Path(__file__).resolve().parents[2] / "sablonlar"
templates = Jinja2Templates(directory=str(SABLON_KLASORU))


@router.get("/", response_class=HTMLResponse)
def ana_sayfa(request: Request) -> HTMLResponse:
    """Uygulama ana giris endpointi."""
    return templates.TemplateResponse(
        request=request,
        name="ana_sayfa.html",
        context={"hata_mesaji": None, "form_data": {}},
    )


@router.post("/sonuc", response_class=HTMLResponse, name="sonuc_sayfasi")
async def sonuc_sayfasi(request: Request) -> HTMLResponse:
    """Form girdisini alip tahmin sonucunu HTML olarak dondurur."""
    ham_form = dict(await request.form())

    try:
        girdi = TahminGirdisi(**ham_form)
        sonuc = TahminCiktisi(**tek_ornek_tahmin_uret(girdi))
        return templates.TemplateResponse(
            request=request,
            name="sonuc.html",
            context={"sonuc": sonuc},
        )
    except ValidationError as hata:
        return templates.TemplateResponse(
            request=request,
            name="ana_sayfa.html",
            context={
                "hata_mesaji": _dogrulama_hatasini_ozetle(hata),
                "form_data": ham_form,
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except (ValueError, TypeError) as hata:
        return templates.TemplateResponse(
            request=request,
            name="hata.html",
            context={"hata_mesaji": str(hata)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except FileNotFoundError as hata:
        return templates.TemplateResponse(
            request=request,
            name="hata.html",
            context={"hata_mesaji": str(hata)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="hata.html",
            context={"hata_mesaji": "Tahmin islemi sirasinda beklenmeyen bir hata olustu."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def _dogrulama_hatasini_ozetle(hata: ValidationError) -> str:
    """Ilk dogrulama hatasini formda gostermek icin sade metin uretir."""
    ilk_hata = hata.errors()[0] if hata.errors() else {}
    ham_alan = ilk_hata.get("loc", [])
    alan = str(ham_alan[-1]) if ham_alan else "girdi"
    mesaj = str(ilk_hata.get("msg", "Gecersiz girdi."))
    return f"{alan}: {mesaj}"
