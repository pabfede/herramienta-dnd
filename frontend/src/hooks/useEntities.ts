import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { EntityCreate, EntityKind, EntityRead } from "@/api/client";
import { entityPath, request } from "@/api/client";

export function useEntities(campaignId: string, kind: EntityKind) {
  const queryClient = useQueryClient();
  const queryKey = ["campaigns", campaignId, kind];

  const list = useQuery({
    queryKey,
    queryFn: () => request<EntityRead[]>(entityPath(campaignId, kind)),
  });

  const create = useMutation({
    mutationFn: (body: EntityCreate) =>
      request<EntityRead>(entityPath(campaignId, kind), {
        method: "POST",
        body: JSON.stringify(body),
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  const remove = useMutation({
    mutationFn: (entityId: string) =>
      request<void>(entityPath(campaignId, kind, entityId), { method: "DELETE" }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  return { list, create, remove };
}
