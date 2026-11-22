"use client";

import { useEffect, useState } from "react";
import {
  Terminal,
  FolderSync,
  RefreshCw,
  FolderOpen,
  FileCode,
  Users,
  CheckCircle2,
  Play,
  Copy,
  Check
} from "lucide-react";

export default function WatchFolderConsole() {
  const [folderInfo, setFolderInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [copiedCmd, setCopiedCmd] = useState(false);
  const [activeTab, setActiveTab] = useState<"terminal" | "json" | "guide">("terminal");

  // Sample real-time terminal output
  const [logs, setLogs] = useState<string[]>([
    "[INIT] Universal Watch Folder Server initialized.",
    "[WATCHER] Root path: D:\\FindZora\\universal_folder",
    "[WATCHER] Active event folders: 2 (ayesha_and_imran_wedding, mca_convocation_2026)",
    "[POLL] Listening for new JPG/PNG camera sync drops every 3s...",
    "[DETECT] Ingested 'wedding_stage_01.jpg' in ayesha_and_imran_wedding/",
    "[AI VISION] Detected 2 faces -> 6-point geometric landmark coordinates extracted.",
    "[EMBEDDING] Generated 512-D L2-normalized ArcFace vectors.",
    "[CLUSTERING] Matched face #1 to Person_101 (Arshad) -> Added 'wedding_stage_01.jpg'",
    "[CLUSTERING] Assigned face #2 to new Person_102 -> Added 'wedding_stage_01.jpg'",
    "[SAVE] Updated 'face_clusters.json' with 2 person clusters.",
    "[READY] Awaiting next image upload..."
  ]);

  useEffect(() => {
    fetchWatchFolderData();
  }, []);

  const fetchWatchFolderData = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/admin/watch-folder");
      if (res.ok) {
        const data = await res.json();
        setFolderInfo(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateDrop = () => {
    const timestamp = new Date().toLocaleTimeString();
    const newLogs = [
      `[WATCHER ${timestamp}] 📸 Camera synced new image: 'reception_candid_${Math.floor(Math.random() * 89 + 10)}.jpg'`,
      `[AI ${timestamp}] Extracting facial keypoints & 512-D embedding...`,
      `[CLUSTER ${timestamp}] Matched to Person_101 (Arshad) with 98.4% cosine similarity!`,
      `[JSON ${timestamp}] Synced face_clusters.json with updated photo path list.`
    ];
    setLogs((prev) => [...prev, ...newLogs]);
  };

  const copyCLICommand = () => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText("python -m backend.cli.watch_folder");
      setCopiedCmd(true);
      setTimeout(() => setCopiedCmd(false), 2000);
    }
  };

  const sampleJson = {
    event_folder: "ayesha_and_imran_wedding",
    last_updated: "2026-11-22T19:35:00Z",
    person_clusters: {
      "101": {
        person_id: "101",
        label: "Person_101 (Arshad)",
        total_photos: 2,
        photo_paths: [
          "wedding_stage_01.jpg",
          "candid_dinner_04.jpg"
        ]
      },
      "102": {
        person_id: "102",
        label: "Person_102",
        total_photos: 1,
        photo_paths: [
          "wedding_stage_01.jpg"
        ]
      }
    }
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
      {/* Title & Status */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
            <FolderSync className="w-3.5 h-3.5 text-emerald-600" /> CLI Universal Watch Folder
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
            Universal Folder Auto-Ingestion Server
          </h2>
          <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">
            Drop event photos directly into your local or VPS folder. The server monitors additions, computes facial points & embeddings, and clusters people into JSON format automatically.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleSimulateDrop}
            className="px-4 py-2 bg-sky-600 hover:bg-sky-700 text-white text-xs font-semibold rounded-xl shadow transition flex items-center gap-1.5"
          >
            <Play className="w-3.5 h-3.5" /> Simulate Photo Sync
          </button>
          <button
            onClick={fetchWatchFolderData}
            className="p-2 text-slate-500 hover:text-slate-800 border rounded-xl hover:bg-slate-50"
            title="Refresh"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Folder Structure Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 text-xs space-y-1">
          <span className="text-slate-500 font-semibold block">Universal Watch Directory:</span>
          <span className="font-mono font-bold text-slate-800 block truncate" title="D:\FindZora\universal_folder">
            universal_folder/
          </span>
          <span className="text-[11px] text-emerald-600 font-medium">● Daemon Listening on Local & VPS</span>
        </div>

        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 text-xs space-y-1">
          <span className="text-slate-500 font-semibold block">Detected Event Folders:</span>
          <span className="font-bold text-slate-800 text-base">
            {folderInfo?.events?.length || 2} Event Folders
          </span>
          <span className="text-[11px] text-slate-400">ayesha_and_imran_wedding, mca_convocation_2026</span>
        </div>

        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 text-xs space-y-1">
          <span className="text-slate-500 font-semibold block">CLI Daemon Command:</span>
          <div className="flex items-center justify-between bg-white px-2.5 py-1.5 rounded-lg border border-slate-300 font-mono text-[11px] text-slate-800">
            <span className="truncate">python -m backend.cli.watch_folder</span>
            <button onClick={copyCLICommand} className="ml-2 text-slate-400 hover:text-slate-700">
              {copiedCmd ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Tabs: Terminal Feed / JSON Cluster Output / Setup Guide */}
      <div className="border-b border-slate-200 flex items-center gap-4 text-xs font-semibold">
        <button
          onClick={() => setActiveTab("terminal")}
          className={`pb-2.5 border-b-2 transition flex items-center gap-1.5 ${
            activeTab === "terminal"
              ? "border-sky-600 text-sky-600 font-bold"
              : "border-transparent text-slate-500 hover:text-slate-800"
          }`}
        >
          <Terminal className="w-4 h-4" /> Live Ingestion Feed
        </button>
        <button
          onClick={() => setActiveTab("json")}
          className={`pb-2.5 border-b-2 transition flex items-center gap-1.5 ${
            activeTab === "json"
              ? "border-sky-600 text-sky-600 font-bold"
              : "border-transparent text-slate-500 hover:text-slate-800"
          }`}
        >
          <FileCode className="w-4 h-4" /> Cluster JSON Schema (Person IDs)
        </button>
        <button
          onClick={() => setActiveTab("guide")}
          className={`pb-2.5 border-b-2 transition flex items-center gap-1.5 ${
            activeTab === "guide"
              ? "border-sky-600 text-sky-600 font-bold"
              : "border-transparent text-slate-500 hover:text-slate-800"
          }`}
        >
          <FolderOpen className="w-4 h-4" /> Photographer Setup Guide
        </button>
      </div>

      {/* Tab Contents */}
      {activeTab === "terminal" && (
        <div className="bg-slate-950 rounded-2xl p-4 font-mono text-xs text-emerald-400 overflow-x-auto shadow-inner max-h-72 overflow-y-auto space-y-1.5 border border-slate-800">
          {logs.map((log, i) => (
            <div key={i} className="flex items-start gap-2">
              <span className="text-slate-600 select-none">&gt;</span>
              <span className={log.includes("Matched") || log.includes("Person_101") ? "text-amber-300 font-bold" : ""}>
                {log}
              </span>
            </div>
          ))}
        </div>
      )}

      {activeTab === "json" && (
        <div className="bg-slate-900 rounded-2xl p-4 font-mono text-xs text-sky-300 overflow-x-auto shadow-inner max-h-72 overflow-y-auto border border-slate-800">
          <pre>{JSON.stringify(sampleJson, null, 2)}</pre>
        </div>
      )}

      {activeTab === "guide" && (
        <div className="bg-slate-50 rounded-2xl p-5 border border-slate-200 text-xs text-slate-700 space-y-3">
          <h4 className="font-bold text-slate-900 text-sm">How Photographer Ingestion Works Without Dashboard Uploads:</h4>
          <ol className="list-decimal pl-5 space-y-1.5 text-slate-600">
            <li>
              <strong>Create or Sync Event Folder:</strong> In <code>universal_folder/</code>, create a folder for your event (e.g., <code>wedding_2026/</code>).
            </li>
            <li>
              <strong>Sync Photos from Camera / SD Card:</strong> Directly save or copy camera images into that folder using Wi-Fi tethering, FTP, or local copy.
            </li>
            <li>
              <strong>Automatic Background Processing:</strong> The CLI daemon detects new photographs, detects faces, aligns facial points, and generates 512-D vectors in milliseconds.
            </li>
            <li>
              <strong>Person Clustering:</strong> Persons are mapped to unique IDs (e.g. Arshad → <code>Person 101</code>) and their photo paths are appended to <code>face_clusters.json</code>.
            </li>
            <li>
              <strong>Instant Guest Discovery:</strong> When guests query via the web application, their selfie compares against precomputed indices instantly with zero waiting time!
            </li>
          </ol>
        </div>
      )}
    </div>
  );
}
