"""Non-invasive provenance and OSINT provider hooks."""
from __future__ import annotations
import hashlib, urllib.parse
from pathlib import Path
from PIL import Image

def _ahash(image:Image.Image)->str:
    g=image.convert("L").resize((8,8)); px=list(g.getdata()); avg=sum(px)/len(px)
    return ''.join('1' if p>=avg else '0' for p in px)

def fingerprint(path:str|Path)->dict:
    p=Path(path); data=p.read_bytes(); image=Image.open(p)
    return {"sha256":hashlib.sha256(data).hexdigest(),"average_hash":_ahash(image),"bytes":len(data),"format":image.format}

def source_lookup_plan(sha256:str)->dict:
    # Providers require a remotely reachable image or API key. Never upload a
    # user's private image automatically; return an explicit, auditable plan.
    q=urllib.parse.quote(sha256)
    return {"status":"not_queried","reason":"privacy_and_provider_credentials_required","fingerprint_query":q,"providers":[{"name":"Google Lens","mode":"manual_upload"},{"name":"Bing Visual Search","mode":"api_key_required"},{"name":"TinEye","mode":"api_key_required"}]}
