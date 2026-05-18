# Test Senaryoları

Bu doküman, teslim öncesi API ve arayüz kontrollerini standartlaştırır.

## Ön Koşullar

```bash
python3 -m uvicorn uygulama.main:app --host 127.0.0.1 --port 8001
```

Testler ve manuel kontroller `3000` portuna dokunmadan yapılmalıdır.

## Referans Geçerli Girdi

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

## API Senaryoları

| Kod | Senaryo | Beklenen Sonuç |
| --- | --- | --- |
| S01 | `GET /health` | HTTP 200 ve `durum=ok` |
| S02 | Geçerli JSON ile `POST /predict` | HTTP 200; `olasilik`, `sinif`, `risk_kategorisi`, `top_faktorler`, `kisa_aciklama` alanları döner |
| S03 | `age=20` | HTTP 422; kullanıcı dostu aralık dışı mesajı döner |
| S04 | `glucose=301` | HTTP 422; kullanıcı dostu aralık dışı mesajı döner |
| S05 | `insulin=0` | HTTP 422; klinik aralık dışı değer reddedilir |
| S06 | Eksik zorunlu alan | HTTP 422; eksik alan mesajı döner |
| S07 | Fazladan alan | HTTP 422; şema dışı alan reddedilir |
| S08 | Sayısal alana metin gönderimi | HTTP 422; sayısal değer mesajı döner |

Beklenen aralık dışı hata mesajı:

```json
{
  "detail": "Girilen değer izin verilen aralığın dışında. Lütfen bilgilerinizi kontrol ediniz."
}
```

## Risk Profili Kontrolleri

### Düşük Risk

```json
{
  "pregnancies": 0,
  "glucose": 90,
  "blood_pressure": 70,
  "skin_thickness": 20,
  "insulin": 80,
  "bmi": 22.0,
  "diabetes_pedigree_function": 0.2,
  "age": 22
}
```

### Orta Risk

```json
{
  "pregnancies": 3,
  "glucose": 135,
  "blood_pressure": 80,
  "skin_thickness": 30,
  "insulin": 140,
  "bmi": 31.0,
  "diabetes_pedigree_function": 0.5,
  "age": 40
}
```

### Yüksek Risk

```json
{
  "pregnancies": 7,
  "glucose": 165,
  "blood_pressure": 86,
  "skin_thickness": 35,
  "insulin": 180,
  "bmi": 36.0,
  "diabetes_pedigree_function": 0.8,
  "age": 52
}
```

## Arayüz Senaryoları

| Kod | Senaryo | Beklenen Sonuç |
| --- | --- | --- |
| UI-01 | Ana sayfa açılır | Form ve hero alanı görünür |
| UI-02 | Geçerli form gönderilir | Sonuç sayfası açılır |
| UI-03 | Aralık dışı değer girilir | Form kullanıcı dostu hata mesajıyla kalır |
| UI-04 | “İlk 5 Faktörü Gör” butonu tıklanır | Kişiye özel faktör listesi görünür |
| UI-05 | Favicon kontrol edilir | Logo sekme ikonunda görünür |
