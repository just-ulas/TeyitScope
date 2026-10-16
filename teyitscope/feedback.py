"""Quarantined feedback store; labels never alter production models directly."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
import json,uuid
class FeedbackStore:
    def __init__(self,path="feedback/quarantine.jsonl"): self.path=Path(path)
    def add(self,report_id:str,label:str,notes:str="",source="anonymous"):
        if label not in {"real","manipulated","uncertain"}: raise ValueError("label must be real, manipulated or uncertain")
        self.path.parent.mkdir(parents=True,exist_ok=True)
        row={"id":str(uuid.uuid4()),"report_id":report_id,"label":label,"notes":notes[:2000],"source":source,"created_at":datetime.now(timezone.utc).isoformat(),"status":"quarantined"}
        with self.path.open("a",encoding="utf-8") as f: f.write(json.dumps(row,ensure_ascii=False)+"\n")
        return row
