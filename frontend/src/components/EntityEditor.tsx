import { useState } from "react";
import type { EntityKind, EntityRead } from "@/api/client";
import { useEntities } from "@/hooks/useEntities";
import { fromEntries, toEntries, type CustomFieldEntry } from "@/lib/customFields";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { LinksPanel } from "@/components/LinksPanel";

interface EntityEditorProps {
  campaignId: string;
  kind: EntityKind;
  entity: EntityRead;
  onClose: () => void;
}

export function EntityEditor({ campaignId, kind, entity, onClose }: EntityEditorProps) {
  const { update } = useEntities(campaignId, kind);
  const [name, setName] = useState(entity.name);
  const [description, setDescription] = useState(entity.description ?? "");
  const [fields, setFields] = useState<CustomFieldEntry[]>(toEntries(entity.customFields));

  function updateField(index: number, patch: Partial<CustomFieldEntry>) {
    setFields((prev) => prev.map((field, i) => (i === index ? { ...field, ...patch } : field)));
  }

  function removeField(index: number) {
    setFields((prev) => prev.filter((_, i) => i !== index));
  }

  function addField() {
    setFields((prev) => [...prev, { key: "", value: "" }]);
  }

  function handleSave(e: React.FormEvent) {
    e.preventDefault();
    const trimmedName = name.trim();
    if (!trimmedName) return;
    update.mutate({
      id: entity.id,
      name: trimmedName,
      description: description.trim() || null,
      customFields: fromEntries(fields),
    });
  }

  return (
    <Card>
      <CardContent className="space-y-3 p-4">
        <form onSubmit={handleSave} className="space-y-3">
          <Input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Name"
            aria-label="Name"
          />
          <Textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description"
            aria-label="Description"
          />

          <div className="space-y-2">
            <p className="text-sm font-medium">Custom fields</p>
            {fields.map((field, index) => (
              <div key={index} className="flex gap-2">
                <Input
                  value={field.key}
                  onChange={(e) => updateField(index, { key: e.target.value })}
                  placeholder="Field name"
                  aria-label="Custom field name"
                />
                <Input
                  value={field.value}
                  onChange={(e) => updateField(index, { value: e.target.value })}
                  placeholder="Value"
                  aria-label="Custom field value"
                />
                <Button variant="ghost" size="sm" type="button" onClick={() => removeField(index)}>
                  Remove
                </Button>
              </div>
            ))}
            <Button variant="outline" size="sm" type="button" onClick={addField}>
              Add field
            </Button>
          </div>

          {update.isError && (
            <p className="text-destructive">Failed to save: {update.error.message}</p>
          )}

          <div className="flex gap-2">
            <Button type="submit" disabled={update.isPending || !name.trim()}>
              Save
            </Button>
            <Button type="button" variant="outline" onClick={onClose}>
              Close
            </Button>
          </div>
        </form>

        <LinksPanel campaignId={campaignId} kind={kind} entityId={entity.id} />
      </CardContent>
    </Card>
  );
}
