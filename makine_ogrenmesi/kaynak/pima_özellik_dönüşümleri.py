"""PIMA 1000/1000 üretim modeli için özellik dönüşümleri."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from .ozellik_yapilandirmasi import OZELLIK_KOLONLARI, SIFIRI_EKSIK_SAYILAN_KOLONLAR


class ClinicalFeatureTransformer(BaseEstimator, TransformerMixin):
    """Seçilen klinik özellik setini üretir ve modele verilecek kolonları döndürür."""

    def __init__(self, base_columns: tuple[str, ...], engineered: tuple[str, ...]) -> None:
        self.base_columns = base_columns
        self.engineered = engineered

    def fit(self, x: Any, y: Any = None) -> "ClinicalFeatureTransformer":
        return self

    def transform(self, x: Any) -> pd.DataFrame:
        df = _dataframe_yap(x)
        eps = 1e-6
        out = df.loc[:, list(self.base_columns)].copy()
        if "glucose_bmi_ratio" in self.engineered:
            out["glucose_bmi_ratio"] = df["Glucose"] / (df["BMI"] + eps)
        if "glucose_age_interaction" in self.engineered:
            out["glucose_age_interaction"] = df["Glucose"] * df["Age"]
        if "glucose_bmi_interaction" in self.engineered:
            out["glucose_bmi_interaction"] = df["Glucose"] * df["BMI"]
        if "glucose_pedigree_interaction" in self.engineered:
            out["glucose_pedigree_interaction"] = df["Glucose"] * df["DiabetesPedigreeFunction"]
        if "age_bmi_interaction" in self.engineered:
            out["age_bmi_interaction"] = df["Age"] * df["BMI"]
        if "age_pedigree_interaction" in self.engineered:
            out["age_pedigree_interaction"] = df["Age"] * df["DiabetesPedigreeFunction"]
        if "pregnancies_age_ratio" in self.engineered:
            out["pregnancies_age_ratio"] = df["Pregnancies"] / (df["Age"] + eps)
        if "insulin_glucose_ratio" in self.engineered:
            out["insulin_glucose_ratio"] = df["Insulin"] / (df["Glucose"] + eps)
        if "bp_bmi_ratio" in self.engineered:
            out["bp_bmi_ratio"] = df["BloodPressure"] / (df["BMI"] + eps)
        if "bmi_age_ratio" in self.engineered:
            out["bmi_age_ratio"] = df["BMI"] / (df["Age"] + eps)
        if "glucose_minus_bmi" in self.engineered:
            out["glucose_minus_bmi"] = df["Glucose"] - df["BMI"]
        if "glucose_per_age" in self.engineered:
            out["glucose_per_age"] = df["Glucose"] / (df["Age"] + eps)
        return out.replace([np.inf, -np.inf], np.nan).fillna(0)

    def feature_names(self) -> list[str]:
        return [*self.base_columns, *self.engineered]


class PimaZeroMedianImputer(BaseEstimator, TransformerMixin):
    """PIMA'da klinik olarak eksik sayılan 0 değerlerini eğitim medyanıyla doldurur."""

    def __init__(self, missing_zero_columns: tuple[str, ...] = tuple(SIFIRI_EKSIK_SAYILAN_KOLONLAR)) -> None:
        self.missing_zero_columns = missing_zero_columns

    def fit(self, x: Any, y: Any = None) -> "PimaZeroMedianImputer":
        veri = _dataframe_yap(x).copy()
        medyanlar: dict[str, float] = {}
        for kolon in OZELLIK_KOLONLARI:
            seri = pd.to_numeric(veri[kolon], errors="coerce")
            if kolon in self.missing_zero_columns:
                seri = seri.where(seri != 0, np.nan)
            medyan = float(seri.median())
            medyanlar[kolon] = medyan if not np.isnan(medyan) else 0.0
        self.medians_ = medyanlar
        return self

    def transform(self, x: Any) -> pd.DataFrame:
        if not hasattr(self, "medians_"):
            raise RuntimeError("PimaZeroMedianImputer fit edilmeden transform çağrıldı.")
        veri = _dataframe_yap(x).copy()
        for kolon in OZELLIK_KOLONLARI:
            seri = pd.to_numeric(veri[kolon], errors="coerce")
            if kolon in self.missing_zero_columns:
                seri = seri.where(seri != 0, np.nan)
            veri[kolon] = seri.fillna(self.medians_[kolon])
        return _clip_clinical(veri)


def _dataframe_yap(x: Any) -> pd.DataFrame:
    if isinstance(x, pd.DataFrame):
        return x.copy()
    return pd.DataFrame(x, columns=OZELLIK_KOLONLARI)


def _clip_clinical(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    bounds = {
        "Pregnancies": (0, 17),
        "Glucose": (45, 220),
        "BloodPressure": (38, 125),
        "SkinThickness": (5, 70),
        "Insulin": (5, 850),
        "BMI": (15, 70),
        "DiabetesPedigreeFunction": (0.05, 2.5),
        "Age": (18, 90),
    }
    for kolon, (alt, ust) in bounds.items():
        if kolon in out.columns:
            out[kolon] = pd.to_numeric(out[kolon], errors="coerce").clip(alt, ust)
    if "Pregnancies" in out.columns:
        out["Pregnancies"] = out["Pregnancies"].round().astype(int)
    if "Age" in out.columns:
        out["Age"] = out["Age"].round().astype(int)
    return out
