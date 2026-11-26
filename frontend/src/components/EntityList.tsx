import type { EntityKind } from "@/api/client";
import { useEntities } from "@/hooks/useEntities";
import { InlineCreate } from "@/components/InlineCreate";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface EntityListProps {
  campaignId: string;
  kind: EntityKind;
  label: string;
}

export function EntityList({ campaignId, kind, label }: EntityListProps) {
  const { list, create, remove } = useEntities(campaignId, kind);

  return (
    <div className="space-y-4">
      <InlineCreate
        placeholder={`New ${label.toLowerCase()} name`}
        onCreate={(name) => create.mutate({ name })}
        isPending={create.isPending}
      />

      {list.isLoading && <p className="text-muted-foreground">Loading {label.toLowerCase()}...</p>}
      {list.isError && <p className="text-destructive">Failed to load {label.toLowerCase()}.</p>}
      {remove.isError && <p className="text-destructive">Failed to delete: {remove.error.message}</p>}

      <div className="space-y-2">
        {list.data?.map((entity) => (
          <Card key={entity.id}>
            <CardContent className="flex items-center justify-between gap-2 p-4">
              <span className="font-medium">{entity.name}</span>
              <div className="flex gap-2">
                {/* shortcut: edit is Phase 4 scope, not wired yet */}
                <Button variant="outline" size="sm" disabled title="Editing arrives in Phase 4">
                  Edit
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => remove.mutate(entity.id)}
                  disabled={remove.isPending}
                >
                  Delete
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {list.data?.length === 0 && (
        <p className="text-muted-foreground">No {label.toLowerCase()} yet. Add one above.</p>
      )}
    </div>
  );
}
