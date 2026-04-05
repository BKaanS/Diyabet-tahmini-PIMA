# Resmi Skor Tablosu

## 1. Deploy Özeti

- Model: `xgboost`
- Kalibrasyon: `isotonic`
- İkili sınıflama yöntemi: `f1_optimum`
- İkili sınıflama eşiği: `0.3200`

### 1.1 Hedef Uyum Tablosu

| Metrik | Hedef | Gerçekleşen | Durum |
| --- | --- | --- | --- |
| Accuracy | >= 0.9000 | 0.7532 | Sağlanmadı |
| ROC AUC | >= 0.8000 | 0.8222 | Sağlandı |
| F1 | >= 0.7000 | 0.7077 | Sağlandı |
| Brier iyileşme | >= %10.00 | %8.79 | Sağlanmadı |

### 1.2 Deploy Metrikleri

| Metrik | Değer |
| --- | --- |
| Accuracy | 0.7532 |
| Precision | 0.6053 |
| Recall | 0.8519 |
| F1 | 0.7077 |
| ROC AUC | 0.8222 |
| Brier | 0.1612 |

## 2. Kalibrasyon Etkisi

| Kalibrasyon Durumu | Brier |
| --- | --- |
| Kalibrasyon öncesi | 0.1768 |
| Kalibrasyon sonrası | 0.1612 |
| İyileşme oranı | %8.79 |

## 3. Model Karşılaştırma (Test Seti)

| Model | Accuracy | Precision | Recall | F1 | ROC AUC | Brier |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | 0.7403 | 0.6029 | 0.7593 | 0.6721 | 0.8339 | 0.1656 |
| random_forest | 0.7208 | 0.5753 | 0.7778 | 0.6614 | 0.8143 | 0.1725 |
| logistic_regression | 0.7143 | 0.5833 | 0.6481 | 0.6140 | 0.8081 | 0.1828 |

## 4. Dokümandaki Hedefleri Yakalamak İçin Teknik Yol Haritası

1. Veri hacmini artırın: Pima veri seti `768` kayıt olduğu için `%90+ accuracy` hedefi aşırı iddialı kalıyor. Benzer dağılımda en az `3.000+` kayıtlık ek veri, hedef metriklerde anlamlı stabilite sağlar.
2. Özellikleri zenginleştirin: HbA1c, bel çevresi, aile öyküsü detay seviyesi, ilaç kullanımı ve geçmiş gebelik diyabet öyküsü gibi klinik olarak daha ayırt edici değişkenler performansı doğrudan etkiler.
3. Veri kalitesini standartlaştırın: Eksik/0 değerlerin ölçüm kaynaklı mı gerçek sıfır mı olduğu saha bazlı temizlenmeli; etiketleme hataları için en az bir klinik uzmanla çift kontrol yapılmalıdır.
4. Hedefe göre eşik yönetimi uygulayın: F1 odağı için mevcut eşik korunurken, tarama senaryosunda recall odaklı alternatif eşik ayrıca dokümante edilmelidir.
5. Dış doğrulama yapın: Tek veri seti yerine farklı merkezden ayrık bir dış test seti olmadan yüksek metrik iddiası paydaş açısından zayıf kalır.
6. Brier iyileşmesini büyütmek için: Kalibrasyon verisi büyütülüp (ayrı validation katmanı) isotonic/sigmoid seçimi her yeni veri partisinde yeniden yapılmalıdır.
