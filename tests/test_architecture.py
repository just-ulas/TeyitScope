from teyitscope.fusion import fuse_findings

def test_unconfigured_models_do_not_lower_evidence():
    r=fuse_findings([{"name":"ela","signal":0.1},{"name":"ai_generated","status":"not_configured","signal":0}])
    assert r["evidence"] == [{"name":"ela","signal":0.1,"weight":1.0}]

def test_disagreement_reduces_confidence():
    r=fuse_findings([{"name":"ela","signal":0.9},{"name":"local_splice","signal":0.0}])
    assert r["confidence"] < 100
    assert r["disagreement"] == 0.9
