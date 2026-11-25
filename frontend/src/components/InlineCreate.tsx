import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface InlineCreateProps {
  placeholder: string;
  onCreate: (name: string) => void;
  isPending?: boolean;
}

export function InlineCreate({ placeholder, onCreate, isPending }: InlineCreateProps) {
  const [name, setName] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) return;
    onCreate(trimmed);
    setName("");
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <Input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder={placeholder}
        aria-label={placeholder}
      />
      <Button type="submit" disabled={isPending || !name.trim()}>
        Add
      </Button>
    </form>
  );
}
