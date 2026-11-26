export interface CustomFieldEntry {
  key: string;
  value: string;
}

export function toEntries(customFields: Record<string, unknown> | undefined): CustomFieldEntry[] {
  if (!customFields) return [];
  return Object.entries(customFields).map(([key, value]) => ({
    key,
    value: typeof value === "string" ? value : JSON.stringify(value),
  }));
}

// Values are always written back as strings; the backend already treats this as a
// migrate-on-open pattern for older non-string custom_fields values.
export function fromEntries(entries: CustomFieldEntry[]): Record<string, string> {
  const result: Record<string, string> = {};
  for (const { key, value } of entries) {
    const trimmedKey = key.trim();
    if (!trimmedKey) continue;
    result[trimmedKey] = value;
  }
  return result;
}
