import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, entityPath, request } from "./client";

describe("entityPath", () => {
  it("builds the list path for npcs", () => {
    expect(entityPath("c1", "npcs")).toBe("/api/campaigns/c1/npcs");
  });

  it("builds the list path for locations", () => {
    expect(entityPath("c1", "locations")).toBe("/api/campaigns/c1/locations");
  });

  it("builds the list path for factions", () => {
    expect(entityPath("c1", "factions")).toBe("/api/campaigns/c1/factions");
  });

  it("builds the item path when an entity id is given", () => {
    expect(entityPath("c1", "npcs", "n1")).toBe("/api/campaigns/c1/npcs/n1");
  });
});

describe("request", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("returns undefined for a 204 response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response(null, { status: 204 })),
    );
    const result = await request("/api/campaigns/c1/npcs/n1", { method: "DELETE" });
    expect(result).toBeUndefined();
  });

  it("parses JSON for a successful response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ id: "n1" }), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );
    const result = await request<{ id: string }>("/api/campaigns/c1/npcs/n1");
    expect(result).toEqual({ id: "n1" });
  });

  it("extracts a string detail from an error response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: "Campaign c1 not found" }), {
          status: 404,
        }),
      ),
    );
    await expect(request("/api/campaigns/c1")).rejects.toThrow(
      "Campaign c1 not found",
    );
  });

  it("extracts a validation error detail array into a message", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({ detail: [{ msg: "field required" }] }),
          { status: 422 },
        ),
      ),
    );
    await expect(request("/api/campaigns")).rejects.toThrow("field required");
  });

  it("throws an ApiError with the response status", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response(null, { status: 500, statusText: "Server Error" })),
    );
    await expect(request("/api/campaigns")).rejects.toMatchObject({
      status: 500,
    });
  });
});

describe("ApiError", () => {
  it("carries the status code", () => {
    const err = new ApiError(404, "not found");
    expect(err.status).toBe(404);
    expect(err.message).toBe("not found");
  });
});
