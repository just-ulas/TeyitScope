# TeyitScope mimari notu

```text
upload
  -> immutable fingerprint (sha256 / average hash)
  -> metadata + camera prior
  -> forensic analyzers (ELA / local splice / seam / noise / light)
  -> optional model adapters (AI generation / face swap)
  -> evidence fusion (weighted + disagreement penalty)
  -> report + optional quarantined feedback
  -> human review before retraining
```

Fusion katmanı yalnızca yapılandırılmış model sinyallerini kullanır. `status=not_configured` olan adapter raporda görünür ama score denominator'ına girmez. Bu, bir modelin henüz kurulu olmamasını “doğal kanıt” gibi saymayı engeller.

Cross-dataset eğitimde veri kaynağı, kamera, codec ve generator alanları korunur. Test seti kaynakları eğitim setiyle çakışmamalıdır. Feedback otomatik öğrenme değildir; zehirlenmiş veya telifli verinin üretim modeline girmesini önlemek için karantinadadır.
