# Veri Artirmadan Optimizasyon Raporu

## 1. Ozet

- En iyi deney: `xgboost_no_smote`
- Kalibrasyon: `none`
- Esik yontemi: `f1_optimum_dogrulama`
- Esik: `0.3800`

### 1.1 Metrikler

| Metrik | Deger |
| --- | --- |
| Accuracy | 0.7727 |
| Precision | 0.6301 |
| Recall | 0.8519 |
| F1 | 0.7244 |
| ROC AUC | 0.8263 |
| Brier | 0.1662 |
| Brier iyilesme orani | 0.00% |

### 1.2 Hedef Uyum Durumu

| Hedef | Durum |
| --- | --- |
| Accuracy >= 0.90 | Saglanmadi |
| ROC AUC >= 0.80 | Saglandi |
| F1 >= 0.70 | Saglandi |
| Brier iyilesme >= %10 | Saglanmadi |

## 2. Deney Siralamasi (Ilk 10)

| Deney | Kalibrasyon | Esik | F1 | ROC AUC | Brier | Brier iyilesme |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_no_smote | none | 0.380 | 0.7244 | 0.8263 | 0.1662 | 0.00% |
| random_forest_balanced | none | 0.460 | 0.7107 | 0.8250 | 0.1671 | 0.00% |
| xgboost_no_smote | sigmoid | 0.330 | 0.7097 | 0.8289 | 0.1624 | 2.28% |
| random_forest_balanced | sigmoid | 0.335 | 0.7097 | 0.8250 | 0.1639 | 1.94% |
| xgboost_smote | none | 0.400 | 0.7097 | 0.8254 | 0.1693 | 0.00% |
| xgboost_no_smote | isotonic | 0.285 | 0.7077 | 0.8297 | 0.1639 | 1.36% |
| logistic_balanced | none | 0.425 | 0.6977 | 0.8143 | 0.1784 | 0.00% |
| xgboost_smote | isotonic | 0.320 | 0.6875 | 0.8190 | 0.1672 | 1.20% |
| logistic_balanced | sigmoid | 0.295 | 0.6822 | 0.8122 | 0.1725 | 3.34% |
| logistic_balanced | isotonic | 0.300 | 0.6822 | 0.8135 | 0.1748 | 2.01% |

## 3. Not

- Bu rapor yalnizca mevcut veriyle uretilmistir; veri hacmi arttirilmadan elde edilen tavan performansi gosterir.
- %90+ accuracy gibi hedefler icin yalnizca algoritma ayari degil, dis veri ve ozellik zenginlestirme gerekir.
