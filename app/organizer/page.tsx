"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  UploadCloud,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Scan,
  Trash2,
  ShieldAlert,
  ArrowLeft,
  FileImage,
  RefreshCw,
  Layers,
  Flag,
  FolderSync
} from "lucide-react";
import BoundingBoxViewer from "@/components/BoundingBoxViewer";
import WatchFolderConsole from "@/components/WatchFolderConsole";

export default function OrganizerDashboard() {
  const [organizerMode, setOrganizerMode] = useState<"watch_folder" | "manual_upload">("watch_folder");
  const [events, setEvents] = useState<any[]>([]);
  const [selectedEventId, setSelectedEventId] = useState<string>("");
  const [photos, setPhotos] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [reports, setReports] = useState<any[]>([]);
  const [inspectPhoto, setInspectPhoto] = useState<any | null>(null);

  // Upload state
  const [uploadFiles, setUploadFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any | null>(null);

  useEffect(() => {
    fetchEvents();
    fetchAdminJobs();
    fetchReports();
  }, []);

  useEffect(() => {
    if (selectedEventId) {
      fetchEventPhotos(selectedEventId);
    }
  }, [selectedEventId]);

  const fetchEvents = async () => {
    try {
      const res = await fetch("/api/events");
      if (res.ok) {
        const data = await res.json();
        setEvents(data);
        if (data.length > 0 && !selectedEventId) {
          setSelectedEventId(data[0].id);
        }
      }
    } catch (e) {
      console.error(e);
    }
  };

  const fetchEventPhotos = async (eventId: string) => {
    try {
      const res = await fetch(`/api/events/${eventId}/photos`);
      if (res.ok) {
        const data = await res.json();
        setPhotos(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const fetchAdminJobs = async () => {
    try {
      const res = await fetch("/api/admin/jobs");
      if (res.ok) {
        const data = await res.json();
        setJobs(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const fetchReports = async () => {
    try {
      const res = await fetch("/api/admin/reports");
      if (res.ok) {
        const data = await res.json();
        setReports(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleBatchUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedEventId || uploadFiles.length === 0) return;

    setIsUploading(true);
    setUploadResult(null);

    const formData = new FormData();
    uploadFiles.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const res = await fetch(`/api/events/${selectedEventId}/photos/batch`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setUploadResult(data);
      setUploadFiles([]);
      fetchEventPhotos(selectedEventId);
      fetchAdminJobs();
    } catch (err) {
      console.error("Batch upload failed:", err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleRetryJob = async (jobId: string) => {
    try {
      await fetch(`/api/admin/jobs/${jobId}/retry`, { method: "POST" });
      fetchAdminJobs();
      if (selectedEventId) fetchEventPhotos(selectedEventId);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteEvent = async (eventId: string) => {
    if (!confirm("Are you sure you want to delete this event? All indexed photos and vector embeddings will be permanently purged.")) {
      return;
    }
    try {
      await fetch(`/api/events/${eventId}`, { method: "DELETE" });
      fetchEvents();
      setPhotos([]);
      setInspectPhoto(null);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <Link href="/" className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 mb-2">
            <ArrowLeft className="w-4 h-4" /> Back to Home
          </Link>
          <h1 className="text-2xl font-extrabold text-slate-900">Organizer & Studio Command Center</h1>
          <p className="text-xs text-slate-500">Universal folder CLI auto-sync, batch uploads, face box inspection & cluster audit</p>
        </div>

        {/* Mode Switcher */}
        <div className="flex items-center gap-2 p-1 bg-slate-100 rounded-xl border border-slate-200">
          <button
            onClick={() => setOrganizerMode("watch_folder")}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              organizerMode === "watch_folder" ? "bg-white text-emerald-700 shadow-sm" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <FolderSync className="w-3.5 h-3.5" /> Watch Folder CLI
          </button>
          <button
            onClick={() => setOrganizerMode("manual_upload")}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              organizerMode === "manual_upload" ? "bg-white text-sky-700 shadow-sm" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <UploadCloud className="w-3.5 h-3.5" /> Web Batch Upload
          </button>
        </div>
      </div>

      {/* Main Mode View */}
      {organizerMode === "watch_folder" ? (
        <WatchFolderConsole />
      ) : (
        /* Manual Web Batch Ingestion */
        <div className="space-y-6">
          <div className="flex items-center justify-between bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
            <div className="flex items-center gap-2">
              <label className="text-xs font-bold text-slate-700">Target Event:</label>
              <select
                value={selectedEventId}
                onChange={(e) => setSelectedEventId(e.target.value)}
                className="text-xs font-semibold px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-sky-500"
              >
                {events.map((evt) => (
                  <option key={evt.id} value={evt.id}>
                    {evt.name} ({evt.total_photos} photos)
                  </option>
                ))}
              </select>
            </div>
            {selectedEventId && (
              <button
                onClick={() => handleDeleteEvent(selectedEventId)}
                className="p-2 text-rose-600 hover:bg-rose-50 rounded-xl transition flex items-center gap-1.5 text-xs font-semibold"
                title="Purge Event Storage"
              >
                <Trash2 className="w-4 h-4" /> Delete Event
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Batch Photo Upload Card */}
            <div className="lg:col-span-2 bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-1">
                  <UploadCloud className="w-5 h-5 text-sky-600" />
                  Manual Batch Photo Upload
                </h2>
                <p className="text-xs text-slate-500 mb-4">
                  Upload multiple JPEG/PNG event photographs. Precomputed face detection and ArcFace embeddings will automatically queue in the background.
                </p>

                <form onSubmit={handleBatchUpload} className="space-y-4">
                  <div className="border-2 border-dashed border-slate-200 hover:border-sky-500 rounded-2xl p-6 text-center cursor-pointer transition bg-slate-50">
                    <input
                      type="file"
                      multiple
                      accept="image/jpeg,image/png,image/webp"
                      onChange={(e) => {
                        if (e.target.files) {
                          setUploadFiles(Array.from(e.target.files));
                        }
                      }}
                      className="hidden"
                      id="batch-input"
                    />
                    <label htmlFor="batch-input" className="cursor-pointer flex flex-col items-center">
                      <FileImage className="w-8 h-8 text-sky-500 mb-2" />
                      <span className="text-xs font-semibold text-slate-700">
                        {uploadFiles.length > 0 ? `${uploadFiles.length} files selected` : "Click or drag event photos here"}
                      </span>
                      <span className="text-[11px] text-slate-400 mt-1">Supports JPG, PNG up to 25MB each</span>
                    </label>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-500">
                      Target event: <span className="font-semibold text-slate-700">{events.find((e) => e.id === selectedEventId)?.name || "Select an event"}</span>
                    </span>
                    <button
                      type="submit"
                      disabled={isUploading || uploadFiles.length === 0}
                      className="px-5 py-2.5 bg-sky-600 hover:bg-sky-700 text-white text-xs font-semibold rounded-xl shadow-md transition disabled:opacity-50 flex items-center gap-2"
                    >
                      {isUploading ? (
                        <>
                          <RefreshCw className="w-4 h-4 animate-spin" /> Ingesting & Indexing...
                        </>
                      ) : (
                        <>
                          <UploadCloud className="w-4 h-4" /> Start Ingestion ({uploadFiles.length})
                        </>
                      )}
                    </button>
                  </div>
                </form>

                {uploadResult && (
                  <div className="mt-4 p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 space-y-1">
                    <p className="font-bold flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                      Ingestion complete: {uploadResult.successful} uploaded & queued.
                    </p>
                    {uploadResult.duplicates_skipped > 0 && (
                      <p className="text-[11px] text-amber-700">
                        ⚠️ {uploadResult.duplicates_skipped} duplicate file(s) skipped based on SHA-256 hash.
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Quick System Stats */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-4">
                <Layers className="w-5 h-5 text-indigo-600" />
                Ingestion Pipeline Stats
              </h2>
              <div className="space-y-3">
                <div className="p-3 bg-slate-50 rounded-xl flex items-center justify-between text-xs">
                  <span className="text-slate-600 font-medium">Uploaded Event Photos:</span>
                  <span className="font-bold text-slate-900">{photos.length}</span>
                </div>
                <div className="p-3 bg-emerald-50 rounded-xl flex items-center justify-between text-xs">
                  <span className="text-emerald-700 font-medium">Indexed Face Vectors:</span>
                  <span className="font-bold text-emerald-900">
                    {photos.reduce((sum, p) => sum + (p.face_count || 0), 0)}
                  </span>
                </div>
                <div className="p-3 bg-amber-50 rounded-xl flex items-center justify-between text-xs">
                  <span className="text-amber-700 font-medium">Recent Processing Jobs:</span>
                  <span className="font-bold text-amber-900">{jobs.length}</span>
                </div>
                <div className="p-3 bg-rose-50 rounded-xl flex items-center justify-between text-xs">
                  <span className="text-rose-700 font-medium">Wrong-Match Reports:</span>
                  <span className="font-bold text-rose-900">{reports.length}</span>
                </div>
              </div>
              <button
                onClick={() => {
                  if (selectedEventId) fetchEventPhotos(selectedEventId);
                  fetchAdminJobs();
                  fetchReports();
                }}
                className="mt-4 w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl transition flex items-center justify-center gap-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" /> Refresh Dashboard
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Face Bounding Box Inspector */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Scan className="w-5 h-5 text-emerald-600" />
              Face Detection & Quality Inspector
            </h2>
            <p className="text-xs text-slate-500">
              Select any event photograph to inspect detected face bounding boxes, alignment and quality gate results.
            </p>
          </div>
          {inspectPhoto && (
            <button
              onClick={() => setInspectPhoto(null)}
              className="text-xs font-semibold text-slate-500 hover:text-slate-800"
            >
              Close Inspector
            </button>
          )}
        </div>

        {inspectPhoto ? (
          <BoundingBoxViewer
            photoId={inspectPhoto.id}
            filename={inspectPhoto.filename}
            streamUrl={inspectPhoto.stream_url}
          />
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-3 max-h-80 overflow-y-auto p-1">
            {photos.map((p) => (
              <div
                key={p.id}
                onClick={() => setInspectPhoto(p)}
                className="group relative aspect-square rounded-xl overflow-hidden bg-slate-100 border border-slate-200 cursor-pointer hover:border-emerald-500 transition"
              >
                <img src={p.stream_url} alt={p.filename} className="w-full h-full object-cover" />
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex flex-col items-center justify-center text-white text-[10px] font-semibold p-1 text-center">
                  <Scan className="w-4 h-4 mb-1" />
                  <span>Inspect {p.face_count} Face(s)</span>
                </div>
                <div className="absolute bottom-1 right-1 bg-black/70 text-emerald-300 text-[9px] font-mono px-1.5 py-0.5 rounded">
                  {p.face_count}F
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Background Processing Queue Log */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-1">
          <RotateCcw className="w-5 h-5 text-sky-600" />
          Recent Processing Queue Jobs
        </h2>
        <p className="text-xs text-slate-500 mb-4">
          Shows image validation, quality filtering, and vector indexing statuses.
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 font-semibold border-y border-slate-200">
              <tr>
                <th className="py-2.5 px-3">Job ID</th>
                <th className="py-2.5 px-3">Photo ID</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3">Attempts</th>
                <th className="py-2.5 px-3">Timestamp</th>
                <th className="py-2.5 px-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {jobs.slice(0, 10).map((j) => (
                <tr key={j.id} className="hover:bg-slate-50">
                  <td className="py-2 px-3 font-mono text-[11px] text-slate-600">{j.id.slice(0, 8)}...</td>
                  <td className="py-2 px-3 font-mono text-[11px] text-slate-600">{j.photo_id.slice(0, 8)}...</td>
                  <td className="py-2 px-3">
                    <span
                      className={`inline-block px-2 py-0.5 rounded-full font-semibold text-[10px] ${
                        j.status === "completed"
                          ? "bg-emerald-50 text-emerald-700"
                          : j.status === "failed"
                          ? "bg-rose-50 text-rose-700"
                          : "bg-amber-50 text-amber-700"
                      }`}
                    >
                      {j.status}
                    </span>
                  </td>
                  <td className="py-2 px-3">{j.attempts}</td>
                  <td className="py-2 px-3 text-slate-400">{new Date(j.created_at).toLocaleTimeString()}</td>
                  <td className="py-2 px-3">
                    {j.status === "failed" && (
                      <button
                        onClick={() => handleRetryJob(j.id)}
                        className="text-sky-600 hover:text-sky-800 font-semibold"
                      >
                        Retry
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
