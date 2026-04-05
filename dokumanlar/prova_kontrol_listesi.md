# Prova Kontrol Listesi

## 1. Süre ve Akış Kontrolü

- Toplam sunum süresi: `<= 24 dk`
- Soru-cevap için ayrılan süre: `6-8 dk`
- Her slaytta tek ana mesaj cümlesi hazır

## 2. Teknik Hazırlık

- `.venv` aktif
- `pytest -q` çalıştırıldı
- `GET /health` yanıtı alındı
- Uygulama arayüzü açıldı
- Swagger ekranı açık

## 3. Demo Hazırlığı

- Düşük risk senaryosu canlı test edildi
- Yüksek risk senaryosu canlı test edildi
- API doğrulama komutları hazır
- SHAP açıklaması okunacak cümle hazır

## 4. Yedek Plan Hazırlığı

- Sonuç ekranı ekran görüntüleri hazır
- Demo payload’ları yerel dosyada hazır
- Port çakışması çözüm komutları hazır

## 5. Mesaj Disiplini

- "Klinik tanı yerine geçmez" ifadesi en az iki noktada kullanılacak
- `%90+ accuracy` savunma cümlesi kısa ve net
- Yol haritası üç maddeyle kapanışta tekrar edilecek

## 6. Kabul Kriteri

Aşağıdaki koşullar sağlanıyorsa prova başarılı kabul edilir:

1. Tam akış 24 dakikayı geçmedi.
2. Demo iki kez hatasız çalıştı.
3. Bir kez yedek ekran görüntüsü akışıyla prova edildi.
4. En az 10 olası soruya kısa ve net cevap verilebildi.
