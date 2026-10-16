"""Reproducible baseline and leave-one-dataset-out training utilities."""
from __future__ import annotations
import json,pickle
from pathlib import Path
from .analysis import ELAAnalyzer,NoiseAnalyzer

def feature_vector(path):
    from PIL import Image
    image=Image.open(path).convert("RGB"); ela=ELAAnalyzer().analyze(image); noise=NoiseAnalyzer().analyze(image)
    return [float(ela["mean_error"]),float(ela["signal"]),float(noise["global_noise_proxy"]),image.width/image.height]
def read_manifest(manifest):
    base=Path(manifest).parent
    for line in Path(manifest).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"): continue
        row=json.loads(line); yield base/row["path"],int(row["label"]),row.get("dataset",base.name)
def train(manifest,output):
    rows=list(read_manifest(manifest))
    if len(rows)<2 or len({r[1] for r in rows})<2: raise ValueError("Manifest en az iki örnek ve iki sınıf içermeli")
    X=[feature_vector(p) for p,_,_ in rows]; y=[label for _,label,_ in rows]
    try:
        from sklearn.ensemble import RandomForestClassifier
        model=RandomForestClassifier(n_estimators=100,random_state=42,class_weight="balanced"); model.fit(X,y); backend="scikit-learn"
    except ImportError:
        centers={label:[sum(row[i] for row,l in zip(X,y) if l==label)/sum(l==label for l in y) for i in range(len(X[0]))] for label in set(y)}; model={"type":"nearest_centroid","centers":centers}; backend="builtin"
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("wb") as f: pickle.dump({"model":model,"backend":backend,"features":["ela_mean","ela_signal","noise_proxy","aspect_ratio"]},f)
    return {"samples":len(rows),"datasets":sorted({r[2] for r in rows}),"backend":backend,"model":str(out)}
def cross_dataset(manifests:dict[str,str|Path])->dict:
    groups={name:list(read_manifest(path)) for name,path in manifests.items()}
    if len(groups)<2: raise ValueError("Çapraz doğrulama için en az iki ayrı dataset gerekir")
    return {"protocol":"leave_one_dataset_out","datasets":{name:{"samples":len(rows),"labels":sorted({r[1] for r in rows})} for name,rows in groups.items()},"status":"manifest_validated","next_step":"train on all groups except one and evaluate on the held-out group"}
