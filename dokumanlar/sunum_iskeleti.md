# Diyabet Risk Tahmini Sunum İskeleti

## 1. Sunum Hedefi

Bu sunumun amacı, projenin teknik doğruluğunu ve iş/etki potansiyelini birlikte göstermek; son bölümde uçtan uca canlı demo ile güven oluşturmaktır.

Ana mesaj:

"Bu çalışma bir klinik tanı sistemi değil; açıklanabilir, test edilebilir ve prototip seviyede bir karar destek sistemidir."

## 2. Akış (21-24 dk + 6-8 dk soru-cevap)

| # | Süre | Slayt Başlığı | Tek Ana Mesaj Cümlesi |
| --- | --- | --- | --- |
| 1 | 1 dk | Kapak ve Ekip | Bu proje, diyabet risk farkındalığı için geliştirilen bir karar destek prototipidir. |
| 2 | 1 dk | Problem Tanımı | Erken risk farkındalığı, klinik yükü azaltabilecek kritik bir ara adımdır. |
| 3 | 1 dk | Amaç ve Kapsam | Proje tanı koymaz; risk olasılığı üretir ve anlaşılır şekilde sunar. |
| 4 | 1.5 dk | Veri Seti | PIMA veri seti, prototip geliştirme için uygun bir başlangıç zemini sağlar. |
| 5 | 1.5 dk | Veri Ön İşleme | 0→NaN, imputasyon ve ölçekleme adımları modelin güvenilirliğini artırır. |
| 6 | 1.5 dk | Model Adayları | Logistic Regression, Random Forest ve XGBoost karşılaştırmalı seçilmiştir. |
| 7 | 1.5 dk | Değerlendirme Metodolojisi | Başarı tek metrikle değil, metrik setiyle değerlendirilmiştir. |
| 8 | 1 dk | Model Seçim Mantığı | Model seçimi AUC/Recall/F1 dengesiyle yapılmıştır. |
| 9 | 1.5 dk | Resmî Deploy Özeti | Deploy metrikleri: Accuracy 0.7532, Recall 0.8519, F1 0.7077, AUC 0.8222, Brier 0.1612. |
| 10 | 1 dk | Hedef Sapması Açıklaması | `%90+ accuracy` hedefi mevcut veri ölçeğinde doğal olarak zorlayıcıdır. |
| 11 | 1 dk | Kalibrasyon Etkisi | Kalibrasyon, olasılık güvenilirliğini artıran temel bileşendir. |
| 12 | 1 dk | Risk Kategorileri | Risk seviyesi `%0-33 düşük`, `%33-66 orta`, `%66-100 yüksek` olarak standarttır. |
| 13 | 1 dk | Açıklanabilirlik | SHAP çıktıları, sonucun nedenini kullanıcıya anlaşılır biçimde gösterir. |
| 14 | 1 dk | Sistem Mimarisi | FastAPI + artifact + Jinja yapısı, prototipin sade ve sürdürülebilir olmasını sağlar. |
| 15 | 1 dk | API Sözleşmesi | `GET /health` ve `POST /predict` ile sistem davranışı nettir ve test edilebilir. |
| 16 | 1 dk | Kalite Güvencesi | `pytest` ve şema doğrulamaları ile temel kalite güvencesi sağlanır. |
| 17 | 1.5 dk | Riskler ve Sınırlılıklar | Veri boyutu ve dış validasyon eksikliği, mevcut sürümün doğal sınırlarıdır. |
| 18 | 1.5 dk | Yol Haritası | Dış veri ve çok merkezli validasyon, bir sonraki kritik gelişim adımıdır. |
| 19 | 1 dk | Ticarileşme Potansiyeli | Kurumsal pilot ile karar destek entegrasyonu uygulanabilir bir yoldur. |
| 20 | 0.5 dk | Demo Çerçevesi | Şimdi sistemi uçtan uca canlı olarak gösteriyoruz. |
| 21 | 4 dk | Uçtan Uca Demo | Girdi, sonuç kartı, risk seviyesi ve API çıktısı arasında birebir tutarlılık vardır. |
| 22 | 1 dk | Kapanış ve Çağrı | Proje teknik olarak çalışır durumdadır ve bir sonraki adım validasyon genişletmesidir. |

## 3. Slayt Bazlı İçerik Notları

### 3.1 Kapak - Problem - Amaç

- Problem cümlesi kısa tutulmalı: "Amaç tanı koymak değil, riski erken görünür kılmak."
- "Klinik tanı yerine geçmez" ifadesi bu bölümde ilk kez söylenmeli.

### 3.2 Veri - Modelleme - Değerlendirme

- Veri seti boyutu açıkça belirtilmeli: `768` kayıt.
- Modellerin neden seçildiği birer cümle ile anlatılmalı.
- Metrikler tek tek ezberlenmek yerine tek tabloda verilmelidir.

### 3.3 Deploy - Kalibrasyon - Risk Kategorisi

- Deploy metrikleri tek slaytta tablo olarak gösterilmeli.
- Kalibrasyon etkisi (Brier öncesi/sonrası) kısa teknik yorumla anlatılmalı.
- Risk eşikleri sözel değil görsel bant ile sunulmalı.

### 3.4 Mimari - API - Test

- Mimariyi 1 diyagram ile anlat: `Form -> API -> Model -> Sonuç Kartı`.
- `POST /predict` giriş/çıkış sözleşmesi net gösterilmeli.
- Testlerin temel amacı: "kırılmayı erken yakalamak".

### 3.5 Sınırlılıklar - Yol Haritası - Kapanış

- `%90+ accuracy` hedef sapması savunması tek cümle: veri ölçeği + dış validasyon ihtiyacı.
- Yol haritası 3 maddede kalmalı: dış veri, özellik zenginleştirme, çok merkezli test.
- Kapanışta net çağrı: "Kurumsal pilot için birlikte ilerleyebiliriz."

## 4. Zorunlu Vurgular (Sunumda Mutlaka Geçmeli)

1. "Bu sistem klinik tanı yerine geçmez." cümlesini en az iki kez kullan.
2. `%90+ accuracy` sorusunda kısa yanıt ver: veri ölçeği, dış validasyon gereksinimi.
3. Deploy metriklerini tek slaytta tablo ile göster.
4. Risk eşiklerini görsel bant ile anlat.
5. Demo için yedek ekran görüntüsü planını hazır tut.

## 5. Geçiş Cümleleri (Akışı Yumuşatmak İçin)

- "Problemden çözüme geçelim; şimdi veriyi nasıl işlediğimizi göstereceğim."
- "Modelleri gördük, şimdi neden bu metrik setiyle karar verdiğimizi paylaşacağım."
- "Teknik resmi çizdik, şimdi sistemi canlıda uçtan uca göstereceğim."
- "Demo sonrası son olarak sınırlar ve bir sonraki adımla kapatacağım."

## 6. Kapanış Metni (Öneri)

"Özetle, bu proje klinik tanı yerine geçmeyen ancak erken risk farkındalığı sağlayan, açıklanabilir ve test edilebilir bir karar destek prototipidir. Teknik olarak çalışır durumdayız; bir sonraki adımımız dış veriyle validasyon kapsamını genişletmek ve kurumsal pilot çalışmaya geçmektir."
