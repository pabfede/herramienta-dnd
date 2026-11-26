import { useEffect, useState } from "react";
import type { Combatant, EncounterRead, EncounterUpdate } from "@/api/client";
import { sortByInitiative } from "@/lib/initiative";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

interface CombatTrackerProps {
  encounter: EncounterRead;
  onSave: (changes: EncounterUpdate) => void;
}

export function CombatTracker({ encounter, onSave }: CombatTrackerProps) {
  const [combatants, setCombatants] = useState<Combatant[]>(encounter.combatants ?? []);
  const [notes, setNotes] = useState(encounter.notes ?? "");

  useEffect(() => {
    setCombatants(encounter.combatants ?? []);
    setNotes(encounter.notes ?? "");
  }, [encounter.id]);

  const sorted = sortByInitiative(combatants);

  function handleInitiativeChange(name: string, sourceId: string | null | undefined, value: string) {
    const parsed = value.trim() === "" ? null : Number.parseInt(value, 10);
    setCombatants((prev) =>
      prev.map((c) =>
        c.name === name && c.sourceId === sourceId
          ? { ...c, initiative: Number.isFinite(parsed) ? parsed : null }
          : c
      )
    );
  }

  function saveCombatants() {
    onSave({ combatants });
  }

  function saveNotes() {
    onSave({ notes });
  }

  return (
    <div className="space-y-3">
      <div className="space-y-1">
        {sorted.map((combatant, index) => (
          <div
            key={`${combatant.name}-${combatant.sourceId ?? "none"}`}
            className="flex items-center justify-between gap-2 rounded-md border p-2"
          >
            <div className="flex items-center gap-2">
              {index === 0 && (
                <span className="rounded bg-primary px-2 py-0.5 text-xs font-medium text-primary-foreground">
                  Current turn
                </span>
              )}
              <span>{combatant.name}</span>
            </div>
            <Input
              type="number"
              className="w-20"
              aria-label={`Initiative for ${combatant.name}`}
              value={combatant.initiative ?? ""}
              onChange={(e) =>
                handleInitiativeChange(combatant.name, combatant.sourceId, e.target.value)
              }
              onBlur={saveCombatants}
            />
          </div>
        ))}
        {sorted.length === 0 && (
          <p className="text-muted-foreground">No combatants in this encounter.</p>
        )}
      </div>

      <Textarea
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        onBlur={saveNotes}
        placeholder="Combat log / session notes"
        aria-label="Encounter notes"
      />
    </div>
  );
}
