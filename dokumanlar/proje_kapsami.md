# Proje Kapsamı

## 1. Proje Özeti

Bu proje, kadın bireylerde Tip-2 diyabet riskini PIMA değişkenleri üzerinden tahmin eden akademik bir karar destek prototipidir. Sistem tanı koymaz; kullanıcının risk düzeyi hakkında farkındalık oluşturur ve sonucu açıklanabilir biçimde sunar.

## 2. Güncel Üretim Yüzeyi

- Backend: FastAPI
- Arayüz: Jinja2, HTML, CSS ve JavaScript
- Model: ExtraTrees tabanlı nihai sınıflandırma hattı
- Eğitim verisi: Source ID kontrollü dengelenmiş PIMA sentetik eğitim seti
- Açıklanabilirlik: SHAP tabanlı kişisel faktör analizi
- Artifact klasörü: `makine_ogrenmesi/artifactler/`

## 3. Kapsam Dahilindeki Çıktılar

- `GET /health`
- `POST /predict`
- Web formu ve sonuç sayfası
- Klinik aralık doğrulaması
- Düşük, orta ve yüksek risk kategorileri
- SHAP tabanlı faktör listesi
- Pytest tabanlı otomatik testler
- Güncel model metadata ve skor tablosu

## 4. Kapsam Dışı Konular

- Klinik tanı veya tedavi önerisi üretme
- Gerçek hasta verisiyle prospektif klinik validasyon
- Hastane bilgi sistemleriyle canlı entegrasyon
- Regülasyon ve tıbbi cihaz sertifikasyon süreçleri
- Üretim seviyesinde kimlik doğrulama, rate limit ve merkezi log altyapısı

## 5. Model ve Doğrulama Notu

Nihai model `pima_1000_1000_extra_trees_v1` koduyla izlenir. Eğitim seti 1000 negatif ve 1000 pozitif örnekten oluşur. Sentetik kayıtların kaynak aldığı özgün örnekler `source_id` ile takip edildiği için doğrulama sırasında aynı kaynak ailesinin kontrolsüz biçimde iki tarafa da dağılması engellenmiştir.

Harici/orijinal PIMA kontrolü, klinik genellenebilirlik kanıtı değil; modelin özgün PIMA dağılımı karşısındaki davranışını izleyen ek kontrol olarak yorumlanmalıdır.

## 6. Kanıt Dosyaları

- `makine_ogrenmesi/artifactler/model_metadata.json`
- `makine_ogrenmesi/artifactler/metrik_ozeti.json`
- `makine_ogrenmesi/artifactler/esik_yapilandirmasi.json`
- `makine_ogrenmesi/raporlar/degerlendirme/nihai_model_degerlendirme_ozeti.json`
- `dokumanlar/resmi_skor_tablosu.md`
- `dokumanlar/test_senaryolari.md`
