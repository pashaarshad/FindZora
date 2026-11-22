"use client";

import Link from "next/link";
import { Camera, ShieldCheck, LayoutDashboard, FileText } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="bg-gradient-to-tr from-sky-600 to-indigo-600 text-white p-2 rounded-xl shadow-md">
            <Camera className="w-5 h-5" />
          </div>
          <div>
            <span className="font-bold text-xl tracking-tight text-slate-900">Find<span className="text-sky-600">Zora</span></span>
            <span className="ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-sky-50 text-sky-700 border border-sky-200">
              AI Biometric Search
            </span>
          </div>
        </Link>

        <nav className="flex items-center gap-4">
          <Link
            href="/"
            className="text-sm font-medium text-slate-600 hover:text-sky-600 transition flex items-center gap-1.5"
          >
            <Camera className="w-4 h-4" />
            Universal Search
          </Link>
          <Link
            href="/organizer"
            className="text-sm font-medium text-slate-600 hover:text-sky-600 transition flex items-center gap-1.5"
          >
            <LayoutDashboard className="w-4 h-4" />
            Organizer & CLI
          </Link>
          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-medium text-slate-500 hover:text-slate-800 transition flex items-center gap-1.5"
          >
            <FileText className="w-4 h-4" />
            API Docs
          </a>
        </nav>
      </div>
    </header>
  );
}
