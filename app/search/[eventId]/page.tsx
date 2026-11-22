"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/link";
import Link from "next/link";
import { ShieldCheck, ArrowLeft, Lock, Sparkles, AlertCircle, RefreshCw } from "lucide-react";
import ConsentModal from "@/components/ConsentModal";
import CameraCapture from "@/components/CameraCapture";
import CandidateGallery from "@/components/CandidateGallery";

export default function AttendeeSearchPage() {
  const params = useParams();
  const eventId = params?.eventId as string;

  const [eventData, setEventData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [passcode, setPasscode] = useState("");
  const [passcodeNeeded, setPasscodeNeeded] = useState(false);
  const [passcodeError, setPasscodeError] = useState("");

  // Consent & Search state
  const [hasConsented, setHasConsented] = useState(false);
  const [showConsentModal, setShowConsentModal] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [searchResult, setSearchResult] = useState<any>(null);
  const [searchError, setSearchError] = useState<string | null>(null);

  useEffect(() => {
    if (eventId) {
      loadEvent();
    }
  }, [eventId]);

  const loadEvent = async (codeToTry: string = "") => {
    setLoading(true);
    setPasscodeError("");
    try {
      const url = codeToTry
        ? `/api/events/${eventId}?passcode=${encodeURIComponent(codeToTry)}`
        : `/api/events/${eventId}`;
      const res = await fetch(url);
      if (res.status === 403) {
        setPasscodeNeeded(true);
        setPasscodeError(codeToTry ? "Invalid event passcode. Please re-enter." : "");
      } else if (res.ok) {
        const data = await res.json();
        setEventData(data);
        setPasscodeNeeded(false);
        // Show consent modal on initial entry
        setShowConsentModal(true);
      } else {
        setPasscodeError("Event not found or expired.");
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleConsentGiven = async (attendeeName: string) => {
    try {
      await fetch(`/api/events/${eventId}/consent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ attendee_name: attendeeName }),
      });
      setHasConsented(true);
      setShowConsentModal(false);
    } catch (err) {
      console.error("Consent log failed:", err);
      setHasConsented(true);
      setShowConsentModal(false);
    }
  };

  const handleSelfieSearch = async (selfieBlob: Blob) => {
    setIsSearching(true);
    setSearchError(null);
    setSearchResult(null);

    const formData = new FormData();
    formData.append("selfie", selfieBlob, "selfie_capture.jpg");
    formData.append("threshold", "0.55");
    formData.append("top_k", "50");

    try {
      const res = await fetch(`/api/events/${eventId}/search`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Search failed");
      }
      setSearchResult(data);
    } catch (err: any) {
      setSearchError(err.message || "Failed to process search.");
    } finally {
      setIsSearching(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center text-slate-400">
        <RefreshCw className="w-6 h-6 animate-spin mr-2" />
        Loading event details...
      </div>
    );
  }

  if (passcodeNeeded) {
    return (
      <div className="max-w-md mx-auto mt-16 p-6 bg-white rounded-2xl border border-slate-200 shadow-sm text-center">
        <div className="w-12 h-12 bg-amber-100 text-amber-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <Lock className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-slate-800">Protected Event Access</h2>
        <p className="text-xs text-slate-500 mt-1 mb-4">
          This event requires an access passcode provided by the organizer.
        </p>

        {passcodeError && (
          <p className="text-xs text-rose-600 bg-rose-50 p-2 rounded-lg mb-3">{passcodeError}</p>
        )}

        <form
          onSubmit={(e) => {
            e.preventDefault();
            loadEvent(passcode);
          }}
          className="space-y-3"
        >
          <input
            type="password"
            placeholder="Enter Event Passcode"
            value={passcode}
            onChange={(e) => setPasscode(e.target.value)}
            className="w-full text-sm p-3 border border-slate-300 rounded-xl text-center tracking-widest focus:ring-2 focus:ring-sky-500 focus:outline-none"
          />
          <button
            type="submit"
            className="w-full py-2.5 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-xs rounded-xl shadow transition"
          >
            Unlock & Continue
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
      {/* Back button and event header */}
      <div className="mb-6 flex items-center justify-between">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Events
        </Link>
        <div className="flex items-center gap-2 text-xs font-medium text-slate-500">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          Isolated Event Index: <span className="font-mono text-slate-800">{eventId.slice(0, 8)}...</span>
        </div>
      </div>

      <div className="text-center max-w-xl mx-auto mb-8">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">{eventData?.name}</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          {eventData?.description || "Organized with FindZora AI face discovery"}
        </p>
      </div>

      {/* Informed Consent Modal */}
      <ConsentModal
        isOpen={showConsentModal}
        eventName={eventData?.name || "Selected Event"}
        onConsentGiven={handleConsentGiven}
        onCancel={() => setShowConsentModal(false)}
      />

      {/* Camera Capture Section */}
      {hasConsented ? (
        <div className="space-y-6">
          <CameraCapture onCapture={handleSelfieSearch} isSearching={isSearching} />

          {searchError && (
            <div className="max-w-xl mx-auto p-4 bg-rose-50 border border-rose-200 rounded-2xl flex items-start gap-3 text-xs text-rose-800">
              <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
              <div>
                <p className="font-bold">Search Notice:</p>
                <p className="mt-0.5">{searchError}</p>
              </div>
            </div>
          )}

          {/* Search Result Gallery */}
          {searchResult && (
            <CandidateGallery
              candidates={searchResult.candidates || []}
              eventId={eventId}
              eventName={eventData?.name || "Event"}
            />
          )}
        </div>
      ) : (
        <div className="text-center p-10 bg-white rounded-2xl border border-slate-200 max-w-md mx-auto shadow-sm">
          <ShieldCheck className="w-12 h-12 text-sky-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-800">Consent Required</h3>
          <p className="text-xs text-slate-500 mt-1 mb-4">
            Under privacy guidelines, attendee search requires reviewing our biometric processing notice.
          </p>
          <button
            onClick={() => setShowConsentModal(true)}
            className="px-5 py-2.5 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-xs rounded-xl shadow transition"
          >
            Review Consent Terms
          </button>
        </div>
      )}
    </div>
  );
}
