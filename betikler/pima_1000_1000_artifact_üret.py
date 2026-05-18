"""PIMA 1000/1000 sentetik eğitim seti için üretim artifactlerini oluşturur."""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.pipeline import Pipeline


PROJE_KOKU = Path(__file__).resolve().parents[1]
if str(PROJE_KOKU) not in sys.path:
    sys.path.insert(0, str(PROJE_KOKU))

from makine_ogrenmesi.kaynak.artifact_kaydet import artifactleri_kaydet  # noqa: E402
from makine_ogrenmesi.kaynak.ozellik_yapilandirmasi import HEDEF_KOLONU, OZELLIK_KOLONLARI  # noqa: E402
from makine_ogrenmesi.kaynak.pima_özellik_dönüşümleri import (  # noqa: E402
    ClinicalFeatureTransformer,
    PimaZeroMedianImputer,
)


RANDOM_STATE = 42
MODEL_KODU = "pima_1000_1000_extra_trees_v1"
VERI_YOLU = PROJE_KOKU / "makine_ogrenmesi" / "veri" / "deneysel" / "pima_1000_1000_sentetik_eğitim.csv"
METADATA_YOLU = PROJE_KOKU / "makine_ogrenmesi" / "veri" / "deneysel" / "pima_1000_1000_sentetik_metadata.csv"
ARTIFACT_KLASORU = PROJE_KOKU / "makine_ogrenmesi" / "artifactler"
YEDEK_KLASORU = PROJE_KOKU / "tmp" / "artifact_yedekleri" / datetime.now().strftime("%Y%m%d_%H%M%S")

HOLDOUT_METRIKLERI = {
    "accuracy": 0.9392523364485982,
    "precision": 0.943127962085308,
    "recall": 0.9342723004694836,
    "sensitivity": 0.9342723004694836,
    "specificity": 0.9441860465116279,
    "f1": 0.9386792452830188,
    "roc_auc": 0.9860246751828803,
    "balanced_accuracy": 0.9392291734905558,
    "mcc": 0.8785350866651979,
    "brier": 0.04589904997296672,
    "threshold": 0.45,
    "confusion_matrix": {
        "tn": 203,
        "fp": 12,
        "fn": 14,
        "tp": 199,
        "matrix": [[203, 12], [14, 199]],
    },
    "ana_metrik_minimumu": 0.9342723004694836,
}

GROUP_CV_OZETI = {
    "accuracy_mean": 0.918001046881543,
    "precision_mean": 0.9092939244663383,
    "recall_mean": 0.9289893497337435,
    "specificity_mean": 0.907,
    "f1_mean": 0.9188970545983102,
    "roc_auc_mean": 0.9784548098702469,
    "balanced_accuracy_mean": 0.9179946748668717,
    "mcc_mean": 0.8364622838364777,
    "brier_mean": 0.05610909457659834,
    "ana_metrik_minimumu_mean": 0.9030000000000001,
    "max_source_intersection_count": 0,
}


def _pipeline_olustur() -> Pipeline:
    # Üretim modeli ham 8 PIMA girdisini kabul eder; klinik dönüşümler pipeline içinde yapılır.
    return Pipeline(
        steps=[
            ("pima_zero_median_imputer", PimaZeroMedianImputer()),
            (
                "features",
                ClinicalFeatureTransformer(
                    base_columns=("Pregnancies", "Glucose", "BMI", "DiabetesPedigreeFunction", "Age", "Insulin"),
                    engineered=("glucose_bmi_interaction", "insulin_glucose_ratio", "glucose_pedigree_interaction"),
                ),
            ),
            (
                "model",
                ExtraTreesClassifier(
                    n_estimators=220,
                    max_features="sqrt",
                    min_samples_leaf=1,
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                    n_jobs=2,
                ),
            ),
        ]
    )


def _artifactleri_yedekle() -> None:
    if not ARTIFACT_KLASORU.exists():
        return
    mevcutlar = [yol for yol in ARTIFACT_KLASORU.iterdir() if yol.is_file()]
    if not mevcutlar:
        return
    YEDEK_KLASORU.mkdir(parents=True, exist_ok=True)
    for yol in mevcutlar:
        try:
            shutil.copy2(yol, YEDEK_KLASORU / yol.name)
        except OSError as hata:
            print(f"Uyarı: mevcut artifact yedeklenemedi: {yol.name} ({hata})")


def _metadata_oku() -> pd.DataFrame:
    metadata = pd.read_csv(METADATA_YOLU)
    if "is_synthetic" not in metadata.columns:
        raise ValueError("Metadata dosyasında is_synthetic kolonu yok.")
    return metadata


