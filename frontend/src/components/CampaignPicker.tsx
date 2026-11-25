import { useCampaigns } from "@/hooks/useCampaigns";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { InlineCreate } from "@/components/InlineCreate";

interface CampaignPickerProps {
  onSelect: (campaignId: string) => void;
}

export function CampaignPicker({ onSelect }: CampaignPickerProps) {
  const { list, create, remove } = useCampaigns();

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-4">
      <h1 className="text-2xl font-bold">Campaigns</h1>

      <InlineCreate
        placeholder="New campaign name"
        onCreate={(name) => create.mutate({ name })}
        isPending={create.isPending}
      />

      {list.isLoading && <p className="text-muted-foreground">Loading campaigns...</p>}
      {list.isError && <p className="text-destructive">Failed to load campaigns.</p>}

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
