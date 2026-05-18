# Kadın Bireylerde Tip-2 Diyabet Riski Tahmini

Bu proje, Pima Indians Diabetes veri seti temel alınarak kadın bireylerde Tip-2 diyabet riskini tahmin etmek amacıyla geliştirilmiş akademik bir makine öğrenmesi ve web uygulaması çalışmasıdır. Uygulama, kullanıcıdan alınan sekiz klinik parametre üzerinden diyabet risk olasılığını, risk kategorisini ve tahmine en çok etki eden değişkenleri üretir.

Bu sistem bir klinik tanı aracı değildir. Üretilen sonuçlar yalnızca karar destek, farkındalık ve akademik değerlendirme amacıyla kullanılmalıdır. Tıbbi kararlar için uzman hekim değerlendirmesi gerekir.

## Proje Kapsamı

- Problem tipi: İkili sınıflandırma
- Veri tabanı: Pima Indians Diabetes veri seti
- Nihai model: ExtraTrees tabanlı sınıflandırma hattı
- Eğitim yaklaşımı: Dengelenmiş PIMA sentetik eğitim seti
- Açıklanabilirlik: SHAP tabanlı kişisel faktör analizi
- Backend: FastAPI
- Arayüz: HTML, Jinja2, CSS ve JavaScript
- API dokümantasyonu: Swagger UI ve ReDoc

## Akademik Yaklaşım

Çalışmada yalnızca model başarımını artırmak değil, doğrulama sürecinin metodolojik olarak savunulabilir olması hedeflenmiştir. Bu nedenle sentetik veri üretiminden sonra veri sızıntısı riskini azaltmak için `source_id` kontrollü doğrulama mantığı kullanılmıştır. Aynı özgün kaynaktan türetilen sentetik örneklerin eğitim ve doğrulama bölümlerine kontrolsüz biçimde dağılması engellenmiştir.

Nihai model, dengelenmiş PIMA eğitim senaryosu üzerinde üretilmiş ve kalibre edilmiş olasılık çıktısı verecek şekilde yapılandırılmıştır. Modelin çıktıları doğrudan klinik tanı olarak değil, risk düzeyi göstergesi olarak yorumlanmalıdır.

## Nihai Model

| Alan | Değer |
| --- | --- |
| Model | ExtraTrees |
| Model kodu | `pima_1000_1000_extra_trees_v1` |
| Eğitim verisi | Dengelenmiş PIMA sentetik eğitim seti |
| Toplam eğitim satırı | 2000 |
| Sınıf dağılımı | 1000 negatif, 1000 pozitif |
| İkili karar eşiği | 0.45 |
| Risk kategorileri | Düşük, orta, yüksek |
| Artifact klasörü | `makine_ogrenmesi/artifactler/` |

Model artifact bilgileri `model_metadata.json`, `metrik_ozeti.json`, `esik_yapilandirmasi.json` ve `ozellik_sirasi.json` dosyalarında tutulur.

## Model Performansı

Aşağıdaki değerler mevcut deploy artifact dosyalarındaki benchmark holdout çıktısından alınmıştır.

| Metrik | Değer |
| --- | ---: |
| Accuracy | 0.9393 |
| Precision | 0.9431 |
| Recall / Sensitivity | 0.9343 |
| Specificity | 0.9442 |
| F1 | 0.9387 |
| ROC AUC | 0.9860 |
| Balanced Accuracy | 0.9392 |
| MCC | 0.8785 |
| Brier | 0.0459 |

Konfüzyon matrisi:

|  | Tahmin: Negatif | Tahmin: Pozitif |
| --- | ---: | ---: |
| Gerçek: Negatif | 203 | 12 |
| Gerçek: Pozitif | 14 | 199 |

GroupCV özet değerleri:

| Metrik | Ortalama |
| --- | ---: |
| Accuracy | 0.9180 |
| Precision | 0.9093 |
| Recall | 0.9290 |
| Specificity | 0.9070 |
| F1 | 0.9189 |
| ROC AUC | 0.9785 |
| Balanced Accuracy | 0.9180 |
| MCC | 0.8365 |
| Brier | 0.0561 |
| Maksimum source intersection | 0 |

Not: Bu değerler sentetik destekli PIMA deney tasarımına aittir. Harici/orijinal PIMA kontrolü klinik genellenebilirlik kanıtı olarak değil, model davranışını izlemek için ek kontrol olarak değerlendirilmelidir.

## Kullanılan Girdiler

Model sekiz temel PIMA değişkeniyle çalışır:

