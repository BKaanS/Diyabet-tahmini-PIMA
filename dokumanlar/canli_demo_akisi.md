# Canlı Demo Akışı ve Yedek Plan

## 1. Demo Amacı

Canlı demoda, aynı girdinin hem arayüzde hem API çıktısında tutarlı şekilde işlendiğini göstermek.

## 2. Demo Öncesi Kontrol (T-15 dk)

1. Sanal ortam aktif:
   - `source .venv/bin/activate`
2. Uygulama ayağa kalkıyor:
   - `python3 -m uvicorn uygulama.main:app --host 127.0.0.1 --port 8000 --reload`
3. Sağlık kontrolü:
   - `curl -s http://127.0.0.1:8000/health`
4. Tarayıcı sekmeleri hazır:
   - `http://127.0.0.1:8000/`
   - `http://127.0.0.1:8000/docs`

## 3. Senaryo 1 - Düşük Risk (Yeşil Gösterge)

### 3.1 UI Girdisi

- pregnancies: `1`
- glucose: `85`
- blood_pressure: `66`
- skin_thickness: `29`
- insulin: `0`
- bmi: `26.6`
- diabetes_pedigree_function: `0.351`
- age: `31`

Beklenen çıktı (yaklaşık):

- olasilik: `%1.96`
- risk_kategorisi: `dusuk`
- sinif: `0`

### 3.2 API Doğrulaması

```bash
curl -s -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 1,
    "glucose": 85,
    "blood_pressure": 66,
    "skin_thickness": 29,
    "insulin": 0,
    "bmi": 26.6,
    "diabetes_pedigree_function": 0.351,
    "age": 31
  }'
```

## 4. Senaryo 2 - Yüksek Risk (Kırmızı Gösterge)

### 4.1 UI Girdisi

- pregnancies: `6`
- glucose: `178`
- blood_pressure: `90`
- skin_thickness: `35`
- insulin: `0`
- bmi: `38.2`
- diabetes_pedigree_function: `0.79`
- age: `52`

Beklenen çıktı (yaklaşık):

- olasilik: `%90.60`
- risk_kategorisi: `yuksek`
- sinif: `1`

### 4.2 API Doğrulaması

```bash
curl -s -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 6,
    "glucose": 178,
    "blood_pressure": 90,
    "skin_thickness": 35,
    "insulin": 0,
    "bmi": 38.2,
    "diabetes_pedigree_function": 0.79,
    "age": 52
  }'
```

## 5. Demo Sırasında Söylenecek Kısa Metin

- "Aynı girdiyi önce arayüzde, sonra API’de çalıştırıyorum; çıktılar birebir tutarlı."
- "Risk seviyesi, olasılığa göre düşük-orta-yüksek bandına otomatik yerleşiyor."
- "Bu sistem klinik tanı aracı değildir; karar destek ve farkındalık amacı taşır."

## 6. Yedek Plan (Teknik Aksama Durumu)

1. Sunucu açılmazsa:
   - Önceden alınmış sonuç ekran görüntülerini göster.
2. Port çakışırsa:
   - `lsof -i :8000`
   - `kill -9 <PID>`
3. Bağımlılık sorunu olursa:
   - `.venv/bin/python` ile komutları çalıştır.
4. İnternet kesintisinde:
   - Local sunum akışına devam et; Swagger ve UI local çalışır.

## 7. Demo Kabul Kriteri

- Düşük risk ve yüksek risk senaryoları hatasız çalışmalı.
- En az bir senaryoda SHAP tabanlı "en belirgin faktör" cümlesi okunmalı.
- UI ve API tutarlılığı en az bir kez canlı gösterilmeli.
