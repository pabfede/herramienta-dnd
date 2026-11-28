import type { components } from "./schema";

export type CampaignRead = components["schemas"]["CampaignRead"];
export type CampaignCreate = components["schemas"]["CampaignCreate"];
export type NpcRead = components["schemas"]["NpcRead"];
export type NpcCreate = components["schemas"]["NpcCreate"];
export type NpcUpdate = components["schemas"]["NpcUpdate"];
export type LocationRead = components["schemas"]["LocationRead"];
export type LocationCreate = components["schemas"]["LocationCreate"];
export type LocationUpdate = components["schemas"]["LocationUpdate"];
export type FactionRead = components["schemas"]["FactionRead"];
export type FactionCreate = components["schemas"]["FactionCreate"];
export type FactionUpdate = components["schemas"]["FactionUpdate"];
export type EncounterRead = components["schemas"]["EncounterRead"];
export type EncounterUpdate = components["schemas"]["EncounterUpdate"];
export type EncounterGenerate = components["schemas"]["EncounterGenerate"];
export type Combatant = components["schemas"]["Combatant"];
export type SessionRead = components["schemas"]["SessionRead"];
export type SessionCreate = components["schemas"]["SessionCreate"];
export type SessionUpdate = components["schemas"]["SessionUpdate"];
export type LinkRead = components["schemas"]["LinkRead"];
export type LinkCreate = components["schemas"]["LinkCreate"];

export type EntityKind = "npcs" | "locations" | "factions";
export type EntityRead = NpcRead | LocationRead | FactionRead;
export type EntityCreate = NpcCreate | LocationCreate | FactionCreate;
export type EntityUpdate = NpcUpdate | LocationUpdate | FactionUpdate;

// Links store kind as the singular entity name; this maps the plural URL kind to it.
export type LinkKind = "npc" | "location" | "faction";

const LINK_KIND_BY_ENTITY_KIND: Record<EntityKind, LinkKind> = {
  npcs: "npc",
  locations: "location",
  factions: "faction",
};

export function toLinkKind(kind: EntityKind): LinkKind {
  return LINK_KIND_BY_ENTITY_KIND[kind];
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function extractErrorMessage(res: Response): Promise<string> {
  try {
    const body = await res.json();
    if (typeof body?.detail === "string") return body.detail;
    if (Array.isArray(body?.detail)) {
      return body.detail.map((d: { msg?: string }) => d.msg).join(", ");
    }
    return res.statusText;
  } catch {
    return res.statusText;
  }
}

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!res.ok) {
    throw new ApiError(res.status, await extractErrorMessage(res));
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return (await res.json()) as T;
}

export function entityPath(campaignId: string, kind: EntityKind, entityId?: string): string {
  const base = `/api/campaigns/${campaignId}/${kind}`;
  return entityId ? `${base}/${entityId}` : base;
}

export async function exportCampaign(campaignId: string): Promise<void> {
  const res = await fetch(`${BASE_URL}/api/campaigns/${campaignId}/export`);
  if (!res.ok) {
    throw new ApiError(res.status, await extractErrorMessage(res));
  }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${campaignId}.db`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export async function importCampaign(file: File): Promise<CampaignRead> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${BASE_URL}/api/campaigns/import`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new ApiError(res.status, await extractErrorMessage(res));
  }

  return (await res.json()) as CampaignRead;
}
