import type { components } from "./schema";

export type CampaignRead = components["schemas"]["CampaignRead"];
export type CampaignCreate = components["schemas"]["CampaignCreate"];
export type NpcRead = components["schemas"]["NpcRead"];
export type NpcCreate = components["schemas"]["NpcCreate"];
export type LocationRead = components["schemas"]["LocationRead"];
export type LocationCreate = components["schemas"]["LocationCreate"];
export type FactionRead = components["schemas"]["FactionRead"];
export type FactionCreate = components["schemas"]["FactionCreate"];

export type EntityKind = "npcs" | "locations" | "factions";
export type EntityRead = NpcRead | LocationRead | FactionRead;
export type EntityCreate = NpcCreate | LocationCreate | FactionCreate;

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
