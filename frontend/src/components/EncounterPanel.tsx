import { useState } from "react";
import { useEncounters } from "@/hooks/useEncounters";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { CombatTracker } from "@/components/CombatTracker";

interface EncounterPanelProps {
  campaignId: string;
}

export function EncounterPanel({ campaignId }: EncounterPanelProps) {
  const { list, generate, update, remove } = useEncounters(campaignId);
  const [size, setSize] = useState("3");
  const [faction, setFaction] = useState("");

  function handleGenerate(e: React.FormEvent) {
    e.preventDefault();
    const parsedSize = Number.parseInt(size, 10);
    if (!Number.isFinite(parsedSize) || parsedSize <= 0) return;
    generate.mutate({ size: parsedSize, faction: faction.trim() || null });
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleGenerate} className="flex gap-2">
        <Input
          type="number"
          min={1}
          value={size}
          onChange={(e) => setSize(e.target.value)}
          placeholder="Size"
          aria-label="Encounter size"
          className="w-24"
        />
        <Input
          value={faction}
          onChange={(e) => setFaction(e.target.value)}
          placeholder="Faction (optional)"
          aria-label="Faction filter"
        />
        <Button type="submit" disabled={generate.isPending}>
          Generate
        </Button>
      </form>

      {generate.isError && (
        <p className="text-destructive">Failed to generate: {generate.error.message}</p>
      )}

      {list.isLoading && <p className="text-muted-foreground">Loading encounters...</p>}
      {list.isError && <p className="text-destructive">Failed to load encounters.</p>}
      {remove.isError && <p className="text-destructive">Failed to delete: {remove.error.message}</p>}

      <div className="space-y-4">
        {list.data?.map((encounter) => (
          <Card key={encounter.id}>
            <CardContent className="space-y-4 p-4">
              <div className="flex items-center justify-between gap-2">
                <span className="font-medium">{encounter.name}</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => remove.mutate(encounter.id)}
                  disabled={remove.isPending}
                >
                  Delete
                </Button>
              </div>
              <CombatTracker
                encounter={encounter}
                onSave={(changes) => update.mutate({ id: encounter.id, ...changes })}
              />
            </CardContent>
          </Card>
        ))}
      </div>

      {list.data?.length === 0 && (
        <p className="text-muted-foreground">No encounters yet. Generate one above.</p>
      )}
    </div>
  );
}
