import { useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { useCampaigns } from "@/hooks/useCampaigns";
import { importCampaign } from "@/api/client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { InlineCreate } from "@/components/InlineCreate";

interface CampaignPickerProps {
  onSelect: (campaignId: string) => void;
}

export function CampaignPicker({ onSelect }: CampaignPickerProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const queryClient = useQueryClient();
  const { list, create, remove } = useCampaigns();
  const [isImporting, setIsImporting] = useState(false);
  const [importError, setImportError] = useState<string | null>(null);

  const handleImportClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileSelected = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.currentTarget.files?.[0];
    if (!file) return;

    setIsImporting(true);
    setImportError(null);
    try {
      await importCampaign(file);
      // Refetch campaigns list after import
      await queryClient.invalidateQueries({ queryKey: ["campaigns"] });
    } catch (err) {
      setImportError(err instanceof Error ? err.message : "Import failed");
    } finally {
      setIsImporting(false);
      e.currentTarget.value = "";
    }
  };

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-4">
      <div className="flex items-center justify-between gap-2">
        <h1 className="text-2xl font-bold">Campaigns</h1>
        <Button
          variant="outline"
          onClick={handleImportClick}
          disabled={isImporting}
        >
          {isImporting ? "Importing..." : "Import"}
        </Button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".db"
          onChange={handleFileSelected}
          style={{ display: "none" }}
        />
      </div>

      <InlineCreate
        placeholder="New campaign name"
        onCreate={(name) => create.mutate({ name })}
        isPending={create.isPending}
      />

      {list.isLoading && <p className="text-muted-foreground">Loading campaigns...</p>}
      {list.isError && <p className="text-destructive">Failed to load campaigns.</p>}
      {remove.isError && <p className="text-destructive">Failed to delete: {remove.error.message}</p>}
      {importError && <p className="text-destructive">Import failed: {importError}</p>}

      <div className="grid gap-3 sm:grid-cols-2">
        {list.data?.map((campaign) => (
          <Card key={campaign.id}>
            <CardHeader>
              <CardTitle className="text-lg">{campaign.name}</CardTitle>
            </CardHeader>
            <CardContent className="flex items-center justify-between gap-2">
              <Button onClick={() => onSelect(campaign.id)}>Open</Button>
              <Button
                variant="ghost"
                onClick={() => remove.mutate(campaign.id)}
                disabled={remove.isPending}
              >
                Delete
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {list.data?.length === 0 && (
        <p className="text-muted-foreground">No campaigns yet. Create one above.</p>
      )}
    </div>
  );
}
