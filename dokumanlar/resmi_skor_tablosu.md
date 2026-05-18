# Nihai Model Skor Tablosu

Bu doküman, depoya alınan güncel üretim artifactlerinin performans özetini verir. Eski XGBoost ve veri artırmadan optimizasyon çıktıları bu sürümde resmi skor olarak kullanılmaz.

## 1. Model Özeti

| Alan | Değer |
| --- | --- |
| Nihai model | ExtraTrees |
| Model kodu | `pima_1000_1000_extra_trees_v1` |
| Eğitim verisi | Source ID kontrollü dengelenmiş PIMA sentetik eğitim seti |
| Toplam eğitim satırı | 2000 |
| Sınıf dağılımı | 1000 negatif, 1000 pozitif |
| İkili karar eşiği | 0.45 |
| Risk kategorileri | Düşük, orta, yüksek |

## 2. İç Holdout Sonuçları

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

## 3. GroupCV Özeti

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

## 4. Yorum

Source ID kontrollü doğrulama, aynı özgün örnekten türetilen sentetik kayıtların eğitim ve doğrulama tarafına karışmasını engellemek için kullanılmıştır. Bu nedenle GroupCV sonucu, klasik rastgele bölmeye göre daha ihtiyatlı ve metodolojik olarak daha savunulabilir bir kontrol sağlar.

Harici/orijinal PIMA kontrolü klinik genellenebilirlik kanıtı olarak değil, modelin orijinal veri dağılımı karşısındaki davranışını izleyen ek kontrol olarak değerlendirilmelidir.
