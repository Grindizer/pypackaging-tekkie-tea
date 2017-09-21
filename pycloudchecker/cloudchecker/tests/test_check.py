from elbchecker.runner import check_elb


def test_elb_check_crosszone(monkeypatch):
    monkeypatch.setattr('elbchecker.runner.list_load_balancer', lambda x: [])
    assert list(check_elb(None)) == []
