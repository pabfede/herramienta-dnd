import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { EncounterGenerate, EncounterRead, EncounterUpdate } from "@/api/client";
import { request } from "@/api/client";

function encounterPath(campaignId: string, encounterId?: string): string {
  const base = `/api/campaigns/${campaignId}/encounters`;
  return encounterId ? `${base}/${encounterId}` : base;
}

export function useEncounters(campaignId: string) {
  const queryClient = useQueryClient();
  const queryKey = ["campaigns", campaignId, "encounters"];

  const list = useQuery({
    queryKey,
    queryFn: () => request<EncounterRead[]>(encounterPath(campaignId)),
  });

  const generate = useMutation({
    mutationFn: (body: EncounterGenerate) =>
      request<EncounterRead>(`${encounterPath(campaignId)}/generate`, {
        method: "POST",
        body: JSON.stringify(body),
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  const update = useMutation({
    mutationFn: ({ id, ...body }: EncounterUpdate & { id: string }) =>
      request<EncounterRead>(encounterPath(campaignId, id), {
        method: "PATCH",
        body: JSON.stringify(body),
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  const remove = useMutation({
    mutationFn: (encounterId: string) =>
      request<void>(encounterPath(campaignId, encounterId), { method: "DELETE" }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  return { list, generate, update, remove };
}
