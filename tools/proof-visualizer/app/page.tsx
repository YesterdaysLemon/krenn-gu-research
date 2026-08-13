import frontierData from "./data/frontier.generated.json";
import type { FrontierData } from "./frontier-types";
import { ProofBonsai } from "./ProofBonsai";

export default function Home() {
  return <ProofBonsai data={frontierData as FrontierData} />;
}
