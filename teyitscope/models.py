"""Adapter contracts for real AI/deepfake models."""
from __future__ import annotations
from typing import Any, Protocol
from PIL import Image
class ModelAdapter(Protocol):
    name:str; version:str
    def predict(self,image:Image.Image)->dict[str,Any]: ...
class UnavailableAdapter:
    def __init__(self,name,version="unconfigured"): self.name=name; self.version=version
    def predict(self,image): return {"name":self.name,"version":self.version,"status":"not_configured","probability":None}
class ModelRegistry:
    def __init__(self): self.adapters={}
    def register(self,adapter:ModelAdapter): self.adapters[adapter.name]=adapter
    def predict_all(self,image): return [a.predict(image) for a in self.adapters.values()]
