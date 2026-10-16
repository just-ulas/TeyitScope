# TeyitScope

Kayıt istemeyen kullanım için tasarlanmış, tamamen açık kaynaklı ve **0BSD lisanslı** görsel adli analiz platformu. Kullanıcı hesabı, veritabanı veya kalıcı görsel depolama gerektirmez.

> Sonuçlar karar destek sinyalidir; tek başına bir görselin sahte veya gerçek olduğunu kanıtlamaz. İnsan incelemesi ve kaynak doğrulaması gerekir.

## V2 büyük güncellemesi

- **No-login web UI:** `GET /` tarayıcı arayüzü; görsel yükleyip raporu anında görme.
- **Forensic katman:** JPEG ELA ısı haritası, EXIF/metadata dökümü ve silinmiş metadata uyarısı, gürültü proxy'si.
- **Işık/gölge triage:** 4×4 luminance yayılımı ile açıklanabilir ön sinyal.
- **Yüz/deepfake adapter yüzeyi:** Güvenli model eklentileri için `FaceManipulationAnalyzer` ve AI analyzer kancaları.
- **Eğitilebilir baseline:** JSONL manifestten ELA/gürültü özellikleriyle Random Forest; scikit-learn yoksa yerleşik nearest-centroid fallback.
- **REST API & CLI:** `POST /v1/analyze`, `GET /health`, `teyitscope analyze` ve `teyitscope train`.
- **CI ve mahremiyet:** GitHub Actions testi, SECURITY.md ve görsellerin varsayılan olarak kalıcı tutulmaması.

## Kurulum ve çalıştırma

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,api,ml]"
uvicorn teyitscope.api:app --host 0.0.0.0 --port 8000
```

Tarayıcıdan `http://localhost:8000` adresini açın. Kullanıcı kaydı yoktur.

## CLI

```bash
teyitscope analyze foto.jpg --output ./rapor
```

## Custom dataset ile eğitim

Veri setini repoya göndermek zorunda değilsiniz. `data/README.md` biçimindeki JSONL manifesti hazırlayın:

```json
{"path":"images/real/001.jpg","label":0}
{"path":"images/manipulated/001.jpg","label":1}
```

Sonra:

```bash
teyitscope train manifest.jsonl --output models/baseline.pkl
```

Bu ilk model açıklanabilir bir baseline'dır; gerçek üretim sistemi için ayrı train/test bölümü, veri lisansları, rıza, kalibrasyon, benchmark ve insan değerlendirmesi şarttır. Proje kasıtlı olarak modelin hazır olmadığı yerlerde `not_configured` döndürür; sahte kesinlik üretmez.

## Plugin yaklaşımı

Bir eklenti `Analyzer` protokolündeki `name` ve `analyze(image)` üyelerini uygular. Yüz swap, AI üretim sınıflandırması, optik akış veya fizik tabanlı ışık çözümü bu kancaya bağlanabilir. Eklentiler güvenilmeyen dosyaları çalıştırmamalı; üretim kullanımında sandbox ve kaynak sınırı uygulanmalıdır.

## Platform notu

Public depoları ziyaretçiler genellikle hesapsız görüntüleyebilir; ancak güvenilir forge'lar spam ve kötüye kullanım nedeniyle anonim hesap/repo oluşturmayı desteklemez. Bu nedenle v2'nin asıl kullanıcı deneyimi **kayıtsız web arayüzüdür**. Projeyi Codeberg, SourceHut veya kendi Forgejo sunucunuza taşımak için ilgili hesap/anahtar gerekir; kullanıcı adına sahte veya geçici e-posta hesabı oluşturulmamıştır.

## Lisans ve geliştirme

0BSD. Test: `pytest -q`. Güvenlik ve görsel mahremiyeti için [SECURITY.md](SECURITY.md) dosyasına bakın.
