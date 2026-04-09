# Diyabet Risk Tahmini (PIMA)

Bu proje, **Pima Indians Diabetes** veri seti üzerinden kadın bireylerde diyabet riskini tahmin eden bir makine öğrenmesi uygulamasıdır.  
Sistem bir klinik tanı aracı değildir; karar destek ve farkındalık amacıyla tasarlanmıştır.

## 1. Proje Özeti

- Problem tipi: Binary classification
- Veri seti: Pima Indians Diabetes (`diabetes.csv`)
- Modeller: Logistic Regression, Random Forest, XGBoost
- Backend: FastAPI
- Arayüz: HTML + Jinja2
- Açıklanabilirlik: SHAP tabanlı üst faktörler

## 2. Klasör Yapısı

- `uygulama/`: FastAPI uygulaması, servisler, şemalar, şablonlar ve statik dosyalar
- `makine_ogrenmesi/`: modelleme kodları, veri klasörleri, raporlar, notebook’lar
- `testler/`: pytest testleri
- `betikler/`: eğitim, değerlendirme ve raporlama betikleri
- `dokumanlar/`: proje ve teslimat dokümanları
- `dagitim/`: deploy (gunicorn/nginx/systemd) dosyaları

## 3. Kurulum

### 3.1 Gereksinimler

- Python 3.10+
- `pip`

### 3.2 Sanal ortam ve paket kurulumu

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3.3 Ortam değişkenleri

```bash
cp .env.example .env
```

Önemli varsayılan alanlar:

- `APP_ADI=diyabet-risk-tahmini`
- `APP_ENV=gelistirme`
- `APP_HOST=127.0.0.1`
- `APP_PORT=8000`
- `MODEL_ARTIFACT_KLASORU=makine_ogrenmesi/artifactler`

## 4. Veri Dosyası

Veri dosyasını şu konumda tut:

- `makine_ogrenmesi/veri/ham/diabetes.csv`

Kaynak:

- https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

## 5. Uygulamayı Çalıştırma

```bash
python3 -m uvicorn uygulama.main:app --host 127.0.0.1 --port 8000 --reload
```

Adresler:

- Ana sayfa: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/health`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 6. API Örneği

### 6.1 Health

```bash
curl -s http://127.0.0.1:8000/health
```

### 6.2 Predict

```bash
curl -s -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 2,
    "glucose": 148,
    "blood_pressure": 72,
    "skin_thickness": 35,
    "insulin": 0,
    "bmi": 33.6,
    "diabetes_pedigree_function": 0.627,
    "age": 50
  }'
```

Dönüş alanları:

- `olasilik`
- `sinif`
- `risk_kategorisi`
- `top_faktorler`
- `kisa_aciklama`

## 7. Risk Kategorileri

Mevcut eşik yapısı:

- `%0 - %33`: `dusuk`
- `%33 - %66`: `orta`
- `%66 - %100`: `yuksek`

## 8. Güncel Resmî Skorlar (Deploy Çıktısı)

Kaynak: `dokumanlar/resmi_skor_tablosu.md`

| Metrik | Değer |
| --- | --- |
| Accuracy | 0.7727 |
| Precision | 0.6301 |
| Recall | 0.8519 |
| F1 | 0.7244 |
| ROC AUC | 0.8263 |
| Brier | 0.1662 |

## 9. Betikler

### 9.1 Eğitim özeti

```bash
python3 betikler/egitimi_calistir.py
```

### 9.2 Model değerlendirme özeti

```bash
python3 betikler/degerlendirmeyi_calistir.py
```

### 9.3 Resmî skor tablosu üretimi

```bash
python3 betikler/resmi_skor_tablosu_uret.py
```

### 9.4 Veri artırmadan optimizasyon raporu

```bash
python3 betikler/veri_artirmadan_optimizasyon.py
```

Bu betik, veri seti boyutunu artırmadan eşik/kalibrasyon/model kombinasyonlarını tarar ve rapor üretir.

## 10. Testler

```bash
pytest -q
```

## 11. Son Not

Bu proje, akademik/Ar-Ge amaçlı bir karar destek çalışmasıdır.  
Klinik tanı yerine geçmez; tıbbi kararlar için mutlaka uzman hekim değerlendirmesi gerekir.
