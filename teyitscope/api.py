"""FastAPI adapter, provenance report and quarantined feedback."""
from pathlib import Path
import tempfile
try:
    from fastapi import FastAPI,File,UploadFile
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
except ImportError: FastAPI=None
if FastAPI:
    app=FastAPI(title="TeyitScope API",version="0.3.0")
    class Feedback(BaseModel): report_id:str; label:str; notes:str=""
    @app.get("/health")
    def health(): return {"status":"ok","service":"teyitscope","version":"0.3.0"}
    @app.get("/")
    def home(): return FileResponse(Path(__file__).parent.parent/"web"/"index.html")
    @app.post("/v1/analyze")
    async def analyze(upload:UploadFile=File(...)):
        from .analysis import analyze_file
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/(upload.filename or "upload.bin"); p.write_bytes(await upload.read()); return analyze_file(p,Path(d)/"out").to_dict()
    @app.post("/v1/feedback")
    def feedback(payload:Feedback):
        from .feedback import FeedbackStore
        return FeedbackStore().add(payload.report_id,payload.label,payload.notes)
else: app=None
