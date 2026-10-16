# TeyitScope

Kayıt istemeyen, tamamen açık kaynaklı ve **0BSD** lisanslı görsel adli inceleme aracı. Arayüz özellikle süssüzdür: koyu teknik panel, net tipografi ve ham kanıt raporu.

> Skor karar destek sinyalidir. Hiçbir otomatik yöntem tek başına görselin gerçekliğini kanıtlamaz.

## V0.3 mimari güncellemesi

- **Cross-dataset eğitim sözleşmesi:** Kaynaklar arası train/test ayrımı ve leave-one-dataset-out manifest protokolü. Veri setleri lisans ve izinleriyle dışarıda tutulur.
- **Model fusion:** ELA, bölgesel splice, seam, noise, ışık/gölge ve gelecekte bağlanacak AI/yüz modelleri ağırlıklı olarak birleştirilir. `not_configured` modeller skoru yapay biçimde düşürmez. Kanıtlar ayrıştığında `confidence` azalır.
- **AI/deepfake adapter sistemi:** `teyitscope.models.ModelAdapter` ile Stable Diffusion, Midjourney, DALL-E, yüz-swap ve diğer doğrulanmış modeller bağlanabilir. Ağırlık yokken sistem kesinlik uydurmaz.
- **Provenance:** SHA-256, average hash, boyut ve format parmak izi rapora eklenir.
- **OSINT planı:** Google Lens, Bing Visual Search ve TinEye için açık sağlayıcı kancaları var; özel görseller API anahtarı veya açık izin olmadan otomatik yüklenmez.
- **Kamera profilleri:** iPhone 13 Pro ve generic JPEG profilleri priors olarak bulunur; metadata yokluğu kamera kanıtı sayılmaz.
- **Geri bildirim döngüsü:** `/v1/feedback` verileri karantina JSONL’sine yazar. İnsan incelemesi ve lisans kontrolü olmadan modele katılmaz.
- **Minimal panel:** Kart, neon, renkli alarm kutusu veya grafik dashboard yok; düz siyah zemin ve teknik rapor.

## Çalıştırma

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,api,ml]"
uvicorn teyitscope.api:app --host 0.0.0.0 --port 8000
```

Tarayıcıda `http://localhost:8000` adresini açın. Kullanıcı kaydı yoktur.

## API

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/v1/analyze -F "upload=@foto.jpg"
curl -X POST http://localhost:8000/v1/feedback \
  -H 'Content-Type: application/json' \
  -d '{"report_id":"sha256-or-case-id","label":"uncertain","notes":"İnsan incelemesi bekliyor"}'
```

## Eğitim

Tek dataset baseline:

```bash
teyitscope train manifest.jsonl --output models/baseline.pkl
```

Çapraz dataset manifest doğrulaması:

```bash
teyitscope cross-dataset data/cross-dataset.json
```

`data/README.md` ve `data/cross-dataset.json.example` gerçek verinin nasıl kaydedileceğini anlatır. Bu depo büyük lisanslı veri setlerini veya model ağırlıklarını izinsiz içermez. Gerçek AI/deepfake eğitimi için veri lisansı, kaynak dengesi, kamera/codec çeşitliliği, üretici çeşitliliği ve dış test seti gereklidir.

## Test

```bash
pytest -q
```

Kontrollü testte Wikimedia referans fotoğrafı v4/v5 motorunda düşük, bilerek nesne eklenmiş sürüm yüksek sinyal üretmiştir. Bu, yalnızca belirgin splice senaryosu için regresyon kanıtıdır; profesyonel retouch ve tüm üretici modelleri için doğruluk garantisi değildir.

## Gizlilik ve lisans

Görseller varsayılan olarak kalıcı tutulmaz. OSINT sağlayıcılarına otomatik görsel gönderilmez. Üretim kurulumunda dosya boyutu, MIME doğrulaması, rate limit, geçici dosya temizliği ve erişim politikaları ekleyin. Lisans: **0BSD**.
