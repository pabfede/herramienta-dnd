import { describe, expect, it } from "vitest";
import type { Combatant } from "@/api/client";
import { sortByInitiative } from "./initiative";

function combatant(name: string, initiative: number | null): Combatant {
  return { name, initiative, sourceId: null };
}

describe("sortByInitiative", () => {
  it("sorts descending by initiative", () => {
    const result = sortByInitiative([
      combatant("A", 10),
      combatant("B", 20),
      combatant("C", 15),
    ]);
    expect(result.map((c) => c.name)).toEqual(["B", "C", "A"]);
  });

  it("puts null initiative last", () => {
    const result = sortByInitiative([
      combatant("A", null),
      combatant("B", 5),
    ]);
    expect(result.map((c) => c.name)).toEqual(["B", "A"]);
  });

  it("is stable by name when initiatives tie", () => {
    const result = sortByInitiative([
      combatant("Zed", 10),
      combatant("Anna", 10),
    ]);
    expect(result.map((c) => c.name)).toEqual(["Anna", "Zed"]);
  });

  it("keeps multiple null initiatives in original order among themselves", () => {
    const result = sortByInitiative([
      combatant("First", null),
      combatant("Second", null),
      combatant("Leader", 10),
    ]);
    expect(result.map((c) => c.name)).toEqual(["Leader", "First", "Second"]);
  });
});
