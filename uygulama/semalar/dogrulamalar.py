"""Sema katmani icin ortak dogrulama kurallari."""

from __future__ import annotations

import math


ALAN_ARALIKLARI: dict[str, tuple[float, float]] = {
    "pregnancies": (0, 17),
    "glucose": (50, 300),
    "blood_pressure": (40, 130),
    "skin_thickness": (7, 70),
    "insulin": (10, 850),
    "bmi": (15, 70),
    "diabetes_pedigree_function": (0.05, 2.5),
    "age": (21, 90),
}

ALAN_GORUNUR_ADLARI: dict[str, str] = {
    "pregnancies": "Gebelik sayısı",
    "glucose": "Glikoz",
    "blood_pressure": "Kan basıncı",
    "skin_thickness": "Cilt kalınlığı",
    "insulin": "İnsülin",
    "bmi": "Vücut kitle indeksi",
    "diabetes_pedigree_function": "Soyağacı fonksiyonu",
    "age": "Yaş",
}

ALAN_BIRIMLERI: dict[str, str] = {
    "glucose": "mg/dL",
    "blood_pressure": "mmHg",
    "skin_thickness": "mm",
    "insulin": "µU/mL",
    "bmi": "kg/m²",
}

RISK_KATEGORILERI = {"dusuk", "orta", "yuksek"}
YON_DEGERLERI = {"arttirici", "azaltici"}


def _sayi_metni(deger: float) -> str:
    if float(deger).is_integer():
        return str(int(deger))
    return str(deger)


def alan_aralik_mesaji(alan_adi: str) -> str:
    """Alan için kullanıcıya gösterilecek temiz aralık mesajını üretir."""
    alt_sinir, ust_sinir = ALAN_ARALIKLARI[alan_adi]
    alan_etiketi = ALAN_GORUNUR_ADLARI.get(alan_adi, alan_adi)
    birim = ALAN_BIRIMLERI.get(alan_adi, "")
    birim_metni = f" {birim}" if birim else ""
    return (
        f"{alan_etiketi} {_sayi_metni(alt_sinir)} ile {_sayi_metni(ust_sinir)}"
        f"{birim_metni} arasında olmalıdır."
    )


def dogrulama_hatalarini_ozetle(hatalar: list[dict]) -> str:
    """Pydantic/FastAPI doğrulama hatasını kullanıcı dostu tek cümleye indirger."""
    ilk_hata = hatalar[0] if hatalar else {}
    konum = ilk_hata.get("loc", [])
    alan = str(konum[-1]) if konum else "girdi"
    hata_tipi = str(ilk_hata.get("type", ""))
    alan_etiketi = ALAN_GORUNUR_ADLARI.get(alan, "Girdi")

    if hata_tipi == "missing":
        return f"{alan_etiketi} alanı zorunludur."
    if hata_tipi in {"int_parsing", "float_parsing", "int_type", "float_type"}:
        return f"{alan_etiketi} sayısal bir değer olmalıdır."
    if alan in ALAN_ARALIKLARI:
        return alan_aralik_mesaji(alan)

    return "Girilen değerleri kontrol edin."


def sayisal_aralik_dogrula(alan_adi: str, deger: float | int) -> float | int:
    """Sayisal bir degerin alan bazli aralik kurallarina uydugunu dogrular."""
    if alan_adi not in ALAN_ARALIKLARI:
        raise ValueError(f"Aralik tanimi bulunamadi: {alan_adi}")

    alt_sinir, ust_sinir = ALAN_ARALIKLARI[alan_adi]
    sayi = float(deger)

    if not math.isfinite(sayi):
        alan_etiketi = ALAN_GORUNUR_ADLARI.get(alan_adi, alan_adi)
        raise ValueError(f"{alan_etiketi} geçerli bir sayı olmalıdır.")
    if sayi < alt_sinir or sayi > ust_sinir:
        raise ValueError(alan_aralik_mesaji(alan_adi))

    return deger


def birim_aralik_dogrula(alan_adi: str, deger: float | int) -> float | int:
    """0-1 araligindaki olasilik degerlerini dogrular."""
    sayi = float(deger)
    if not math.isfinite(sayi):
        raise ValueError(f"{alan_adi} sonlu bir sayi olmalidir.")
    if sayi < 0 or sayi > 1:
        raise ValueError(f"{alan_adi} degeri 0 ile 1 araliginda olmalidir.")
    return deger


def risk_kategorisi_dogrula(deger: str) -> str:
    """Risk kategorisi alaninin desteklenen degerlerden biri oldugunu dogrular."""
    if deger not in RISK_KATEGORILERI:
        raise ValueError("risk_kategorisi sadece dusuk, orta veya yuksek olabilir.")
    return deger


def yon_dogrula(deger: str) -> str:
    """SHAP yon alaninin desteklenen degerlerden biri oldugunu dogrular."""
    if deger not in YON_DEGERLERI:
        raise ValueError("yon sadece arttirici veya azaltici olabilir.")
    return deger
