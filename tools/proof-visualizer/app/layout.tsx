import type { Metadata } from "next";
import "./globals.css";

const title = "Proof Bonsai · Krenn–Gu research map";
const description =
  "An interactive, repository-derived view of the Krenn–Gu proof-obligation topology.";

export const metadata: Metadata = {
  metadataBase: new URL("https://proof-bonsai.alirezaafshan.com"),
  title,
  description,
  openGraph: {
    title,
    description,
    type: "website",
    images: [{ url: "/og.png", width: 1536, height: 1024, alt: "Proof Bonsai research map" }],
  },
  twitter: {
    card: "summary_large_image",
    title,
    description,
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
