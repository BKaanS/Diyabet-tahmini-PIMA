# Soru-Cevap Kartları (Karma Jüri)

Bu doküman, sunum sonrası sık gelmesi muhtemel sorulara kısa ve net yanıt vermek için hazırlanmıştır.

## 1. "Neden `%90+ accuracy` yok?"

Yanıt:

"Mevcut veri seti 768 kayıtla sınırlı. Bu ölçekte `%90+ accuracy` hedefi iddialı kalıyor. Bu yüzden tek metrik yerine AUC, F1, Recall ve kalibrasyon dengesini koruyan bir yaklaşım benimsedik."

## 2. "Bu sistem tanı koyuyor mu?"

Yanıt:

"Hayır. Sistem klinik tanı yerine geçmez. Amaç risk farkındalığı oluşturmak ve gerektiğinde kullanıcıyı sağlık profesyoneline yönlendirmektir."

## 3. "Neden XGBoost seçtiniz?"

Yanıt:

"Karşılaştırmalı denemelerde AUC/F1 dengesinde güçlü performans verdiği için deploy adayı olarak öne çıktı."

## 4. "Risk kategorileri nasıl belirleniyor?"

Yanıt:

"Olasılık değeri sabit bantlara map ediliyor: `%0-33 düşük`, `%33-66 orta`, `%66-100 yüksek`."

## 5. "Model neden sadece tek metrikle seçilmedi?"

Yanıt:

"Çünkü tek metrik yanıltıcı olabilir. Klinik risk iletişimi için Recall, F1, AUC ve Brier birlikte değerlendirilmeli."

## 6. "Kalibrasyon neyi iyileştirdi?"

Yanıt:

"Kalibrasyon, olasılık tahminlerinin güvenilirliğini artırdı; özellikle Brier metriğinde iyileşme sağlandı."

## 7. "Yanlılık (bias) riski var mı?"

Yanıt:

"Evet, sınırlı ve tek kaynaklı veri nedeniyle bias riski vardır. Bu yüzden dış veri ve çok merkezli validasyon yol haritasında önceliklidir."

## 8. "Gerçek hastane ortamına ne kadar hazır?"

Yanıt:

"Prototip teknik olarak çalışır durumda; klinik kullanım için dış validasyon, regülasyon ve entegrasyon adımları tamamlanmalıdır."

## 9. "SHAP çıktısı iş kararına ne katkı veriyor?"

Yanıt:

"Kullanıcıya sonucun nedenini anlaşılır şekilde gösteriyor. Böylece model çıktısı bir kara kutu olmaktan çıkıyor."

## 10. "Neden bu veri setiyle başladınız?"

Yanıt:

"PIMA, alan literatüründe kabul gören ve prototip geliştirmeyi hızlandıran standart bir başlangıç veri seti olduğu için seçildi."

## 11. "Sistemin en güçlü yönü nedir?"

Yanıt:

"Açıklanabilirlik, API/arayüz tutarlılığı ve test edilebilir bir mimariyle hızlı prototipleme yapılabilmesi."

## 12. "Bir sonraki 3 somut adımınız ne?"

Yanıt:

"Dış veriyle validasyon, özellik setinin klinik olarak zenginleştirilmesi, kurumsal pilot entegrasyon."
