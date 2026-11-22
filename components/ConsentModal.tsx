"use client";

import { useState } from "react";
import { ShieldCheck, AlertCircle, CheckCircle } from "lucide-react";

interface ConsentModalProps {
  isOpen: boolean;
  eventName: string;
  onConsentGiven: (attendeeName: string) => void;
  onCancel: () => void;
}

export default function ConsentModal({ isOpen, eventName, onConsentGiven, onCancel }: ConsentModalProps) {
  const [attendeeName, setAttendeeName] = useState("");
  const [agreed, setAgreed] = useState(false);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 flex flex-col gap-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-sky-100 text-sky-700 rounded-xl">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Biometric Informed Consent</h3>
            <p className="text-xs text-slate-500">Event Scope: {eventName}</p>
          </div>
        </div>

        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs text-slate-600 space-y-2.5 max-h-60 overflow-y-auto">
          <p className="font-semibold text-slate-800">
            Before proceeding, please read and confirm the following privacy safeguards:
          </p>
          <ul className="list-disc pl-4 space-y-1.5">
            <li>
              <strong>Purpose-Bound Discovery:</strong> Your selfie will be used exclusively to generate a mathematical face vector to match photos from this event.
            </li>
            <li>
              <strong>Event Isolation:</strong> Vector search is strictly restricted to "{eventName}". Your biometric data is never searched across other events or third parties.
            </li>
            <li>
              <strong>Ephemeral Processing:</strong> Your temporary selfie photo is deleted from the server immediately after query embedding generation. Raw vectors are never stored in your browser.
            </li>
            <li>
              <strong>Conservative Thresholding:</strong> The system applies high similarity thresholds to avoid false matches. You can flag any incorrect match via the feedback tool.
            </li>
          </ul>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">
            Attendee Alias / Name (Optional)
          </label>
          <input
            type="text"
            placeholder="e.g. Alex Smith (or leave blank)"
            value={attendeeName}
            onChange={(e) => setAttendeeName(e.target.value)}
            className="w-full text-sm px-3.5 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
          />
        </div>

        <label className="flex items-start gap-2.5 text-xs text-slate-700 cursor-pointer pt-1">
          <input
            type="checkbox"
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
            className="mt-0.5 rounded text-sky-600 focus:ring-sky-500"
          />
          <span>
            I understand and give consent to generate a temporary biometric vector for finding my photos in this event.
          </span>
        </label>

        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            onClick={onCancel}
            className="px-4 py-2 text-sm text-slate-600 hover:text-slate-800 font-medium transition"
          >
            Cancel
          </button>
          <button
            disabled={!agreed}
            onClick={() => onConsentGiven(attendeeName || "Anonymous Attendee")}
            className={`px-5 py-2 rounded-xl text-sm font-semibold text-white shadow-md transition flex items-center gap-2 ${
              agreed
                ? "bg-sky-600 hover:bg-sky-700 shadow-sky-200"
                : "bg-slate-300 cursor-not-allowed"
            }`}
          >
            <CheckCircle className="w-4 h-4" />
            Agree & Capture Selfie
          </button>
        </div>
      </div>
    </div>
  );
}
