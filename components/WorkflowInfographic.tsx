"use client";

import { useState } from "react";
import { Sparkles, ZoomIn, Eye, CheckCircle2, ShieldAlert, Rocket, Layers } from "lucide-react";

export default function WorkflowInfographic() {
  const [showLightbox, setShowLightbox] = useState(false);
  const [activeStage, setActiveStage] = useState<number | null>(null);

  const stages = [
    {
      range: "Steps 1–6",
      title: "Event Creation & Batch Ingestion",
      color: "border-sky-500 bg-sky-50 text-sky-800",
      details: "Organizer logs in, creates an event, generates guest links/QR codes, and uploads photographs (via Web or Universal Watch Folder CLI). Photos automatically queue for AI analysis."
    },
    {
      range: "Steps 7–10",
      title: "Face Detection, Alignment & Vector Indexing",
      color: "border-indigo-500 bg-indigo-50 text-indigo-800",
      details: "AI detects all faces (single, couple, group), checks quality, extracts geometric facial points, and generates 512-D L2-normalized embeddings stored in the isolated FAISS vector database."
    },
    {
      range: "Steps 11–17",
      title: "Consent, Camera Selfie & Multi-Event Gallery",
      color: "border-emerald-500 bg-emerald-50 text-emerald-800",
      details: "Guest opens link or Universal Portal, agrees to biometric consent, captures a selfie, and instantly discovers grouped photos across events with single-click batch downloads."
    },
    {
      range: "Step 18",
      title: "Insights, Feedback & Auto-Retention",
      color: "border-amber-500 bg-amber-50 text-amber-800",
      details: "Organizers track analytics (faces indexed, searches conducted), review attendee wrong-match feedback, and enforce GDPR/privacy auto-retention policies."
    }
  ];

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-100 text-sky-800 text-xs font-bold mb-2">
            <Sparkles className="w-3.5 h-3.5" /> Complete A-to-Z Workflow Architecture
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
            How FindZora Works — End-to-End Visual Guide
          </h2>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Official 18-step pipeline from photographer studio upload to instant guest discovery & batch downloads.
          </p>
        </div>

        <button
          onClick={() => setShowLightbox(true)}
          className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-xl shadow transition flex items-center gap-2"
        >
          <ZoomIn className="w-4 h-4" /> Full-Screen Diagram
        </button>
      </div>

      {/* Embedded Infographic Preview */}
      <div
        onClick={() => setShowLightbox(true)}
        className="relative group rounded-2xl overflow-hidden border border-slate-200 bg-slate-950 cursor-pointer shadow-inner flex items-center justify-center max-h-[440px]"
      >
        <img
          src="/images/findzora_workflow_infographic.jpg"
          alt="Complete Workflow of FindZora from Event Creation to Photo Search (A to Z)"
          className="w-full h-auto object-contain transition duration-300 group-hover:scale-[1.01]"
        />
        <div className="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-white gap-2 font-semibold text-sm">
          <Eye className="w-5 h-5" /> Click to View High-Resolution Architecture Chart
        </div>
      </div>

      {/* Stage Breakdown Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
        {stages.map((stage, idx) => (
          <div
            key={idx}
            className={`p-4 rounded-2xl border-2 transition ${stage.color} hover:shadow-md cursor-default`}
          >
            <span className="text-[11px] font-bold uppercase tracking-wider block opacity-75">
              {stage.range}
            </span>
            <h4 className="font-bold text-sm mt-0.5">{stage.title}</h4>
            <p className="text-xs mt-1.5 opacity-90 leading-relaxed">{stage.details}</p>
          </div>
        ))}
      </div>

      {/* Lightbox Modal */}
      {showLightbox && (
        <div
          className="fixed inset-0 z-50 bg-slate-950/90 backdrop-blur-md flex items-center justify-center p-4"
          onClick={() => setShowLightbox(false)}
        >
          <div
            className="max-w-6xl max-h-[95vh] bg-white rounded-3xl overflow-hidden shadow-2xl flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-4 border-b border-slate-200 flex items-center justify-between">
              <div>
                <h3 className="font-bold text-slate-900 text-sm">
                  Complete Workflow of FindZora — From Event Creation to Photo Search (A to Z)
                </h3>
                <p className="text-xs text-slate-500">18 Sequential Steps • Current Implementation & Future Scope</p>
              </div>
              <button
                onClick={() => setShowLightbox(false)}
                className="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 rounded-xl text-xs font-semibold text-slate-700"
              >
                Close (ESC)
              </button>
            </div>
            <div className="p-3 bg-slate-100 overflow-auto max-h-[85vh] flex items-center justify-center">
              <img
                src="/images/findzora_workflow_infographic.jpg"
                alt="FindZora Full Workflow"
                className="max-w-full h-auto rounded-xl shadow"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
