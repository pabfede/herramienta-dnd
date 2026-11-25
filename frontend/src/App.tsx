import { useState } from "react";
import { CampaignPicker } from "@/components/CampaignPicker";
import { CampaignDashboard } from "@/components/CampaignDashboard";

export default function App() {
  const [campaignId, setCampaignId] = useState<string | null>(null);

  if (!campaignId) {
    return <CampaignPicker onSelect={setCampaignId} />;
  }

  return (
    <CampaignDashboard
      campaignId={campaignId}
      onChangeCampaign={() => setCampaignId(null)}
    />
  );
}
