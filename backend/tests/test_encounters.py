def _create_campaign(client):
    resp = client.post("/api/campaigns", json={"name": "Campaign"})
    return resp.json()["id"]


def _create_npc(client, campaign_id, name, faction=None):
    custom_fields = {"faction": faction} if faction else {}
    resp = client.post(
        f"/api/campaigns/{campaign_id}/npcs",
        json={"name": name, "customFields": custom_fields},
    )
    return resp.json()["id"]


def test_generate_encounter_empty_pool_returns_no_combatants(client):
    campaign_id = _create_campaign(client)

    resp = client.post(
        f"/api/campaigns/{campaign_id}/encounters/generate", json={"size": 3}
    )
    assert resp.status_code == 201
    assert resp.json()["combatants"] == []


def test_generate_encounter_samples_from_npc_pool(client):
    campaign_id = _create_campaign(client)
    _create_npc(client, campaign_id, "Gundren")
    _create_npc(client, campaign_id, "Sildar")

    resp = client.post(
        f"/api/campaigns/{campaign_id}/encounters/generate", json={"size": 2}
    )
    assert resp.status_code == 201
    combatants = resp.json()["combatants"]
    assert len(combatants) == 2
    for combatant in combatants:
        assert combatant["initiative"] is None


def test_generate_encounter_filters_by_faction(client):
    campaign_id = _create_campaign(client)
    _create_npc(client, campaign_id, "Gundren", faction="Harpers")
    _create_npc(client, campaign_id, "Sildar", faction="Zhentarim")

    resp = client.post(
        f"/api/campaigns/{campaign_id}/encounters/generate",
        json={"size": 1, "faction": "Harpers"},
    )
    assert resp.status_code == 201
    combatants = resp.json()["combatants"]
    assert len(combatants) == 1
    assert combatants[0]["name"] == "Gundren"


def test_generate_encounter_faction_with_no_matches_returns_no_combatants(client):
    campaign_id = _create_campaign(client)
    _create_npc(client, campaign_id, "Gundren", faction="Harpers")

    resp = client.post(
        f"/api/campaigns/{campaign_id}/encounters/generate",
        json={"size": 1, "faction": "Zhentarim"},
    )
    assert resp.status_code == 201
    assert resp.json()["combatants"] == []


def test_patch_combatant_initiative(client):
    campaign_id = _create_campaign(client)
    _create_npc(client, campaign_id, "Gundren")

    gen_resp = client.post(
        f"/api/campaigns/{campaign_id}/encounters/generate", json={"size": 1}
    )
    encounter_id = gen_resp.json()["id"]
    combatants = gen_resp.json()["combatants"]
    combatants[0]["initiative"] = 15

    patch_resp = client.patch(
        f"/api/campaigns/{campaign_id}/encounters/{encounter_id}",
        json={"combatants": combatants},
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["combatants"][0]["initiative"] == 15


def test_encounter_404s(client):
    campaign_id = _create_campaign(client)

    missing_resp = client.get(f"/api/campaigns/{campaign_id}/encounters/does-not-exist")
    assert missing_resp.status_code == 404

    patch_missing_resp = client.patch(
        f"/api/campaigns/{campaign_id}/encounters/does-not-exist", json={"notes": "x"}
    )
    assert patch_missing_resp.status_code == 404

    delete_missing_resp = client.delete(
        f"/api/campaigns/{campaign_id}/encounters/does-not-exist"
    )
    assert delete_missing_resp.status_code == 404


def test_encounters_under_unknown_campaign_404(client):
    resp = client.get("/api/campaigns/does-not-exist/encounters")
    assert resp.status_code == 404
