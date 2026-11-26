def _create_campaign(client):
    resp = client.post("/api/campaigns", json={"name": "Campaign"})
    return resp.json()["id"]


def _create_npc(client, campaign_id, name="Gundren"):
    resp = client.post(f"/api/campaigns/{campaign_id}/npcs", json={"name": name})
    return resp.json()["id"]


def _create_faction(client, campaign_id, name="Harpers"):
    resp = client.post(f"/api/campaigns/{campaign_id}/factions", json={"name": name})
    return resp.json()["id"]


def test_session_crud(client):
    campaign_id = _create_campaign(client)

    create_resp = client.post(
        f"/api/campaigns/{campaign_id}/sessions",
        json={"name": "Session 1", "notes": "The party arrives in Phandalin"},
    )
    assert create_resp.status_code == 201
    session_id = create_resp.json()["id"]
    assert create_resp.json()["notes"] == "The party arrives in Phandalin"

    list_resp = client.get(f"/api/campaigns/{campaign_id}/sessions")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    patch_resp = client.patch(
        f"/api/campaigns/{campaign_id}/sessions/{session_id}", json={"notes": "Updated notes"}
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["notes"] == "Updated notes"

    delete_resp = client.delete(f"/api/campaigns/{campaign_id}/sessions/{session_id}")
    assert delete_resp.status_code == 204

    missing_resp = client.get(f"/api/campaigns/{campaign_id}/sessions/{session_id}")
    assert missing_resp.status_code == 404


def test_link_crud(client):
    campaign_id = _create_campaign(client)
    npc_id = _create_npc(client, campaign_id)
    faction_id = _create_faction(client, campaign_id)

    create_resp = client.post(
        f"/api/campaigns/{campaign_id}/links",
        json={
            "kindA": "npc",
            "idA": npc_id,
            "kindB": "faction",
            "idB": faction_id,
            "relation": "member",
        },
    )
    assert create_resp.status_code == 201
    link_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/api/campaigns/{campaign_id}/links/{link_id}")
    assert delete_resp.status_code == 204

    missing_delete_resp = client.delete(f"/api/campaigns/{campaign_id}/links/{link_id}")
    assert missing_delete_resp.status_code == 404


def test_link_symmetry_appears_in_both_entities_backlinks(client):
    campaign_id = _create_campaign(client)
    npc_id = _create_npc(client, campaign_id)
    faction_id = _create_faction(client, campaign_id)

    client.post(
        f"/api/campaigns/{campaign_id}/links",
        json={"kindA": "npc", "idA": npc_id, "kindB": "faction", "idB": faction_id},
    )

    npc_links = client.get(
        f"/api/campaigns/{campaign_id}/links",
        params={"entity_kind": "npc", "entity_id": npc_id},
    )
    assert npc_links.status_code == 200
    assert len(npc_links.json()) == 1

    faction_links = client.get(
        f"/api/campaigns/{campaign_id}/links",
        params={"entity_kind": "faction", "entity_id": faction_id},
    )
    assert faction_links.status_code == 200
    assert faction_links.json()[0]["id"] == npc_links.json()[0]["id"]


def test_duplicate_link_rejected_regardless_of_direction(client):
    campaign_id = _create_campaign(client)
    npc_id = _create_npc(client, campaign_id)
    faction_id = _create_faction(client, campaign_id)

    first = client.post(
        f"/api/campaigns/{campaign_id}/links",
        json={"kindA": "npc", "idA": npc_id, "kindB": "faction", "idB": faction_id},
    )
    assert first.status_code == 201

    reversed_dup = client.post(
        f"/api/campaigns/{campaign_id}/links",
        json={"kindA": "faction", "idA": faction_id, "kindB": "npc", "idB": npc_id},
    )
    assert reversed_dup.status_code == 409


def test_link_requires_existing_entities(client):
    campaign_id = _create_campaign(client)
    npc_id = _create_npc(client, campaign_id)

    resp = client.post(
        f"/api/campaigns/{campaign_id}/links",
        json={"kindA": "npc", "idA": npc_id, "kindB": "faction", "idB": "does-not-exist"},
    )
    assert resp.status_code == 404


def test_cascade_delete_removes_links(client):
    campaign_id = _create_campaign(client)
    npc_id = _create_npc(client, campaign_id)
    faction_id = _create_faction(client, campaign_id)

    client.post(
        f"/api/campaigns/{campaign_id}/links",
        json={"kindA": "npc", "idA": npc_id, "kindB": "faction", "idB": faction_id},
    )

    delete_resp = client.delete(f"/api/campaigns/{campaign_id}/npcs/{npc_id}")
    assert delete_resp.status_code == 204

    faction_links = client.get(
        f"/api/campaigns/{campaign_id}/links",
        params={"entity_kind": "faction", "entity_id": faction_id},
    )
    assert faction_links.json() == []
