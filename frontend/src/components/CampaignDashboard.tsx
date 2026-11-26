import { useQuery } from "@tanstack/react-query";
import { request } from "@/api/client";
import type { CampaignRead } from "@/api/client";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { EntityList } from "@/components/EntityList";
import { EncounterPanel } from "@/components/EncounterPanel";

interface CampaignDashboardProps {
  campaignId: string;
  onChangeCampaign: () => void;
}

export function CampaignDashboard({ campaignId, onChangeCampaign }: CampaignDashboardProps) {
  const campaign = useQuery({
    queryKey: ["campaigns", campaignId],
    queryFn: () => request<CampaignRead>(`/api/campaigns/${campaignId}`),
  });

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-4">
      <div className="flex items-center justify-between gap-2">
        <h1 className="text-2xl font-bold">
          {campaign.isError
            ? "Failed to load campaign."
            : campaign.data
              ? campaign.data.name
              : "Loading..."}
        </h1>
        <Button variant="outline" onClick={onChangeCampaign}>
          Change campaign
        </Button>
      </div>

      {campaign.isError && (
        <div className="flex items-center gap-2">
          <p className="text-destructive">{campaign.error.message}</p>
          <Button variant="outline" size="sm" onClick={() => campaign.refetch()}>
            Retry
          </Button>
        </div>
      )}

      <Tabs defaultValue="overview">
        <TabsList className="flex-wrap">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="npcs">NPCs</TabsTrigger>
          <TabsTrigger value="locations">Locations</TabsTrigger>
          <TabsTrigger value="factions">Factions</TabsTrigger>
          <TabsTrigger value="encounters">Encounters</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <p className="text-muted-foreground">
            {campaign.data?.description ?? "No description yet."}
          </p>
        </TabsContent>

        <TabsContent value="npcs">
          <EntityList campaignId={campaignId} kind="npcs" label="NPCs" />
        </TabsContent>

        <TabsContent value="locations">
          <EntityList campaignId={campaignId} kind="locations" label="Locations" />
        </TabsContent>

        <TabsContent value="factions">
          <EntityList campaignId={campaignId} kind="factions" label="Factions" />
        </TabsContent>

        <TabsContent value="encounters">
          <EncounterPanel campaignId={campaignId} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
