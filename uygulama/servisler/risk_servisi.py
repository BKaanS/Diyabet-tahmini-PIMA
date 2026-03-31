"""Risk seviyesi ve ikili sinif karari icin servis fonksiyonlari."""

from __future__ import annotations

from typing import Any

from makine_ogrenmesi.kaynak.esik_analizi import risk_kategorisi_belirle


def ikili_sinif_hesapla(olasilik: float, esik_yapilandirmasi: dict[str, Any]) -> int:
    """Kalibre edilmis olasiliga gore ikili sinif tahmini uretir."""
    esik = onerilen_ikili_siniflama_esigi_al(esik_yapilandirmasi)
    return int(float(olasilik) >= esik)


def risk_kategorisi_hesapla(olasilik: float, esik_yapilandirmasi: dict[str, Any]) -> str:
    """Kalibre edilmis olasiliga gore risk kategorisini dondurur."""
    risk_esikleri = risk_esiklerini_al(esik_yapilandirmasi)
    return risk_kategorisi_belirle(
        olasilik=float(olasilik),
        dusuk_ust_esik=float(risk_esikleri["dusuk_ust_esik"]),
        orta_ust_esik=float(risk_esikleri["orta_ust_esik"]),
    )


def risk_ozeti_hazirla(olasilik: float, esik_yapilandirmasi: dict[str, Any]) -> dict[str, Any]:
    """Risk siniflamasini tek sozlukte toplar."""
    olasilik_float = float(olasilik)
    return {
        "olasilik": olasilik_float,
        "sinif": ikili_sinif_hesapla(olasilik_float, esik_yapilandirmasi),
        "risk_kategorisi": risk_kategorisi_hesapla(olasilik_float, esik_yapilandirmasi),
        "onerilen_ikili_siniflama_esigi": onerilen_ikili_siniflama_esigi_al(
            esik_yapilandirmasi
        ),
    }


def onerilen_ikili_siniflama_esigi_al(esik_yapilandirmasi: dict[str, Any]) -> float:
    """Esik konfigurasyonundan onerilen ikili siniflama esigini alir."""
    try:
        esik = float(esik_yapilandirmasi["onerilen_ikili_siniflama_esigi"])
    except KeyError as hata:
        raise KeyError("esik_yapilandirmasi icinde 'onerilen_ikili_siniflama_esigi' yok.") from hata

    _birim_aralik_kontrolu(esik, "onerilen_ikili_siniflama_esigi")
    return esik


def risk_esiklerini_al(esik_yapilandirmasi: dict[str, Any]) -> dict[str, float]:
    """Risk seviyesi esiklerini konfigurasyondan alir."""
    try:
        risk_kategorileri = esik_yapilandirmasi["risk_kategorileri"]
        dusuk = float(risk_kategorileri["dusuk_ust_esik"])
        orta = float(risk_kategorileri["orta_ust_esik"])
    except KeyError as hata:
        raise KeyError("esik_yapilandirmasi icinde risk esikleri eksik.") from hata

    _birim_aralik_kontrolu(dusuk, "dusuk_ust_esik")
    _birim_aralik_kontrolu(orta, "orta_ust_esik")
    if dusuk > orta:
        raise ValueError("risk esiklerinde dusuk_ust_esik, orta_ust_esik degerinden buyuk olamaz.")

    return {
        "dusuk_ust_esik": dusuk,
        "orta_ust_esik": orta,
    }


def _birim_aralik_kontrolu(deger: float, alan_adi: str) -> None:
    if deger < 0 or deger > 1:
        raise ValueError(f"{alan_adi} degeri 0 ile 1 araliginda olmalidir.")
