"use client";

import { useFormStatus } from "react-dom";

export function SubmitButton({ idleLabel, loadingLabel }: { idleLabel: string; loadingLabel: string }) {
  const { pending } = useFormStatus();

  return (
    <button
      type="submit"
      disabled={pending}
      className="mt-4 rounded-md bg-accent px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-60"
    >
      {pending ? loadingLabel : idleLabel}
    </button>
  );
}
