"use client";

import { useState } from "react";
import {
  Download,
  Calendar,
  Sparkles,
  CheckCircle,
  Eye,
  Flag,
  Share2,
  FolderDown,
  Layers,
  ArrowRight,
  ExternalLink
} from "lucide-react";
import WrongMatchModal from "./WrongMatchModal";

export interface MatchedPhoto {
  photo_id: string;
  filename: string;
  similarity: number;
  confidence_percentage: number;
  image_url: string;
  width: number;
  height: number;
  created_at: string;
}

export interface GroupedEvent {
  event_id: string;
  event_name: string;
  description?: string;
  organizer_name?: string;
  created_at?: string;
  total_matches: number;
  photos: MatchedPhoto[];
}

interface MultiEventGalleryProps {
  groupedEvents: GroupedEvent[];
  totalPhotos: number;
}

export default function MultiEventGallery({ groupedEvents, totalPhotos }: MultiEventGalleryProps) {
  const [selectedPhoto, setSelectedPhoto] = useState<MatchedPhoto | null>(null);
  const [selectedEventId, setSelectedEventId] = useState<string>("");
  const [reportPhotoId, setReportPhotoId] = useState<string | null>(null);
  const [downloadingEventId, setDownloadingEventId] = useState<string | null>(null);
  const [copiedLink, setCopiedLink] = useState(false);

  if (groupedEvents.length === 0) {
    return (
      <div className="bg-white rounded-3xl p-10 text-center max-w-lg mx-auto border border-slate-200 shadow-sm mt-8">
        <Layers className="w-12 h-12 text-slate-300 mx-auto mb-3" />
        <h3 className="text-base font-bold text-slate-800">No Matching Photos Discovered</h3>
        <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          We searched through all indexed events in FindZora. We couldn't find matching photographs exceeding our confidence threshold.
        </p>
      </div>
    );
  }

  // Simulated Single-Click Batch Download for an entire event
  const handleBatchDownloadEvent = async (eventItem: GroupedEvent) => {
    setDownloadingEventId(eventItem.event_id);
    try {
      // Trigger download for each photo sequentially
      for (const p of eventItem.photos) {
        const link = document.createElement("a");
        link.href = p.image_url;
        link.download = `${eventItem.event_name.replace(/\s+/g, "_")}_${p.filename}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        await new Promise((resolve) => setTimeout(resolve, 300));
      }
    } finally {
      setDownloadingEventId(null);
    }
  };

  const handleShare = (photo: MatchedPhoto) => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(window.location.origin + photo.image_url);
      setCopiedLink(true);
      setTimeout(() => setCopiedLink(false), 2000);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8 mt-6">
      {/* Universal Overview Banner */}
      <div className="bg-gradient-to-r from-sky-600 via-indigo-600 to-purple-600 rounded-3xl p-6 sm:p-8 text-white shadow-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-white text-xs font-bold mb-2">
            <Sparkles className="w-3.5 h-3.5" /> Universal Multi-Event Attendee Discovery
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Found {totalPhotos} Photos Across {groupedEvents.length} Event{groupedEvents.length === 1 ? "" : "s"}
          </h2>
          <p className="text-xs sm:text-sm text-sky-100 mt-1 max-w-xl">
            Your single verification selfie was matched across all precomputed indexes. Photos are automatically categorized by event with one-click batch downloads.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-white/10 backdrop-blur-md px-4 py-3 rounded-2xl border border-white/20 text-xs">
          <Calendar className="w-5 h-5 text-sky-200" />
          <div>
            <div className="font-bold">{groupedEvents.length} Verified Events</div>
            <div className="text-[11px] text-sky-200">Grouped Categorization</div>
          </div>
        </div>
      </div>

      {/* Grouped Event Sections */}
      <div className="space-y-8">
        {groupedEvents.map((evt, evtIndex) => (
          <div
            key={evt.event_id}
            className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-5"
          >
            {/* Event Header with One-Click Batch Download Button */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-5">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
                    Event #{evtIndex + 1}
                  </span>
                  <h3 className="text-xl font-bold text-slate-900">{evt.event_name}</h3>
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  {evt.description || "Event photos securely indexed in FindZora"} • {evt.photos.length} matching photograph{evt.photos.length === 1 ? "" : "s"}
                </p>
              </div>

              {/* Single Click Download Button for this entire event */}
              <button
                onClick={() => handleBatchDownloadEvent(evt)}
                disabled={downloadingEventId === evt.event_id}
                className="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-semibold text-xs rounded-2xl shadow-md shadow-emerald-100 transition flex items-center justify-center gap-2 disabled:opacity-50"
              >
                <FolderDown className="w-4 h-4" />
                {downloadingEventId === evt.event_id ? (
                  <span>Downloading All ({evt.photos.length})...</span>
                ) : (
                  <span>Download All Event Photos ({evt.photos.length})</span>
                )}
              </button>
            </div>

            {/* Photo Grid for this Event */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {evt.photos.map((p) => (
                <div
                  key={p.photo_id}
                  className="group relative bg-white rounded-2xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col"
                >
                  <div
                    className="relative aspect-[4/3] bg-slate-100 overflow-hidden cursor-pointer"
                    onClick={() => {
                      setSelectedPhoto(p);
                      setSelectedEventId(evt.event_id);
                    }}
                  >
                    <img
                      src={p.image_url}
                      alt={p.filename}
                      className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                      loading="lazy"
                    />
                    <div className="absolute top-2 left-2 bg-slate-900/80 backdrop-blur-md text-white text-[11px] font-semibold px-2 py-0.5 rounded-full flex items-center gap-1">
                      <CheckCircle className="w-3 h-3 text-emerald-400" />
                      {p.confidence_percentage}% Match
                    </div>
                  </div>

                  <div className="p-3 flex items-center justify-between bg-white border-t border-slate-100 mt-auto">
                    <span className="text-xs text-slate-600 truncate max-w-[120px]" title={p.filename}>
                      {p.filename}
                    </span>
                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => {
                          setSelectedPhoto(p);
                          setSelectedEventId(evt.event_id);
                        }}
                        className="p-1.5 text-slate-500 hover:text-sky-600 hover:bg-sky-50 rounded-lg transition"
                        title="View Full Size"
                      >
                        <Eye className="w-3.5 h-3.5" />
                      </button>
                      <a
                        href={p.image_url}
                        download={`${evt.event_name}_${p.filename}`}
                        className="p-1.5 text-slate-500 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition"
                        title="Download Single Photo"
                      >
                        <Download className="w-3.5 h-3.5" />
                      </a>
                      <button
                        onClick={() => {
                          setReportPhotoId(p.photo_id);
                          setSelectedEventId(evt.event_id);
                        }}
                        className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
                        title="Report Wrong Match"
                      >
                        <Flag className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Lightbox Modal */}
      {selectedPhoto && (
        <div
          className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4"
          onClick={() => setSelectedPhoto(null)}
        >
          <div
            className="max-w-4xl max-h-[90vh] bg-white rounded-3xl overflow-hidden shadow-2xl flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-4 border-b border-slate-100 flex items-center justify-between">
              <div>
                <h4 className="font-semibold text-slate-800 text-sm">{selectedPhoto.filename}</h4>
                <p className="text-xs text-slate-500">
                  Confidence: {selectedPhoto.confidence_percentage}% • {selectedPhoto.width}x{selectedPhoto.height} px
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleShare(selectedPhoto)}
                  className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition"
                >
                  <Share2 className="w-3.5 h-3.5" />
                  {copiedLink ? "Link Copied!" : "Share Link"}
                </button>
                <a
                  href={selectedPhoto.image_url}
                  download={selectedPhoto.filename}
                  className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5"
                >
                  <Download className="w-3.5 h-3.5" />
                  Download
                </a>
                <button
                  onClick={() => setReportPhotoId(selectedPhoto.photo_id)}
                  className="px-3 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-xl text-xs font-semibold flex items-center gap-1.5"
                >
                  <Flag className="w-3.5 h-3.5" />
                  Report Wrong Match
                </button>
                <button
                  onClick={() => setSelectedPhoto(null)}
                  className="px-3 py-1.5 text-slate-500 hover:text-slate-800 text-xs font-medium"
                >
                  Close
                </button>
              </div>
            </div>
            <div className="p-2 bg-slate-900 flex items-center justify-center overflow-auto max-h-[75vh]">
              <img
                src={selectedPhoto.image_url}
                alt={selectedPhoto.filename}
                className="max-h-[72vh] max-w-full object-contain rounded-lg"
              />
            </div>
          </div>
        </div>
      )}

      {/* Wrong Match Feedback Modal */}
      <WrongMatchModal
        isOpen={Boolean(reportPhotoId)}
        photoId={reportPhotoId}
        eventId={selectedEventId}
        onClose={() => setReportPhotoId(null)}
      />
    </div>
  );
}
