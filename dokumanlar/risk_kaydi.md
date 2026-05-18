# Risk Kaydı

Bu doküman, teslim edilecek akademik prototip için kalan teknik ve metodolojik riskleri özetler.

| Risk No | Risk Tanımı | Olasılık | Etki | Güncel Durum | Aksiyon / Not |
| --- | --- | --- | --- | --- | --- |
| R-01 | Modelin klinik genellenebilirliğinin yalnız PIMA tabanlı veriyle sınırlı kalması | Orta | Yüksek | Açık | Sunum ve README içinde sistemin tanı aracı olmadığı açıkça belirtilir. |
| R-02 | Sentetik veri nedeniyle doğrulama şişmesi algısı | Orta | Yüksek | Azaltıldı | Source ID kontrollü GroupCV sonucu ve maksimum source intersection = 0 bilgisi raporlanır. |
| R-03 | Web arayüzüne gerçekçi olmayan klinik değer girilmesi | Düşük | Orta | Azaltıldı | API ve form alanlarında aynı aralık kuralları uygulanır. |
| R-04 | SHAP açıklamalarının son kullanıcı tarafından klinik neden-sonuç gibi yorumlanması | Orta | Orta | Azaltıldı | Sonuç sayfasında açıklamaların model katkısı olduğu vurgulanır. |
| R-05 | Lokal ortam ve port çakışmaları nedeniyle demo kesintisi | Orta | Orta | Açık | Demo öncesi `pytest -q`, `/health` ve alternatif port kontrolü yapılır. |
| R-06 | Üretim seviyesi güvenlik kontrollerinin prototipte bulunmaması | Orta | Orta | Kabul Edildi | API key, rate limit ve güvenlik headerları akademik prototip kapsamı dışında bırakılmıştır. |

## İzleme Kuralı

Teslim öncesinde açık kalan riskler sunumda sınırlılık olarak anlatılmalı; model çıktısının klinik karar yerine farkındalık amaçlı olduğu özellikle belirtilmelidir.