def _sinif_dagilimi(veri: pd.DataFrame) -> dict[str, int]:
    return {str(k): int(v) for k, v in veri[HEDEF_KOLONU].value_counts().sort_index().items()}


def _json_yaz(yol: Path, veri: Any) -> None:
    yol.write_text(json.dumps(veri, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    if not VERI_YOLU.exists():
        raise FileNotFoundError(VERI_YOLU)
    if not METADATA_YOLU.exists():
        raise FileNotFoundError(METADATA_YOLU)

    veri = pd.read_csv(VERI_YOLU)
    metadata = _metadata_oku()
    x = veri[OZELLIK_KOLONLARI]
    y = veri[HEDEF_KOLONU].astype(int)

    pipeline = _pipeline_olustur()
    pipeline.fit(x, y)

    sentetik_maskesi = metadata["is_synthetic"].astype(bool)
    sentetik_satir = int(sentetik_maskesi.sum())
    orijinal_satir = int((~sentetik_maskesi).sum())
    threshold = float(HOLDOUT_METRIKLERI["threshold"])

    _artifactleri_yedekle()
    kaydedilenler = artifactleri_kaydet(
        ARTIFACT_KLASORU,
        en_iyi_pipeline=pipeline,
        kalibrator=pipeline,
        esik_yapilandirmasi={
            "ikili_siniflama_esikleri": {
                MODEL_KODU: {
                    "esik": threshold,
                    "aciklama": "PIMA 1000/1000 sentetik eğitim seti için iç doğrulama/holdout dengesine göre seçilen eşik.",
                }
            },
            "onerilen_ikili_siniflama_esigi": threshold,
            "onerilen_ikili_siniflama_yontemi": MODEL_KODU,
            "risk_kategorileri": {
                "dusuk_ust_esik": 0.33,
                "orta_ust_esik": 0.66,
                "etiketler": ["dusuk", "orta", "yuksek"],
            },
        },
        ozellik_sirasi=list(OZELLIK_KOLONLARI),
        metrik_ozeti=HOLDOUT_METRIKLERI,
        model_metadata={
            "veri_seti": "PIMA 1000/1000 sentetik eğitim seti",
            "model_adi": "ExtraTrees",
            "model_kodu": MODEL_KODU,
            "model_aciklamasi": "PIMA 1000/1000 sentetik eğitim seti - ExtraTrees",
            "final_benchmark_adayi": "1000/1000",
            "veri_yolu": str(VERI_YOLU.relative_to(PROJE_KOKU)),
            "metadata_yolu": str(METADATA_YOLU.relative_to(PROJE_KOKU)),
            "feature_set": "high_signal_features",
            "model_girdi_kolonlari": list(OZELLIK_KOLONLARI),
            "model_ic_ozellikler": [
                "Pregnancies",
                "Glucose",
                "BMI",
                "DiabetesPedigreeFunction",
                "Age",
                "Insulin",
                "glucose_bmi_interaction",
                "insulin_glucose_ratio",
                "glucose_pedigree_interaction",
            ],
            "orijinal_dev_satiri": orijinal_satir,
            "sentetik_satir": sentetik_satir,
            "toplam_satir": int(len(veri)),
            "sinif_dagilimi": _sinif_dagilimi(veri),
            "source_id_kurali": "Her sentetik satır kaynak aldığı original_{index} ailesine bağlıdır.",
            "independent_synthetic_source_id_count": int(
                metadata.loc[sentetik_maskesi, "source_id"].astype(str).str.startswith(("synthetic_", "gaussian_")).sum()
            ),
            "benchmark_holdout_metrikleri": HOLDOUT_METRIKLERI,
            "benchmark_group_cv": GROUP_CV_OZETI,
            "not": (
                "Bu artifact PIMA 1000/1000 sentetik eğitim setine göre üretilmiştir. "
                "Original external holdout klinik genellenebilirlik kanıtı değil, dış kontrol sınırı olarak yorumlanmalıdır."
            ),
        },
    )

    _json_yaz(
        ARTIFACT_KLASORU / "artifact_uretimi_ozeti.json",
        {
            "model_kodu": MODEL_KODU,
            "dosyalar": {k: str(v.relative_to(PROJE_KOKU)) for k, v in kaydedilenler.items()},
        },
    )

    print("PIMA 1000/1000 üretim artifactleri oluşturuldu.")
    print(f"Model kodu: {MODEL_KODU}")
    print(f"Veri: {VERI_YOLU}")
    print(f"Artifact klasörü: {ARTIFACT_KLASORU}")
    for ad, yol in kaydedilenler.items():
        print(f"- {ad}: {yol} ({yol.stat().st_size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
