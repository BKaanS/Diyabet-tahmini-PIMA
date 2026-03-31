# Diyabet Risk Tahmini

Bu proje, kadin bireylerde diyabet riski icin makine ogrenmesi destekli bir tahmin uygulamasidir.

- Veri seti: Pima Indians Diabetes
- Problem tipi: Binary classification
- Modeller: Logistic Regression, Random Forest, XGBoost
- Backend: FastAPI
- Arayuz: HTML + Jinja2
- Aciklanabilirlik: SHAP (top faktorler)

## 1. Proje Klasorleri

- `uygulama/`: FastAPI, semalar, servisler, HTML/Jinja sablonlari ve statik dosyalar
- `makine_ogrenmesi/`: veri, notebook, kaynak kod, artifact ve rapor klasorleri
- `testler/`: pytest test dosyalari
- `betikler/`: terminalden calistirilacak yardimci betikler
- `dagitim/`: gunicorn, nginx, systemd ve deploy notlari
- `dokumanlar/`: ek proje dokumanlari

## 2. Kurulum

### 2.1 Gereksinimler

- Python 3.10+
- `pip`

### 2.2 Ortam kurulumu

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2.3 Ortam degiskenleri

```bash
cp .env.example .env
```

Varsayilan onemli alanlar:

- `APP_ADI=diyabet-risk-tahmini`
- `APP_ENV=gelistirme`
- `APP_HOST=127.0.0.1`
- `APP_PORT=8000`
- `MODEL_ARTIFACT_KLASORU=makine_ogrenmesi/artifactler`

## 3. Veri Seti Hazirlama

Veri dosyasini su konuma koy:

- `makine_ogrenmesi/veri/ham/diabetes.csv`

Kaynak (Kaggle):

- `https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database`

Dosya adinin `diabetes.csv` olmasi ve zorunlu kolonlari icermesi gerekir.

## 4. Uygulamayi Calistirma

```bash
python3 -m uvicorn uygulama.main:app --host 127.0.0.1 --port 8000 --reload
```

Acilan adresler:

- Ana sayfa: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/health`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 5. API Kullanim Ornegi

### 5.1 Health

```bash
curl -s http://127.0.0.1:8000/health
```

### 5.2 Predict

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

Beklenen donus alanlari:

- `olasilik`
- `sinif`
- `risk_kategorisi`
- `top_faktorler`
- `kisa_aciklama`

## 6. Testleri Calistirma

```bash
pytest -q
```

Beklenen: tum testler `passed`.

## 7. Egitim ve Degerlendirme Betikleri

### 7.1 Egitim ozeti uretme

```bash
python3 betikler/egitimi_calistir.py
```

Cikti dosyasi:

- `makine_ogrenmesi/raporlar/degerlendirme/egitim_ozeti.json`

### 7.2 Model degerlendirme ozeti uretme

```bash
python3 betikler/degerlendirmeyi_calistir.py
```

Cikti dosyasi:

- `makine_ogrenmesi/raporlar/degerlendirme/model_degerlendirme_ozeti.json`

Not:

- Tahmin API'si `makine_ogrenmesi/artifactler/` altindaki artifact dosyalarini kullanir.
- Bu klasorde zorunlu dosyalar (pipeline, kalibrator, esik, metadata) mevcut olmalidir.

## 8. Deploy Dosyalari

Deploy ile ilgili dosyalar:

- `dagitim/gunicorn_conf.py`
- `dagitim/nginx.conf`
- `dagitim/diyabet_risk.service`
- `dagitim/dagitim_notlari.md`

VPS adimlari icin dogrudan:

- `dagitim/dagitim_notlari.md`

## 9. Sik Karsilasilan Durumlar

### 9.1 Port kullanimda

Hata: `Address already in use`

Cozum:

```bash
lsof -i :8000
kill -9 <PID>
```

### 9.2 Veri dosyasi bulunamadi

Hata: `Veri dosyasi bulunamadi: makine_ogrenmesi/veri/ham/diabetes.csv`

Cozum:

- Komutlari proje kokunden calistir.
- Dosyanin gercekten su yolda oldugunu kontrol et:
  - `makine_ogrenmesi/veri/ham/diabetes.csv`

### 9.3 Artifact dosyalari eksik

Hata: `Artifact dosyalari eksik`

Cozum:

- `makine_ogrenmesi/artifactler/` altindaki zorunlu dosyalarin varligini kontrol et.
- `MODEL_ARTIFACT_KLASORU` yolunu `.env` icinde dogrula.

## 10. Son Teknik Kontrol Komutlari

```bash
pytest -q
python3 -m compileall uygulama makine_ogrenmesi testler betikler
```

Bu iki komutun hatasiz bitmesi, temel calisabilirlik ve import tutarliligi icin yeterli son kontroldur.
