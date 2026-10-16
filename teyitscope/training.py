"""Small, reproducible baseline trainer for custom image datasets.

Dataset layout: a JSONL manifest with {"path": "...", "label": 0|1}.
This baseline deliberately uses explainable metadata/ELA/noise features. It is
not a replacement for a validated deep-learning forensic model.
"""
from __future__ import annotations
import json, pickle
from pathlib import Path
from typing import Iterable
from PIL import Image, ImageStat
from .analysis import ELAAnalyzer, NoiseAnalyzer

def feature_vector(path: str | Path) -> list[float]:
    image = Image.open(path).convert("RGB")
    ela = ELAAnalyzer().analyze(image)
    noise = NoiseAnalyzer().analyze(image)
    return [float(ela["mean_error"]), float(ela["signal"]), float(noise["global_noise_proxy"]), image.width/ image.height]

def read_manifest(manifest: str | Path):
    base=Path(manifest).parent
    for line in Path(manifest).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"): continue
        row=json.loads(line); yield base / row["path"], int(row["label"])

def train(manifest: str | Path, output: str | Path) -> dict:
    rows=list(read_manifest(manifest))
    if len(rows)<2 or len({label for _,label in rows})<2: raise ValueError("Manifest en az iki örnek ve iki sınıf içermeli")
    X=[feature_vector(path) for path,_ in rows]; y=[label for _,label in rows]
    try:
        from sklearn.ensemble import RandomForestClassifier
        model=RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
        model.fit(X,y); backend="scikit-learn"
    except ImportError:
        # Nearest-centroid fallback keeps the command usable without ML extras.
        centers={label:[sum(row[i] for row,l in zip(X,y) if l==label)/sum(l==label for l in y) for i in range(len(X[0]))] for label in set(y)}
        model={"type":"nearest_centroid","centers":centers}; backend="builtin"
    out=Path(output); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as f: pickle.dump({"model":model,"backend":backend,"features":["ela_mean","ela_signal","noise_proxy","aspect_ratio"]},f)
    return {"samples":len(rows),"backend":backend,"model":str(out)}
