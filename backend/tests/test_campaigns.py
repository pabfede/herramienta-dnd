def test_campaign_round_trip(client):
    create_resp = client.post("/api/campaigns", json={"name": "Lost Mine"})
    assert create_resp.status_code == 201
    campaign = create_resp.json()
    campaign_id = campaign["id"]
    assert campaign["name"] == "Lost Mine"

    list_resp = client.get("/api/campaigns")
    assert list_resp.status_code == 200
    assert any(c["id"] == campaign_id for c in list_resp.json())

    get_resp = client.get(f"/api/campaigns/{campaign_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Lost Mine"

    patch_resp = client.patch(f"/api/campaigns/{campaign_id}", json={"name": "Phandelver"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["name"] == "Phandelver"

    delete_resp = client.delete(f"/api/campaigns/{campaign_id}")
    assert delete_resp.status_code == 204

    missing_resp = client.get(f"/api/campaigns/{campaign_id}")
    assert missing_resp.status_code == 404


def test_unknown_campaign_404(client):
    resp = client.get("/api/campaigns/does-not-exist")
    assert resp.status_code == 404
    resp = client.patch("/api/campaigns/does-not-exist", json={"name": "x"})
    assert resp.status_code == 404
    resp = client.delete("/api/campaigns/does-not-exist")
    assert resp.status_code == 404


def test_creation_failure_leaves_no_db_file(client, tmp_path, monkeypatch):
    import pytest

    import app.services.campaign_service as campaign_service

    def boom(path):
        raise RuntimeError("migration failed")

    monkeypatch.setattr(campaign_service, "_run_migrations", boom)
    with pytest.raises(RuntimeError):
        client.post("/api/campaigns", json={"name": "Doomed"})
    assert list(tmp_path.glob("*.db")) == []


def test_docs_renders(client):
    resp = client.get("/docs")
    assert resp.status_code == 200
