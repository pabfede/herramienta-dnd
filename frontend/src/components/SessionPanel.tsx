import { useState } from "react";
import type { SessionRead } from "@/api/client";
import { useSessions } from "@/hooks/useSessions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";

interface SessionPanelProps {
  campaignId: string;
}

export function SessionPanel({ campaignId }: SessionPanelProps) {
  const { list, create, update, remove } = useSessions(campaignId);
  const [name, setName] = useState("");

  function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) return;
    create.mutate({ name: trimmed });
    setName("");
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleCreate} className="flex gap-2">
        <Input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="New session name"
          aria-label="New session name"
        />
        <Button type="submit" disabled={create.isPending || !name.trim()}>
          Add
        </Button>
      </form>

      {create.isError && (
        <p className="text-destructive">Failed to create: {create.error.message}</p>
      )}
      {list.isLoading && <p className="text-muted-foreground">Loading sessions...</p>}
      {list.isError && <p className="text-destructive">Failed to load sessions.</p>}
      {remove.isError && <p className="text-destructive">Failed to delete: {remove.error.message}</p>}

      <div className="space-y-4">
        {list.data?.map((session) => (
          <SessionCard
            key={session.id}
            session={session}
            onSaveNotes={(notes) => update.mutate({ id: session.id, notes })}
            onDelete={() => remove.mutate(session.id)}
            deletePending={remove.isPending}
          />
        ))}
      </div>

      {list.data?.length === 0 && (
        <p className="text-muted-foreground">No sessions logged yet. Add one above.</p>
      )}
    </div>
  );
}

interface SessionCardProps {
  session: SessionRead;
  onSaveNotes: (notes: string) => void;
  onDelete: () => void;
  deletePending: boolean;
}

function SessionCard({ session, onSaveNotes, onDelete, deletePending }: SessionCardProps) {
  const [notes, setNotes] = useState(session.notes ?? "");

  return (
    <Card>
      <CardContent className="space-y-2 p-4">
        <div className="flex items-center justify-between gap-2">
          <span className="font-medium">{session.name}</span>
          <Button variant="ghost" size="sm" onClick={onDelete} disabled={deletePending}>
            Delete
          </Button>
        </div>
        <Textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Session notes"
          aria-label={`Notes for ${session.name}`}
        />
        <Button variant="outline" size="sm" onClick={() => onSaveNotes(notes)}>
          Save notes
        </Button>
      </CardContent>
    </Card>
  );
}
