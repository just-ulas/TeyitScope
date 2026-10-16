"""FastAPI adapter and no-login browser UI."""
from pathlib import Path
import tempfile
try:
    from fastapi import FastAPI, File, UploadFile
    from fastapi.responses import FileResponse
except ImportError:
    FastAPI = None
if FastAPI:
    app = FastAPI(title="TeyitScope API", version="0.2.0")
    @app.get("/health")
    def health(): return {"status": "ok", "service": "teyitscope", "version": "0.2.0"}
    @app.get("/")
    def home():
        return FileResponse(Path(__file__).parent.parent / "web" / "index.html")
    @app.post("/v1/analyze")
    async def analyze(upload: UploadFile = File(...)):
        from .analysis import analyze_file
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / (upload.filename or "upload.bin")
            p.write_bytes(await upload.read())
            return analyze_file(p, Path(d) / "out").to_dict()
else:
    app = None
