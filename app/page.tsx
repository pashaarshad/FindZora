"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  Search,
  Calendar,
  Image as ImageIcon,
  Users,
  Shield,
  ArrowRight,
  FolderSync,
  Camera,
  Layers,
  CheckCircle2,
  AlertCircle
} from "lucide-react";
import CameraCapture from "@/components/CameraCapture";
import ConsentModal from "@/components/ConsentModal";
import MultiEventGallery, { GroupedEvent } from "@/components/MultiEventGallery";
import WorkflowInfographic from "@/components/WorkflowInfographic";

interface EventItem {
  id: string;
  name: string;
  description: string;
  organizer_name: string;
  organizer_email: string;
  has_passcode: boolean;
  retention_days: number;
  created_at: string;
  total_photos: number;
  indexed_photos: number;
}

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<"universal" | "events" | "workflow">("universal");
  const [events, setEvents] = useState<EventItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  // Universal Search State
  const [hasConsented, setHasConsented] = useState(false);
  const [showConsentModal, setShowConsentModal] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [universalResults, setUniversalResults] = useState<{
    grouped_events: GroupedEvent[];
    total_photos_matched: number;
  } | null>(null);
  const [searchError, setSearchError] = useState<string | null>(null);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const res = await fetch("/api/events");
      if (res.ok) {
        const data = await res.json();
        setEvents(data);
      }
    } catch (err) {
      console.error("Failed to load events:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUniversalSearch = async (selfieBlob: Blob) => {
    setIsSearching(true);
    setSearchError(null);
    setUniversalResults(null);

    const formData = new FormData();
    formData.append("selfie", selfieBlob, "universal_query.jpg");
    formData.append("threshold", "0.50");

    try {
      const res = await fetch("/api/search/universal", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Search failed");
      }
      setUniversalResults(data);
    } catch (err: any) {
      console.error("Universal search error:", err);
      setSearchError(err.message || "Failed to search across events.");
    } finally {
      setIsSearching(false);
    }
  };

  const filteredEvents = events.filter((e) =>
    e.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    e.organizer_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8">
      {/* Hero Header */}
      <div className="text-center max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-100/80 text-sky-800 text-xs font-semibold mb-4 border border-sky-200">
          <Sparkles className="w-3.5 h-3.5 text-sky-600" />
          AI Biometric Facial Recognition & Event Photo Discovery
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
          Find all your photos across events in <span className="bg-gradient-to-r from-sky-600 to-indigo-600 bg-clip-text text-transparent">FindZora</span>
        </h1>
        <p className="mt-3 text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Precomputed 512-D embeddings and facial landmark points allow instant discovery. Snap a selfie once and get all your photos grouped by event with one-click batch downloads.
        </p>

        {/* Tab Navigation */}
        <div className="inline-flex items-center gap-2 p-1.5 bg-slate-100 rounded-2xl border border-slate-200 mt-6 shadow-inner">
          <button
            onClick={() => setActiveTab("universal")}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "universal"
                ? "bg-white text-sky-700 shadow-sm"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <Camera className="w-3.5 h-3.5" />
            Universal Photo Search
          </button>
          <button
            onClick={() => setActiveTab("events")}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "events"
                ? "bg-white text-sky-700 shadow-sm"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <Calendar className="w-3.5 h-3.5" />
            Browse Specific Events ({events.length})
          </button>
          <button
            onClick={() => setActiveTab("workflow")}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "workflow"
                ? "bg-white text-sky-700 shadow-sm"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            A-to-Z Workflow Guide
          </button>
        </div>
      </div>

      {/* Tab 1: Universal Multi-Event Attendee Search */}
      {activeTab === "universal" && (
        <div className="space-y-6">
          {/* Informed Consent Modal */}
          <ConsentModal
            isOpen={showConsentModal}
            eventName="All Attended Events (Universal Discovery)"
            onConsentGiven={() => {
              setHasConsented(true);
              setShowConsentModal(false);
            }}
            onCancel={() => setShowConsentModal(false)}
          />

          {!hasConsented ? (
            <div className="bg-white rounded-3xl p-8 max-w-xl mx-auto border border-slate-200 shadow-sm text-center space-y-4">
              <div className="w-14 h-14 bg-sky-100 text-sky-600 rounded-2xl flex items-center justify-center mx-auto shadow-inner">
                <Shield className="w-7 h-7" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900">Universal Multi-Event Attendee Search</h3>
                <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                  Snap one verification selfie to discover all your photographs across weddings, college functions, and gatherings. Ephemeral biometric processing deletes your selfie immediately.
                </p>
              </div>

              <button
                onClick={() => setShowConsentModal(true)}
                className="px-6 py-3 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-700 hover:to-indigo-700 text-white font-semibold text-xs rounded-xl shadow-md shadow-sky-200 transition"
              >
                Review Consent & Start Camera
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              <CameraCapture onCapture={handleUniversalSearch} isSearching={isSearching} />

              {searchError && (
                <div className="max-w-xl mx-auto p-4 bg-rose-50 border border-rose-200 rounded-2xl flex items-center gap-2 text-xs text-rose-800">
                  <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
                  <span>{searchError}</span>
                </div>
              )}

              {/* Grouped Results Gallery */}
              {universalResults && (
                <MultiEventGallery
                  groupedEvents={universalResults.grouped_events || []}
                  totalPhotos={universalResults.total_photos_matched || 0}
                />
              )}
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Single Event Browser */}
      {activeTab === "events" && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search events or organizers..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-4 py-2 text-sm border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>
            <Link
              href="/organizer"
              className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-xl shadow transition flex items-center gap-2"
            >
              <FolderSync className="w-4 h-4" /> Organizer & Watch Folder Portal
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredEvents.map((evt) => (
              <div
                key={evt.id}
                className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <h3 className="font-bold text-slate-900 text-base line-clamp-1">{evt.name}</h3>
                    {evt.has_passcode && (
                      <span className="text-[10px] font-semibold bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded-full flex items-center gap-1">
                        <Shield className="w-3 h-3" /> Protected
                      </span>
                    )}
                  </div>

                  <p className="text-xs text-slate-500 line-clamp-2 mb-4">
                    {evt.description || "Event photos indexed in FindZora"}
                  </p>

                  <div className="grid grid-cols-2 gap-2 p-3 bg-slate-50 rounded-xl text-xs text-slate-600 mb-4">
                    <div className="flex items-center gap-1.5">
                      <ImageIcon className="w-3.5 h-3.5 text-sky-600" />
                      <span>{evt.total_photos} Photos</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Users className="w-3.5 h-3.5 text-indigo-600" />
                      <span>{evt.indexed_photos} Indexed</span>
                    </div>
                  </div>
                </div>

                <Link
                  href={`/search/${evt.id}`}
                  className="w-full py-2.5 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-xs rounded-xl shadow-sm transition flex items-center justify-center gap-2"
                >
                  <span>Search This Event Only</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Complete A-to-Z Workflow Infographic */}
      {activeTab === "workflow" && (
        <WorkflowInfographic />
      )}
    </div>
  );
}