| API alanı | Açıklama | Kabul edilen aralık |
| --- | --- | --- |
| `pregnancies` | Gebelik sayısı | 0-17 |
| `glucose` | Plazma glikoz konsantrasyonu | 50-300 mg/dL |
| `blood_pressure` | Diyastolik kan basıncı | 40-130 mmHg |
| `skin_thickness` | Triceps deri kıvrım kalınlığı | 7-70 mm |
| `insulin` | 2 saatlik serum insülin değeri | 10-850 µU/mL |
| `bmi` | Vücut kitle indeksi | 15-70 kg/m² |
| `diabetes_pedigree_function` | Ailesel diyabet yatkınlığı katsayısı | 0.05-2.5 |
| `age` | Yaş | 21-90 |

Bu sınırlar hem web formunda hem de `/predict` API doğrulamasında uygulanır. Aralık dışı değerlerde API `422` durum kodu ile anlaşılır bir hata mesajı döndürür.

## Risk Kategorileri

Model, kalibre edilmiş olasılık değerini üç seviyeli risk kategorisine dönüştürür:

| Olasılık aralığı | Risk kategorisi |
| --- | --- |
| 0.00-0.33 | Düşük risk |
| 0.33-0.66 | Orta risk |
| 0.66-1.00 | Yüksek risk |

İkili sınıflandırma için önerilen karar eşiği `0.45` olarak yapılandırılmıştır.

## Klasör Yapısı

```text
uygulama/              FastAPI uygulaması, API rotaları, servisler, şemalar ve arayüz dosyaları
makine_ogrenmesi/      Veri, modelleme kaynak kodları, artifact dosyaları ve raporlar
betikler/              Güncel nihai model artifact üretim betiği
testler/               Pytest tabanlı testler
dokumanlar/            Proje dokümanları ve değerlendirme çıktıları
dagitim/               Dağıtım yapılandırmaları
```

## Kurulum

Python 3.10 veya üzeri bir sürüm önerilir.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Önemli ortam değişkenleri:

```text
APP_ADI=diyabet-risk-tahmini
APP_ENV=gelistirme
APP_HOST=127.0.0.1
APP_PORT=8000
MODEL_ARTIFACT_KLASORU=makine_ogrenmesi/artifactler
```

## Uygulamayı Çalıştırma

```bash
python3 -m uvicorn uygulama.main:app --host 127.0.0.1 --port 8000 --reload
```

Yerel adresler:

| Alan | URL |
| --- | --- |
| Web arayüzü | `http://127.0.0.1:8000/` |
| Health endpoint | `http://127.0.0.1:8000/health` |
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |

## API Kullanımı

Health kontrolü:

```bash
curl -s http://127.0.0.1:8000/health
```

Tahmin örneği:

```bash
curl -s -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 4,
    "glucose": 170,
    "blood_pressure": 90,
    "skin_thickness": 32,
    "insulin": 170,
    "bmi": 33.0,
    "diabetes_pedigree_function": 0.65,
    "age": 48
  }'
```

Başlıca dönüş alanları:

| Alan | Açıklama |
| --- | --- |
| `olasilik` | Kalibre edilmiş diyabet risk olasılığı |
| `sinif` | İkili sınıf tahmini |
| `risk_kategorisi` | Düşük, orta veya yüksek risk |
| `top_faktorler` | SHAP tabanlı en etkili değişkenler |
| `kisa_aciklama` | Sonuç için kısa kullanıcı açıklaması |

Örnek hata dönüşü:

```json
{
  "detail": "Girilen değer izin verilen aralığın dışında. Lütfen bilgilerinizi kontrol ediniz."
}
```

## Açıklanabilirlik

Sonuç sayfasında modelin kararına en çok etki eden değişkenler SHAP katkılarıyla birlikte gösterilir. Kullanıcıya ilk aşamada en etkili faktörler sunulur; ek bölümde kişiye özel ilk beş faktör listelenir.

Bu açıklamalar modelin karar mantığını şeffaflaştırmak için kullanılır. Klinik yorum yerine geçmez.

## Testler

```bash
pytest -q
```

Son doğrulamada uygulama testleri başarıyla geçmiştir. API doğrulaması, risk mantığı, artifact yükleme ve tahmin servisi testleri test kapsamındadır.

## Akademik Sınırlılıklar

- PIMA veri seti sınırlı örneklem büyüklüğüne ve belirli popülasyon özelliklerine sahiptir.
- Sentetik veri kullanımı model dengesini artırır; ancak gerçek klinik veri yerine geçmez.
- Harici/orijinal PIMA kontrolü genellenebilirlik kanıtı değil, ek davranış kontrolü olarak yorumlanmalıdır.
- Model çıktıları hekim değerlendirmesi olmadan tanı veya tedavi kararı için kullanılmamalıdır.

## Lisans ve Kullanım Notu

Bu çalışma akademik bitirme projesi kapsamında geliştirilmiştir. Sağlık alanında gerçek kullanım için ek klinik doğrulama, etik değerlendirme ve yasal uygunluk süreçleri gereklidir.
