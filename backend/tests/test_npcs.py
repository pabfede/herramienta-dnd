def _create_campaign(client):
    resp = client.post("/api/campaigns", json={"name": "Campaign"})
    return resp.json()["id"]


def test_npc_crud(client):
    campaign_id = _create_campaign(client)

    create_resp = client.post(f"/api/campaigns/{campaign_id}/npcs", json={"name": "Gundren"})
    assert create_resp.status_code == 201
    npc_id = create_resp.json()["id"]

    list_resp = client.get(f"/api/campaigns/{campaign_id}/npcs")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    get_resp = client.get(f"/api/campaigns/{campaign_id}/npcs/{npc_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Gundren"

    patch_resp = client.patch(
        f"/api/campaigns/{campaign_id}/npcs/{npc_id}", json={"name": "Sildar"}
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["name"] == "Sildar"

    delete_resp = client.delete(f"/api/campaigns/{campaign_id}/npcs/{npc_id}")
    assert delete_resp.status_code == 204

    missing_resp = client.get(f"/api/campaigns/{campaign_id}/npcs/{npc_id}")
    assert missing_resp.status_code == 404


def test_location_crud(client):
    campaign_id = _create_campaign(client)

    create_resp = client.post(
        f"/api/campaigns/{campaign_id}/locations", json={"name": "Phandalin"}
    )
    assert create_resp.status_code == 201
    location_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/campaigns/{campaign_id}/locations/{location_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Phandalin"


def test_npcs_under_unknown_campaign_404(client):
    resp = client.get("/api/campaigns/does-not-exist/npcs")
    assert resp.status_code == 404
