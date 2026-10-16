# TeyitScope

Açık kaynak, modüler görsel adli analiz ve teyit araç seti. **0BSD** lisanslıdır.

> TeyitScope sonuçları karar destek sinyalidir; tek başına bir görselin sahte veya gerçek olduğunu kanıtlamaz. İnsan incelemesi ve kaynak doğrulaması gerekir.

## Özellikler

- **Piksel ve derinlik analizi:** JPEG ELA ısı haritası, metadata/EXIF dökümü ve eksik metadata uyarısı, gürültü analizi için başlangıç katmanı.
- **AI/deepfake katmanı:** Model adaptörü için `HeuristicAIAnalyzer` arayüzü; yüz swap, ışık/gölge ve AI üretim modelleri eklenti olarak bağlanabilir.
- **Açık entegrasyon:** CLI ve isteğe bağlı FastAPI REST API (`POST /v1/analyze`, `GET /health`).
- **Custom dataset:** Model ağırlıkları ve eğitim pipeline'ı için ayrılmış API yüzeyi; proje içine veri veya model yüklenmez.
- **Plugin mimarisi:** `Analyzer` protokolünü uygulayan sınıflar `PluginRegistry` ile kaydedilebilir.
- **Anlaşılır rapor:** 0–100 manipülasyon şüphesi skoru, bulgular, sınırlılıklar ve ELA heatmap çıktısı.

## Kurulum

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,api]"
```

## CLI

```bash
teyitscope analyze foto.jpg --output ./rapor
# veya: python -m teyitscope.cli analyze foto.jpg
```

## API

```bash
uvicorn teyitscope.api:app --reload
curl -X POST http://localhost:8000/v1/analyze -F "upload=@foto.jpg"
```

## Yol haritası

1. Yerel bölge bazlı noise/ELA heatmap ve görsel raporlayıcı.
2. Model adapter'ları: AI-generated classifier, yüz manipülasyonu ve ışık-gölge tutarlılığı.
3. Dataset manifest standardı, eğitim/evaluasyon komutları ve kalibrasyonlu güven skorları.
4. Plugin keşfi, sandbox politikası, Telegram/Discord örnek botları.
5. Benchmark veri setleri, yanlış-pozitif raporlaması ve tekrarlanabilir değerlendirme.

## Geliştirme

```bash
pytest -q
```

Katkılar memnuniyetle karşılanır. Hassas görselleri izinsiz yüklemeyin; API kullanımında saklama ve erişim politikalarını ayrıca uygulayın.
