from app.db import _engine_cache


def test_npcs_isolated_between_campaigns(client):
    campaign_a = client.post("/api/campaigns", json={"name": "A"}).json()["id"]
    campaign_b = client.post("/api/campaigns", json={"name": "B"}).json()["id"]

    client.post(f"/api/campaigns/{campaign_a}/npcs", json={"name": "Alice"})
    client.post(f"/api/campaigns/{campaign_b}/npcs", json={"name": "Bob"})

    npcs_a = client.get(f"/api/campaigns/{campaign_a}/npcs").json()
    npcs_b = client.get(f"/api/campaigns/{campaign_b}/npcs").json()

    assert [n["name"] for n in npcs_a] == ["Alice"]
    assert [n["name"] for n in npcs_b] == ["Bob"]


def test_migration_on_open_after_engine_cache_clear(client):
    campaign_id = client.post("/api/campaigns", json={"name": "Reopen"}).json()["id"]
    client.post(f"/api/campaigns/{campaign_id}/npcs", json={"name": "Persisted"})

    _engine_cache.clear()

    npcs = client.get(f"/api/campaigns/{campaign_id}/npcs").json()
    assert [n["name"] for n in npcs] == ["Persisted"]
