import { describe, expect, it } from "vitest";
import { fromEntries, toEntries } from "./customFields";

describe("toEntries", () => {
  it("returns an empty array for undefined custom fields", () => {
    expect(toEntries(undefined)).toEqual([]);
  });

  it("keeps string values as-is", () => {
    expect(toEntries({ faction: "Harpers" })).toEqual([{ key: "faction", value: "Harpers" }]);
  });

  it("stringifies non-string values", () => {
    expect(toEntries({ level: 5, active: true })).toEqual([
      { key: "level", value: "5" },
      { key: "active", value: "true" },
    ]);
  });
});

describe("fromEntries", () => {
  it("builds a record from entries", () => {
    expect(fromEntries([{ key: "faction", value: "Harpers" }])).toEqual({
      faction: "Harpers",
    });
  });

  it("drops entries with an empty key", () => {
    expect(fromEntries([{ key: "  ", value: "x" }])).toEqual({});
  });

  it("trims keys before using them", () => {
    expect(fromEntries([{ key: " faction ", value: "Harpers" }])).toEqual({
      faction: "Harpers",
    });
  });
});
