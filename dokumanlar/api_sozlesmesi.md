# API Sözleşmesi

Bu doküman, güncel FastAPI uygulamasında sunulan temel endpointleri ve giriş doğrulama kurallarını özetler.

## 1. Genel Bilgiler

- Yerel base URL: `http://127.0.0.1:8000`
- İçerik tipi: `application/json`
- Kimlik doğrulama: Yok; akademik prototip kapsamındadır.
- API dokümantasyonu: `/docs` ve `/redoc`

## 2. Endpointler

### `GET /health`

Uygulama sürecinin çalıştığını doğrular.

```json
{
  "durum": "ok",
  "uygulama": "diyabet-risk-tahmini",
  "ortam": "gelistirme"
}
```

### `POST /predict`

Tek kullanıcı girdisi için kalibre edilmiş diyabet risk tahmini üretir.

Örnek istek:

```json
{
  "pregnancies": 2,
  "glucose": 148,
  "blood_pressure": 72,
  "skin_thickness": 35,
  "insulin": 120,
  "bmi": 33.6,
  "diabetes_pedigree_function": 0.627,
  "age": 50
}
```

Başarılı yanıtta şu alanlar döner:

| Alan | Açıklama |
| --- | --- |
| `olasilik` | 0-1 aralığında kalibre edilmiş risk olasılığı |
| `sinif` | İkili sınıf tahmini |
| `risk_kategorisi` | `dusuk`, `orta` veya `yuksek` |
| `top_faktorler` | SHAP tabanlı öne çıkan kişisel faktörler |
| `kisa_aciklama` | Sonuca eşlik eden kısa açıklama |

## 3. Giriş Alanları

| Alan | Açıklama | Kabul edilen aralık |
| --- | --- | --- |
| `pregnancies` | Gebelik sayısı | 0-17 |
| `glucose` | Plazma glikoz konsantrasyonu | 50-300 mg/dL |
| `blood_pressure` | Diyastolik kan basıncı | 40-130 mmHg |
| `skin_thickness` | Triceps deri kıvrım kalınlığı | 7-70 mm |
| `insulin` | 2 saatlik serum insülin değeri | 10-850 µU/mL |
| `bmi` | Vücut kitle indeksi | 15-70 kg/m² |
| `diabetes_pedigree_function` | Ailesel diyabet yatkınlığı katsayısı | 0.05-2.5 |
| `age` | Yaş | 21-90 |

Aralık dışı girişlerde API `422` döndürür:

```json
{
  "detail": "Girilen değer izin verilen aralığın dışında. Lütfen bilgilerinizi kontrol ediniz."
}
```

## 4. Risk Kategorileri

| Olasılık aralığı | API etiketi |
| --- | --- |
| 0.00-0.33 | `dusuk` |
| 0.33-0.66 | `orta` |
| 0.66-1.00 | `yuksek` |
