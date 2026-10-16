from PIL import Image
from teyitscope.analysis import analyze_file

def test_analysis_report(tmp_path):
    p = tmp_path / "sample.png"
    Image.new("RGB", (32, 24), (120, 80, 60)).save(p)
    report = analyze_file(p, tmp_path / "out")
    assert report.width == 32 and report.height == 24
    assert 0 <= report.manipulation_score <= 100
    assert (tmp_path / "out" / "sample-ela-heatmap.png").exists()
