import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { LinkCreate, LinkKind, LinkRead } from "@/api/client";
import { request } from "@/api/client";

function linksPath(campaignId: string, linkId?: string): string {
  const base = `/api/campaigns/${campaignId}/links`;
  return linkId ? `${base}/${linkId}` : base;
}

export function useLinks(campaignId: string, entityKind: LinkKind, entityId: string) {
  const queryClient = useQueryClient();
  const queryKey = ["campaigns", campaignId, "links", entityKind, entityId];

  const list = useQuery({
    queryKey,
    queryFn: () =>
      request<LinkRead[]>(
        `${linksPath(campaignId)}?entity_kind=${encodeURIComponent(entityKind)}&entity_id=${encodeURIComponent(entityId)}`,
      ),
    enabled: Boolean(entityId),
  });

  const create = useMutation({
    mutationFn: (body: LinkCreate) =>
      request<LinkRead>(linksPath(campaignId), {
        method: "POST",
        body: JSON.stringify(body),
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  const remove = useMutation({
    mutationFn: (linkId: string) =>
      request<void>(linksPath(campaignId, linkId), { method: "DELETE" }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  return { list, create, remove };
}
