"""Evidence fusion with explicit disagreement handling."""
from __future__ import annotations
from typing import Any
DEFAULT_WEIGHTS={"ela":1.0,"local_splice":2.0,"seam_boundary":5.0,"noise":0.5,"light_shadow":0.5,"ai_generated":2.0,"face_manipulation":2.0}
def fuse_findings(findings:list[dict[str,Any]], weights:dict[str,float]|None=None)->dict[str,Any]:
    weights=weights or DEFAULT_WEIGHTS; evidence=[]
    for item in findings:
        if item.get("status")=="not_configured": continue
        signal=item.get("signal")
        if isinstance(signal,(int,float)):
            evidence.append({"name":item.get("name"),"signal":max(0.,min(1.,float(signal))),"weight":weights.get(item.get("name"),1.)})
    if not evidence: return {"score":0.,"confidence":0.,"active_models":[],"disagreement":0.,"rule":"no_configured_evidence"}
    active=[x for x in evidence if x["signal"]>0.05]; total=sum(x["weight"] for x in evidence)
    weighted=sum(x["signal"]*x["weight"] for x in evidence)/total
    values=[x["signal"] for x in evidence]; disagreement=max(values)-min(values)
    active_ratio=len(active)/len(evidence)
    agreement=1.0-(0.45*disagreement*(1.0-min(1.,active_ratio)))
    confidence=min(1.,0.25+0.75*active_ratio)*(1.0-0.35*disagreement)
    return {"score":round(max(0.,min(1.,weighted*agreement))*100,2),"confidence":round(confidence*100,2),"active_models":[x["name"] for x in active],"disagreement":round(disagreement,4),"agreement_factor":round(agreement,4),"evidence":evidence}
