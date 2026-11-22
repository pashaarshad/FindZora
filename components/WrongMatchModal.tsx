"use client";

import { useState } from "react";
import { Flag, X, Check } from "lucide-react";

interface WrongMatchModalProps {
  isOpen: boolean;
  photoId: string | null;
  eventId: string;
  onClose: () => void;
}

export default function WrongMatchModal({ isOpen, photoId, eventId, onClose }: WrongMatchModalProps) {
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  if (!isOpen || !photoId) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await fetch(`/api/events/${eventId}/report-wrong-match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          photo_id: photoId,
          attendee_notes: notes || "I do not appear in this photo.",
        }),
      });
      if (res.ok) {
        setSubmitted(true);
        setTimeout(() => {
          setSubmitted(false);
          setNotes("");
          onClose();
        }, 1500);
      }
    } catch (err) {
      console.error("Report submission failed:", err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-100 flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5 text-rose-600 font-bold text-base">
            <Flag className="w-5 h-5" />
            Report Inaccurate Match
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        {submitted ? (
          <div className="p-4 bg-emerald-50 text-emerald-800 rounded-xl flex items-center gap-2 text-sm font-semibold">
            <Check className="w-5 h-5 text-emerald-600" />
            Report recorded! Thank you for helping keep FindZora accurate.
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <p className="text-xs text-slate-600">
              Does this photograph not show you? Organizers can review reported matches to refine calibration thresholds and protect privacy.
            </p>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Reason / Details (Optional)
              </label>
              <textarea
                rows={3}
                placeholder="e.g. Someone resembling me was misidentified, or this is a different person."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="w-full text-xs p-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-rose-500 focus:outline-none"
              />
            </div>

            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-medium text-slate-600 hover:text-slate-800"
              >
                Dismiss
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold rounded-xl shadow-sm transition disabled:opacity-50"
              >
                {submitting ? "Submitting..." : "Submit Report"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
