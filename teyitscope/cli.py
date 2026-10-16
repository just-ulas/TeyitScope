import json
from pathlib import Path
import typer
from .analysis import analyze_file
app = typer.Typer(help="TeyitScope görsel adli analiz CLI")
@app.command()
def analyze(image: Path, output: Path = typer.Option(Path("teyitscope-output"), "--output", "-o")):
    """Görseli analiz eder; JSON raporu ve varsa ELA ısı haritası üretir."""
    report = analyze_file(image, output)
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / f"{image.stem}-report.json"
    report_path.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    typer.echo(f"Rapor: {report_path}")
if __name__ == "__main__": app()
