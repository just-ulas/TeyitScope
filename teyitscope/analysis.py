from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Protocol
import json, math, statistics
from PIL import Image, ImageChops, ImageEnhance, ImageStat, ExifTags

class Analyzer(Protocol):
    name: str
    def analyze(self, image: Image.Image) -> dict[str, Any]: ...

@dataclass
class AnalysisReport:
    source: str
    width: int
    height: int
    metadata: dict[str, Any]
    findings: list[dict[str, Any]]
    manipulation_score: float
    limitations: list[str]
    def to_dict(self): return asdict(self)

class MetadataAnalyzer:
    name = "metadata"
    def analyze(self, image):
        raw = image.getexif()
        data = {}
        for key, value in raw.items():
            label = ExifTags.TAGS.get(key, str(key))
            try: data[label] = str(value)
            except Exception: data[label] = "<unreadable>"
        software = data.get("Software")
        warning = not data
        return {"name": self.name, "fields": data, "metadata_missing_or_stripped": warning,
                "warning": "Metadata silinmiş/manipüle edilmiş olabilir" if warning else None,
                "editing_software": software}

class ELAAnalyzer:
    name = "ela"
    def analyze(self, image):
        # JPEG ELA is a forensic signal, not proof. Re-saving at quality 90 exposes
        # relative compression differences as an amplified heatmap.
        import io
        buf = io.BytesIO(); image.convert("RGB").save(buf, "JPEG", quality=90)
        buf.seek(0); recompressed = Image.open(buf).convert("RGB")
        diff = ImageChops.difference(image.convert("RGB"), recompressed)
        stat = ImageStat.Stat(diff)
        mean = sum(stat.mean) / 3
        scale = 10 if mean == 0 else min(30, 255 / mean)
        heatmap = ImageEnhance.Brightness(diff).enhance(scale)
        return {"name": self.name, "mean_error": round(mean, 4),
                "heatmap": heatmap, "signal": min(1.0, mean / 32)}

class LocalSpliceAnalyzer:
    name = "local_splice"
    def analyze(self, image):
        # Tile-level ELA: spliced regions often retain a different recompression
        # footprint than the surrounding image. We report robust relative stats.
        import io
        base = image.convert("RGB").resize((min(1024, image.width), min(1024, image.height)))
        buf = io.BytesIO(); base.save(buf, "JPEG", quality=90); buf.seek(0)
        recompressed = Image.open(buf).convert("RGB")
        diff = ImageChops.difference(base, recompressed)
        w,h=base.size; cols=8; rows=8; vals=[]
        for y in range(rows):
            for x in range(cols):
                tile=diff.crop((x*w//cols,y*h//rows,(x+1)*w//cols,(y+1)*h//rows))
                vals.append(sum(ImageStat.Stat(tile).mean)/3)
        ordered=sorted(vals); median=statistics.median(ordered)
        p95=ordered[max(0,int(len(ordered)*.95)-1)]
        ratio=p95/(median+1e-6)
        # High relative tile contrast is a triage signal; broad natural edges
        # are less suspicious than a concentrated outlier.
        signal=max(0.0,min(1.0,(ratio-1.15)/3.0))
        return {"name": self.name, "tile_median_error": round(median,4),
                "tile_p95_error": round(p95,4), "outlier_ratio": round(ratio,4),
                "signal": signal, "note":"Bölgesel ELA dışlık sinyali; tek başına kanıt değildir."}

class NoiseAnalyzer:
    name = "noise"
    def analyze(self, image):
        gray = image.convert("L").resize((min(512, image.width), min(512, image.height)))
        px = list(gray.getdata()); mean = statistics.fmean(px)
        variance = statistics.fmean([(p - mean) ** 2 for p in px])
        return {"name": self.name, "global_noise_proxy": round(math.sqrt(variance), 4),
                "note": "Yerel gürültü haritası için gelişmiş model eklentisi kullanılabilir."}

class LightShadowAnalyzer:
    name = "light_shadow"
    def analyze(self, image):
        # A transparent baseline: compares luminance gradients in quadrants.
        # It is a triage signal, not a physical-light solver.
        gray = image.convert("L").resize((64, 64))
        q = []
        for y in range(4):
            for x in range(4):
                crop = gray.crop((x*16, y*16, (x+1)*16, (y+1)*16))
                q.append(ImageStat.Stat(crop).mean[0])
        spread = statistics.pstdev(q)
        return {"name": self.name, "quadrant_luminance_spread": round(spread, 4),
                "note": "Gelişmiş ışık/gölge fizik modeli eklenti olarak bağlanabilir."}

class FaceManipulationAnalyzer:
    name = "face_manipulation"
    def analyze(self, image):
        return {"name": self.name, "status": "not_configured", "faces": None,
                "note": "Yüz tespiti/swap modeli güvenli bir model eklentisiyle etkinleştirilebilir."}

class HeuristicAIAnalyzer:
    name = "ai_generated"
    def analyze(self, image):
        return {"name": self.name, "status": "not_configured", "probability": None,
                "note": "Model ağırlığı yüklenmedi; custom dataset/model eklentisi bağlayın."}

class PluginRegistry:
    def __init__(self): self._analyzers: list[Analyzer] = []
    def register(self, analyzer: Analyzer): self._analyzers.append(analyzer)
    def all(self): return list(self._analyzers)

def analyze_file(path: str | Path, output_dir: str | Path | None = None) -> AnalysisReport:
    path = Path(path); image = Image.open(path)
    analyzers = [MetadataAnalyzer(), ELAAnalyzer(), LocalSpliceAnalyzer(), NoiseAnalyzer(), LightShadowAnalyzer(), FaceManipulationAnalyzer(), HeuristicAIAnalyzer()]
    findings = []
    signals = []
    for analyzer in analyzers:
        result = analyzer.analyze(image)
        signals.append(float(result.pop("signal", 0)))
        if "heatmap" in result:
            if output_dir:
                out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
                heat_path = out / f"{path.stem}-ela-heatmap.png"; result["heatmap_path"] = str(heat_path); result["heatmap"].save(heat_path)
            result.pop("heatmap", None)
        findings.append(result)
    score = round(min(100.0, max(signals) * 100), 2)
    return AnalysisReport(str(path), image.width, image.height, findings[0]["fields"], findings, score,
        ["Bu skor karar destek sinyalidir; tek başına görselin sahte olduğunu kanıtlamaz.",
         "AI/deepfake ve yüz modeli varsayılan olarak etkin değildir."])
