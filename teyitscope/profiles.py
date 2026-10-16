"""Camera/source profiles used as priors, never as proof."""
from __future__ import annotations
from typing import Any
PROFILES={
 "iphone13pro":{"name":"Apple iPhone 13 Pro","maker":"Apple","expected_software":"iOS Camera","notes":"HEIC/JPEG pipeline; EXIF may be stripped by platforms."},
 "generic_jpeg":{"name":"Generic JPEG","maker":None,"expected_software":None,"notes":"No camera-specific prior."},
}
def infer_profile(metadata:dict[str,Any], requested:str|None=None)->dict[str,Any]:
    if requested in PROFILES: return {"id":requested,**PROFILES[requested],"matched":True}
    make=str(metadata.get("Make","")).lower(); model=str(metadata.get("Model","")).lower()
    if "apple" in make and ("13,1" in model or "iphone 13 pro" in model): return {"id":"iphone13pro",**PROFILES["iphone13pro"],"matched":True}
    return {"id":"generic_jpeg",**PROFILES["generic_jpeg"],"matched":False}
