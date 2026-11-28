import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { request, exportCampaign } from "@/api/client";
import type { CampaignRead } from "@/api/client";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { EntityList } from "@/components/EntityList";
import { EncounterPanel } from "@/components/EncounterPanel";
import { SessionPanel } from "@/components/SessionPanel";

interface CampaignDashboardProps {
  campaignId: string;
  onChangeCampaign: () => void;
}

export function CampaignDashboard({ campaignId, onChangeCampaign }: CampaignDashboardProps) {
  const [isExporting, setIsExporting] = useState(false);
  const [exportError, setExportError] = useState<string | null>(null);

  const campaign = useQuery({
    queryKey: ["campaigns", campaignId],
    queryFn: () => request<CampaignRead>(`/api/campaigns/${campaignId}`),
  });

  const handleExport = async () => {
    setIsExporting(true);
    setExportError(null);
    try {
      await exportCampaign(campaignId);
    } catch (err) {
      setExportError(err instanceof Error ? err.message : "Export failed");
    } finally {
      setIsExporting(false);
    }
  };

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
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={handleExport}
            disabled={isExporting}
          >
            {isExporting ? "Exporting..." : "Export"}
          </Button>
          <Button variant="outline" onClick={onChangeCampaign}>
            Change campaign
          </Button>
        </div>
      </div>

      {exportError && (
        <p className="text-destructive">Export failed: {exportError}</p>
      )}

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
          <TabsTrigger value="sessions">Sessions</TabsTrigger>
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

        <TabsContent value="sessions">
          <SessionPanel campaignId={campaignId} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
