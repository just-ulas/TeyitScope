import json
from pathlib import Path
import typer
from .analysis import analyze_file
app=typer.Typer(help="TeyitScope görsel adli analiz CLI")
@app.command()
def analyze(image:Path,output:Path=typer.Option(Path("teyitscope-output"),"--output","-o")):
    """Görseli analiz eder ve füzyon/provenance raporu üretir."""
    report=analyze_file(image,output); output.mkdir(parents=True,exist_ok=True); report_path=output/f"{image.stem}-report.json"; report_path.write_text(json.dumps(report.to_dict(),ensure_ascii=False,indent=2),encoding="utf-8"); typer.echo(json.dumps(report.to_dict(),ensure_ascii=False,indent=2)); typer.echo(f"Rapor: {report_path}")
@app.command()
def train(manifest:Path,output:Path=typer.Option(Path("models/teyitscope-baseline.pkl"),"--output","-o")):
    """Tek manifest üzerinde açıklanabilir baseline eğitir."""
    from .training import train as run_train; typer.echo(json.dumps(run_train(manifest,output),ensure_ascii=False,indent=2))
@app.command("cross-dataset")
def cross_dataset(config:Path):
    """Birden fazla veri kaynağını leave-one-dataset-out protokolüyle doğrular."""
    from .training import cross_dataset as run
    data=json.loads(config.read_text(encoding="utf-8")); typer.echo(json.dumps(run(data["datasets"]),ensure_ascii=False,indent=2))
if __name__=="__main__": app()
