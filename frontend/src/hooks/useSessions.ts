import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { SessionCreate, SessionRead, SessionUpdate } from "@/api/client";
import { request } from "@/api/client";

function sessionPath(campaignId: string, sessionId?: string): string {
  const base = `/api/campaigns/${campaignId}/sessions`;
  return sessionId ? `${base}/${sessionId}` : base;
}

export function useSessions(campaignId: string) {
  const queryClient = useQueryClient();
  const queryKey = ["campaigns", campaignId, "sessions"];

  const list = useQuery({
    queryKey,
    queryFn: () => request<SessionRead[]>(sessionPath(campaignId)),
  });

  const create = useMutation({
    mutationFn: (body: SessionCreate) =>
      request<SessionRead>(sessionPath(campaignId), {
        method: "POST",
        body: JSON.stringify(body),
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  const update = useMutation({
    mutationFn: ({ id, ...body }: SessionUpdate & { id: string }) =>
      request<SessionRead>(sessionPath(campaignId, id), {
        method: "PATCH",
        body: JSON.stringify(body),
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  const remove = useMutation({
    mutationFn: (sessionId: string) =>
      request<void>(sessionPath(campaignId, sessionId), { method: "DELETE" }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  return { list, create, update, remove };
}
