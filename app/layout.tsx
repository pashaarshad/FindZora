import type { Metadata } from "next";
import Navbar from "@/components/Navbar";
import "./globals.css";

export const metadata: Metadata = {
  title: "FindZora - AI-Powered Event Photo Discovery",
  description: "Consent-based, event-scoped photo discovery system powered by ArcFace biometric embeddings and FAISS index.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-slate-50 text-slate-900 antialiased">
        <Navbar />
        <main className="flex-1 pb-16">{children}</main>
        <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
          <p>© 2026 FindZora • Master of Computer Applications (MCA) Project • Prepared by Mohammad Arsh</p>
          <p className="mt-1 text-slate-400">Strictly privacy-preserving • Ephemeral query processing • Event-isolated indexing</p>
        </footer>
      </body>
    </html>
  );
}
