# Custom dataset manifesti

Eğitim verisini repoya yüklemek zorunda değilsiniz. `manifest.jsonl` her satırda bir görsel ve etiket içermelidir:

```json
{"path":"images/real/001.jpg","label":0}
{"path":"images/manipulated/001.jpg","label":1}
```

`teyitscope train manifest.jsonl --output models/baseline.pkl` komutu açıklanabilir ELA/gürültü özellikleriyle bir baseline eğitir. Gerçek kullanımda kaynak, lisans, kişi rızası, train/test ayrımı ve dış değerlendirme kaydedilmelidir.
