# tests/test_pessoa.py
def test_json_invalido(client):
    resp = client.post("/pessoa", data="x", content_type="application/json")
    assert resp.status_code == 400

def test_id_ausente(client):
    resp = client.post("/pessoa", json={})
    assert resp.status_code == 422

def test_id_invalido_tipo(client):
    resp = client.post("/pessoa", json={"id": "1"})
    assert resp.status_code == 422

def test_id_inexistente(client):
    resp = client.post("/pessoa", json={"id": 999})
    assert resp.status_code == 200

def test_registrobr_mock(client, monkeypatch):
    import api_connect as cr

    monkeypatch.setattr(cr, "get_registrobr_avail", lambda domain, timeout=10: "DISPONIVEL")

    resp = client.post("/pessoa", json={"id": 1, "domain": "uol.com.br"})
    assert resp.status_code == 200
    assert resp.get_json()["mensage"] == "DISPONIVEL"
