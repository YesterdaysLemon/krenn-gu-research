import type { Metadata } from "next";
import fieldNotesData from "../data/field-notes.generated.json";
import { FieldNotes } from "../FieldNotes";
import type { FieldNotesData } from "../field-notes-types";

export const metadata: Metadata = {
  title: "Field Notes · Proof Bonsai",
  description:
    "Append-only public activity notes from the Krenn–Gu agent ecology, kept separate from mathematical evidence.",
};

export default function FieldNotesPage() {
  return <FieldNotes data={fieldNotesData as FieldNotesData} />;
}
