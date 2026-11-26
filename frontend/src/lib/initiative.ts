import type { Combatant } from "@/api/client";

export function sortByInitiative(combatants: Combatant[]): Combatant[] {
  return [...combatants]
    .map((combatant, index) => ({ combatant, index }))
    .sort((a, b) => {
      const ai = a.combatant.initiative;
      const bi = b.combatant.initiative;
      if (ai === bi) return a.combatant.name.localeCompare(b.combatant.name) || a.index - b.index;
      if (ai == null) return 1;
      if (bi == null) return -1;
      return bi - ai;
    })
    .map(({ combatant }) => combatant);
}
