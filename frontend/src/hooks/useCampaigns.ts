import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { CampaignCreate, CampaignRead } from "@/api/client";
import { request } from "@/api/client";

const CAMPAIGNS_KEY = ["campaigns"];

export function useCampaigns() {
  const queryClient = useQueryClient();

  const list = useQuery({
    queryKey: CAMPAIGNS_KEY,
    queryFn: () => request<CampaignRead[]>("/api/campaigns"),
  });

  const create = useMutation({
    mutationFn: (body: CampaignCreate) =>
      request<CampaignRead>("/api/campaigns", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: CAMPAIGNS_KEY }),
  });

  const remove = useMutation({
    mutationFn: (campaignId: string) =>
      request<void>(`/api/campaigns/${campaignId}`, { method: "DELETE" }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: CAMPAIGNS_KEY }),
  });

  return { list, create, remove };
}
