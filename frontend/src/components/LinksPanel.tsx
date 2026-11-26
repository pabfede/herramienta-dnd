import { useState } from "react";
import type { EntityKind, LinkKind } from "@/api/client";
import { toLinkKind } from "@/api/client";
import { useEntities } from "@/hooks/useEntities";
import { useLinks } from "@/hooks/useLinks";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface LinksPanelProps {
  campaignId: string;
  kind: EntityKind;
  entityId: string;
}

interface Candidate {
  kind: LinkKind;
  id: string;
  name: string;
}

export function LinksPanel({ campaignId, kind, entityId }: LinksPanelProps) {
  const linkKind = toLinkKind(kind);
  const { list, create, remove } = useLinks(campaignId, linkKind, entityId);

  const npcs = useEntities(campaignId, "npcs").list;
  const locations = useEntities(campaignId, "locations").list;
  const factions = useEntities(campaignId, "factions").list;

  const candidates: Candidate[] = [
    ...(npcs.data ?? []).map((e) => ({ kind: "npc" as const, id: e.id, name: e.name })),
    ...(locations.data ?? []).map((e) => ({ kind: "location" as const, id: e.id, name: e.name })),
    ...(factions.data ?? []).map((e) => ({ kind: "faction" as const, id: e.id, name: e.name })),
  ].filter((candidate) => !(candidate.kind === linkKind && candidate.id === entityId));

  function nameFor(otherKind: string, otherId: string): string {
    return (
      candidates.find((c) => c.kind === otherKind && c.id === otherId)?.name ??
      `${otherKind}:${otherId}`
    );
  }

  const [targetKey, setTargetKey] = useState("");
  const [relation, setRelation] = useState("");

  function handleLink(e: React.FormEvent) {
    e.preventDefault();
    const target = candidates.find((c) => `${c.kind}:${c.id}` === targetKey);
    if (!target) return;
    create.mutate(
      { kindA: linkKind, idA: entityId, kindB: target.kind, idB: target.id, relation: relation.trim() || null },
      { onSuccess: () => setRelation("") },
    );
  }

  return (
    <div className="space-y-2 border-t pt-3">
      <p className="text-sm font-medium">Links</p>

      {list.isLoading && <p className="text-sm text-muted-foreground">Loading links...</p>}
      {list.isError && <p className="text-sm text-destructive">Failed to load links.</p>}

      <div className="space-y-1">
        {list.data?.map((link) => {
          const isSelfSideA = link.kindA === linkKind && link.idA === entityId;
          const otherKind = isSelfSideA ? link.kindB : link.kindA;
          const otherId = isSelfSideA ? link.idB : link.idA;
          return (
            <div key={link.id} className="flex items-center justify-between gap-2 text-sm">
              <span>
                {nameFor(otherKind, otherId)}
                {link.relation ? ` (${link.relation})` : ""}
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => remove.mutate(link.id)}
                disabled={remove.isPending}
              >
                Unlink
              </Button>
            </div>
          );
        })}
        {list.data?.length === 0 && (
          <p className="text-sm text-muted-foreground">No links yet.</p>
        )}
      </div>

      <form onSubmit={handleLink} className="flex gap-2">
        <select
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
          value={targetKey}
          onChange={(e) => setTargetKey(e.target.value)}
          aria-label="Link target"
        >
          <option value="">Link to...</option>
          {candidates.map((candidate) => (
            <option key={`${candidate.kind}:${candidate.id}`} value={`${candidate.kind}:${candidate.id}`}>
              {candidate.name}
            </option>
          ))}
        </select>
        <Input
          value={relation}
          onChange={(e) => setRelation(e.target.value)}
          placeholder="Relation (optional)"
          aria-label="Relation"
        />
        <Button type="submit" disabled={!targetKey || create.isPending}>
          Link
        </Button>
      </form>
      {create.isError && (
        <p className="text-sm text-destructive">Failed to link: {create.error.message}</p>
      )}
    </div>
  );
}
