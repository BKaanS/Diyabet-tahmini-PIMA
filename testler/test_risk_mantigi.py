"""Risk seviyesi ve siniflama mantigi testleri."""

from __future__ import annotations

import pytest

from uygulama.servisler.risk_servisi import risk_esiklerini_al, risk_ozeti_hazirla


ORNEK_ESIK_YAPILANDIRMASI = {
    "onerilen_ikili_siniflama_esigi": 0.40,
    "risk_kategorileri": {
        "dusuk_ust_esik": 0.25,
        "orta_ust_esik": 0.60,
        "etiketler": ["dusuk", "orta", "yuksek"],
    },
}


@pytest.mark.parametrize(
    ("olasilik", "beklenen_sinif", "beklenen_risk"),
    [
        (0.10, 0, "dusuk"),
        (0.30, 0, "orta"),
        (0.60, 1, "yuksek"),
    ],
)
def test_risk_ozeti_hazirla_beklenen_sonuclari_donmeli(
    olasilik: float,
    beklenen_sinif: int,
    beklenen_risk: str,
) -> None:
    sonuc = risk_ozeti_hazirla(olasilik, ORNEK_ESIK_YAPILANDIRMASI)

    assert sonuc["sinif"] == beklenen_sinif
    assert sonuc["risk_kategorisi"] == beklenen_risk


def test_risk_esikleri_ters_sirada_ise_hata_vermeli() -> None:
    gecersiz = {
        "onerilen_ikili_siniflama_esigi": 0.40,
        "risk_kategorileri": {
            "dusuk_ust_esik": 0.80,
            "orta_ust_esik": 0.60,
        },
    }

    with pytest.raises(ValueError, match="buyuk olamaz"):
        risk_esiklerini_al(gecersiz)
