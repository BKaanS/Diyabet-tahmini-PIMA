# Değişim Kaydı

Bu dosya, proje kapsamını etkileyen önemli kararların kısa izini tutar.

## 2026-05-18

### Teslim Öncesi Temizlik

- Eski XGBoost/veri artırmadan optimizasyon dokümanı kaldırıldı.
- Resmi skor tablosu güncel ExtraTrees üretim artifactine göre yeniden yazıldı.
- API sözleşmesi, test senaryoları ve risk kaydı güncel klinik aralık doğrulamalarıyla eşitlendi.
- Artifact üretim özetindeki yerel mutlak dosya yolları göreli proje yollarına çevrildi.
- `.gitignore` içine geçici klasör ve bozuk git yedek klasörü kuralları eklendi.
- `pyproject.toml` içine ruff ve mypy yapılandırması eklendi.

## 2026-05-17

### Nihai Modelin Taşınması

- Nihai üretim modeli `pima_1000_1000_extra_trees_v1` koduyla asıl projeye alındı.
- Dengelenmiş PIMA sentetik eğitim seti ve metadata dosyaları temiz adlarla eklendi.
- Pickle bağımlılığında deneysel modül adı yerine `makine_ogrenmesi/kaynak/pima_özellik_dönüşümleri.py` kullanılmaya başlandı.
- Claude ile yenilenen arayüz, favicon ve sonuç sayfası asıl projeye taşındı.

## 2026-04-05

### İlk Prototip Standardizasyonu

- Risk kategorileri düşük, orta ve yüksek olmak üzere üç seviyede standardize edildi.
- FastAPI endpointleri, temel testler ve proje dokümanları oluşturuldu.

## Not

Bu değişim kaydı commit geçmişinin yerine geçmez; karar ve kapsam izini kısa biçimde tamamlar.
