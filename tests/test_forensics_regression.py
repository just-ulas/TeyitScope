from pathlib import Path
from teyitscope.analysis import analyze_file

def test_v4_distinguishes_controlled_splice(tmp_path):
    root = Path(__file__).parents[1]
    genuine = analyze_file(root / "test-assets/reference/target-store-wikimedia.jpg", tmp_path / "genuine")
    fake = analyze_file(root / "test-assets/reference/target-store-manipulated.jpg", tmp_path / "fake")
    assert genuine.manipulation_score < 5
    assert fake.manipulation_score > 20
