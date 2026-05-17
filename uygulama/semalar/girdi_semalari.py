"""Tahmin girdisi icin Pydantic semalari."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from .dogrulamalar import ALAN_ARALIKLARI, sayisal_aralik_dogrula


class TahminGirdisi(BaseModel):
    """Tahmin endpointine gelecek kullanici girdisi."""

    model_config = ConfigDict(extra="forbid")

    pregnancies: int = Field(
        ...,
        ge=ALAN_ARALIKLARI["pregnancies"][0],
        le=ALAN_ARALIKLARI["pregnancies"][1],
        description="Gebelik sayısı",
        examples=[2],
    )
    glucose: float = Field(
        ...,
        ge=ALAN_ARALIKLARI["glucose"][0],
        le=ALAN_ARALIKLARI["glucose"][1],
        description="Plazma glikoz konsantrasyonu (mg/dL)",
        examples=[120],
    )
    blood_pressure: float = Field(
        ...,
        ge=ALAN_ARALIKLARI["blood_pressure"][0],
        le=ALAN_ARALIKLARI["blood_pressure"][1],
        description="Diyastolik kan basıncı (mmHg)",
        examples=[72],
    )
    skin_thickness: float = Field(
        ...,
        ge=ALAN_ARALIKLARI["skin_thickness"][0],
        le=ALAN_ARALIKLARI["skin_thickness"][1],
        description="Triceps deri kıvrım kalınlığı (mm)",
        examples=[35],
    )
    insulin: float = Field(
        ...,
        ge=ALAN_ARALIKLARI["insulin"][0],
        le=ALAN_ARALIKLARI["insulin"][1],
        description="2 saatlik serum insülin değeri (µU/mL)",
        examples=[120],
    )
    bmi: float = Field(
        ...,
        ge=ALAN_ARALIKLARI["bmi"][0],
        le=ALAN_ARALIKLARI["bmi"][1],
        description="Vücut kitle indeksi (kg/m²)",
        examples=[33.6],
    )
    diabetes_pedigree_function: float = Field(
        ...,
        ge=ALAN_ARALIKLARI["diabetes_pedigree_function"][0],
        le=ALAN_ARALIKLARI["diabetes_pedigree_function"][1],
        description="Ailesel diyabet yatkınlığı katsayısı",
        examples=[0.627],
    )
    age: int = Field(
        ...,
        ge=ALAN_ARALIKLARI["age"][0],
        le=ALAN_ARALIKLARI["age"][1],
        description="Yaş",
        examples=[50],
    )

    @field_validator(
        "pregnancies",
        "glucose",
        "blood_pressure",
        "skin_thickness",
        "insulin",
        "bmi",
        "diabetes_pedigree_function",
        "age",
    )
    @classmethod
    def alan_araliklarini_dogrula(cls, deger: float | int, info: ValidationInfo) -> float | int:
        return sayisal_aralik_dogrula(info.field_name, deger)
