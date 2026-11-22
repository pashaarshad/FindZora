"use client";

import { useState } from "react";
import { Download, Flag, Eye, CheckCircle, ShieldAlert, Sparkles } from "lucide-react";
import WrongMatchModal from "./WrongMatchModal";

interface Candidate {
  photo_id: string;
  filename: string;
  similarity: number;
  confidence_percentage: number;
  image_url: string;
  width: number;
  height: number;
  created_at: string;
}

interface CandidateGalleryProps {
  candidates: Candidate[];
  eventId: string;
  eventName: string;
}

export default function CandidateGallery({ candidates, eventId, eventName }: CandidateGalleryProps) {
  const [selectedPhoto, setSelectedPhoto] = useState<Candidate | null>(null);
  const [reportPhotoId, setReportPhotoId] = useState<string | null>(null);

  if (candidates.length === 0) {
    return (
      <div className="bg-white rounded-2xl p-8 text-center max-w-lg mx-auto border border-slate-200 mt-6 shadow-sm">
        <ShieldAlert className="w-10 h-10 text-amber-500 mx-auto mb-3" />
        <h3 className="text-base font-bold text-slate-800">No Matching Photos Found</h3>
        <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          We didn't find photos exceeding the similarity threshold in "{eventName}". Photos may still be processing or lighting/angle differed significantly.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto mt-8 px-4">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-sky-600" />
            Discovered Photographs ({candidates.length})
          </h2>
          <p className="text-xs text-slate-500">
            Ranked by ArcFace cosine vector similarity within "{eventName}"
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {candidates.map((photo) => (
          <div
            key={photo.photo_id}
            className="group relative bg-white rounded-2xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col"
          >
            <div className="relative aspect-[4/3] bg-slate-100 overflow-hidden cursor-pointer" onClick={() => setSelectedPhoto(photo)}>
              <img
                src={photo.image_url}
                alt={photo.filename}
                className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                loading="lazy"
              />
              <div className="absolute top-2 left-2 bg-slate-900/80 backdrop-blur-md text-white text-[11px] font-semibold px-2 py-0.5 rounded-full flex items-center gap-1">
                <CheckCircle className="w-3 h-3 text-emerald-400" />
                {photo.confidence_percentage}% match
              </div>
            </div>

            <div className="p-3 flex items-center justify-between mt-auto bg-white border-t border-slate-100">
              <span className="text-xs text-slate-600 truncate max-w-[130px]" title={photo.filename}>
                {photo.filename}
              </span>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setSelectedPhoto(photo)}
                  className="p-1.5 text-slate-500 hover:text-sky-600 hover:bg-sky-50 rounded-lg transition"
                  title="View Full Size"
                >
                  <Eye className="w-3.5 h-3.5" />
                </button>
                <a
                  href={photo.image_url}
                  download={photo.filename}
                  className="p-1.5 text-slate-500 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition"
                  title="Download Photo"
                >
                  <Download className="w-3.5 h-3.5" />
                </a>
                <button
                  onClick={() => setReportPhotoId(photo.photo_id)}
                  className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
                  title="Report Inaccurate Match"
                >
                  <Flag className="w-3.5 h-3.5" />
                </button>
              </div>
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
            className="max-w-4xl max-h-[90vh] bg-white rounded-2xl overflow-hidden shadow-2xl flex flex-col"
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
                <a
                  href={selectedPhoto.image_url}
                  download={selectedPhoto.filename}
                  className="px-3 py-1.5 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5"
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
        eventId={eventId}
        onClose={() => setReportPhotoId(null)}
      />
    </div>
  );
}
