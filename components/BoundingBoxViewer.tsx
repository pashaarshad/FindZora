"use client";

import { useEffect, useRef, useState } from "react";
import { Scan, ShieldAlert, Check } from "lucide-react";

interface FaceBox {
  id: string;
  bbox: [number, number, number, number]; // [x, y, w, h]
  quality_score: number;
  blur_score: number;
  model_version: string;
}

interface BoundingBoxViewerProps {
  photoId: string;
  filename: string;
  streamUrl: string;
}

export default function BoundingBoxViewer({ photoId, filename, streamUrl }: BoundingBoxViewerProps) {
  const [faces, setFaces] = useState<FaceBox[]>([]);
  const [loading, setLoading] = useState(true);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const imgRef = useRef<HTMLImageElement | null>(null);
  const [hoveredFace, setHoveredFace] = useState<FaceBox | null>(null);

  useEffect(() => {
    fetchFaces();
  }, [photoId]);

  const fetchFaces = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/photos/${photoId}/faces`);
      if (res.ok) {
        const data = await res.json();
        setFaces(data.faces || []);
      }
    } catch (e) {
      console.error("Failed to load face bounding boxes:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 rounded-2xl p-4 text-white flex flex-col gap-3">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <Scan className="w-5 h-5 text-emerald-400" />
          <h4 className="text-sm font-semibold">{filename}</h4>
        </div>
        <span className="text-xs bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-0.5 rounded-full font-mono">
          {faces.length} detected face{faces.length === 1 ? "" : "s"}
        </span>
      </div>

      <div ref={containerRef} className="relative mx-auto max-w-full overflow-hidden rounded-xl border border-slate-800 bg-black flex items-center justify-center">
        <img
          ref={imgRef}
          src={streamUrl}
          alt={filename}
          className="max-h-[500px] w-auto object-contain block"
          onLoad={() => {
            // Force re-render for coordinate alignment
            setFaces((prev) => [...prev]);
          }}
        />

        {/* Render Bounding Box Overlays */}
        {imgRef.current &&
          faces.map((f, idx) => {
            const img = imgRef.current!;
            const naturalW = img.naturalWidth || 1;
            const naturalH = img.naturalHeight || 1;
            const displayW = img.clientWidth;
            const displayH = img.clientHeight;

            const scaleX = displayW / naturalW;
            const scaleY = displayH / naturalH;

            const [bx, by, bw, bh] = f.bbox;
            const left = bx * scaleX;
            const top = by * scaleY;
            const width = bw * scaleX;
            const height = bh * scaleY;

            return (
              <div
                key={f.id}
                onMouseEnter={() => setHoveredFace(f)}
                onMouseLeave={() => setHoveredFace(null)}
                style={{
                  position: "absolute",
                  left: `${left}px`,
                  top: `${top}px`,
                  width: `${width}px`,
                  height: `${height}px`,
                }}
                className="border-2 border-emerald-400 bg-emerald-400/10 cursor-pointer transition-all hover:border-emerald-300 hover:bg-emerald-400/25 group"
              >
                <div className="absolute -top-6 left-0 bg-emerald-500 text-slate-950 font-mono text-[10px] font-bold px-1.5 py-0.5 rounded whitespace-nowrap shadow">
                  Face #{idx + 1} • Q: {f.quality_score}
                </div>
              </div>
            );
          })}
      </div>

      {hoveredFace ? (
        <div className="bg-slate-800/80 p-2.5 rounded-xl text-xs flex items-center justify-between border border-slate-700">
          <div>
            <span className="font-semibold text-emerald-400">Selected Face Inspection:</span>
            <span className="ml-2 text-slate-300">
              Quality Score: {hoveredFace.quality_score} • Blur Score: {hoveredFace.blur_score.toFixed(1)}
            </span>
          </div>
          <span className="text-[10px] font-mono text-slate-400">{hoveredFace.model_version}</span>
        </div>
      ) : (
        <p className="text-[11px] text-slate-400 text-center">
          Hover over detected green face boxes to inspect quality and sharpness scores.
        </p>
      )}
    </div>
  );
}
