# Çapraz-dataset eğitim sözleşmesi

Gerçek veri setlerini kendi lisans ve izinleriyle dışarıda tutun. Her JSONL satırı `{"path":"...","label":0|1,"dataset":"...","camera":"...","generator":"..."}` olabilir.

Çapraz doğrulama protokolü bir veri kaynağında eğitip diğer veri kaynağında ölçmelidir. Aynı kaynaktan rastgele bölme, modelin kaynağı ezberlemesini gizleyebilir. `cross-dataset.json.example` birden fazla kaynağın nasıl kaydedileceğini gösterir.

AI üretim etiketleri Stable Diffusion, Midjourney, DALL-E gibi üreticiler için ayrı sınıflar taşıyabilir; model adı metadata'dan varsayılmamalı, veri kaynağıyla doğrulanmalıdır. Kullanıcı geri bildirimleri otomatik olarak modele katılmaz; önce `feedback/quarantine.jsonl` içinden insan incelemesi ve lisans kontrolü gerekir.
