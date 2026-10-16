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

class NoiseAnalyzer:
    name = "noise"
    def analyze(self, image):
        gray = image.convert("L").resize((min(512, image.width), min(512, image.height)))
        px = list(gray.getdata()); mean = statistics.fmean(px)
        variance = statistics.fmean([(p - mean) ** 2 for p in px])
        return {"name": self.name, "global_noise_proxy": round(math.sqrt(variance), 4),
                "note": "Yerel gürültü haritası için gelişmiş model eklentisi kullanılabilir."}

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
    analyzers = [MetadataAnalyzer(), ELAAnalyzer(), NoiseAnalyzer(), HeuristicAIAnalyzer()]
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
    score = round(min(100.0, (sum(signals) / max(1, len(signals))) * 100), 2)
    return AnalysisReport(str(path), image.width, image.height, findings[0]["fields"], findings, score,
        ["Bu skor karar destek sinyalidir; tek başına görselin sahte olduğunu kanıtlamaz.",
         "AI/deepfake modeli varsayılan olarak etkin değildir."])
