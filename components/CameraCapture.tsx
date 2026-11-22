"use client";

import { useRef, useState, useEffect } from "react";
import { Camera, RefreshCw, CheckCircle2, Upload, AlertCircle } from "lucide-react";

interface CameraCaptureProps {
  onCapture: (blob: Blob) => void;
  isSearching: boolean;
}

export default function CameraCapture({ onCapture, isSearching }: CameraCaptureProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [capturedUrl, setCapturedUrl] = useState<string | null>(null);
  const [capturedBlob, setCapturedBlob] = useState<Blob | null>(null);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [facingMode, setFacingMode] = useState<"user" | "environment">("user");

  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
    };
  }, [facingMode]);

  const startCamera = async () => {
    stopCamera();
    setCameraError(null);
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("Webcam access not supported in this browser context.");
      }
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode, width: { ideal: 640 }, height: { ideal: 640 } },
        audio: false,
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err: any) {
      console.warn("Camera init failed:", err);
      setCameraError(err.message || "Unable to access camera. Please allow permissions or upload a selfie file.");
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current || document.createElement("canvas");
    canvas.width = video.videoWidth || 480;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(
      (blob) => {
        if (blob) {
          setCapturedBlob(blob);
          setCapturedUrl(URL.createObjectURL(blob));
        }
      },
      "image/jpeg",
      0.92
    );
  };

  const handleRetake = () => {
    if (capturedUrl) {
      URL.revokeObjectURL(capturedUrl);
    }
    setCapturedBlob(null);
    setCapturedUrl(null);
    startCamera();
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setCapturedBlob(file);
      setCapturedUrl(URL.createObjectURL(file));
      stopCamera();
    }
  };

  const handleSubmit = () => {
    if (capturedBlob) {
      onCapture(capturedBlob);
    }
  };

  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 max-w-xl mx-auto flex flex-col items-center gap-4">
      <div className="w-full flex items-center justify-between">
        <div>
          <h2 className="text-base font-bold text-slate-800 flex items-center gap-2">
            <Camera className="w-5 h-5 text-sky-600" />
            Capture Verification Selfie
          </h2>
          <p className="text-xs text-slate-500">Center your face in good light without sunglasses</p>
        </div>
        {!capturedUrl && !cameraError && (
          <button
            onClick={() => setFacingMode((m) => (m === "user" ? "environment" : "user"))}
            className="p-2 text-slate-500 hover:text-sky-600 rounded-lg border border-slate-200 hover:bg-slate-50 transition"
            title="Switch Camera"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        )}
      </div>

      <div className="relative w-72 h-72 sm:w-80 sm:h-80 rounded-2xl overflow-hidden bg-slate-950 flex items-center justify-center border-4 border-slate-100 shadow-inner">
        {capturedUrl ? (
          <img src={capturedUrl} alt="Captured Selfie" className="w-full h-full object-cover" />
        ) : !cameraError ? (
          <>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover"
            />
            {/* Face framing circle guide */}
            <div className="absolute inset-0 pointer-events-none border-2 border-dashed border-sky-400/70 rounded-full m-8 animate-pulse" />
          </>
        ) : (
          <div className="p-4 text-center text-slate-300 flex flex-col items-center gap-2">
            <AlertCircle className="w-8 h-8 text-amber-400" />
            <p className="text-xs">{cameraError}</p>
            <label className="mt-2 px-3 py-1.5 bg-sky-600 text-white text-xs font-semibold rounded-lg cursor-pointer hover:bg-sky-700 transition flex items-center gap-1.5">
              <Upload className="w-3.5 h-3.5" />
              Upload Image File
              <input type="file" accept="image/*" onChange={handleFileUpload} className="hidden" />
            </label>
          </div>
        )}
      </div>

      <canvas ref={canvasRef} className="hidden" />

      {/* Action Buttons */}
      <div className="flex items-center gap-3 w-full justify-center">
        {capturedUrl ? (
          <>
            <button
              onClick={handleRetake}
              disabled={isSearching}
              className="px-4 py-2 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition flex items-center gap-1.5"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Retake
            </button>
            <button
              onClick={handleSubmit}
              disabled={isSearching}
              className="px-6 py-2 text-xs font-semibold text-white bg-sky-600 hover:bg-sky-700 rounded-xl shadow-md shadow-sky-200 transition flex items-center gap-1.5 disabled:opacity-50"
            >
              {isSearching ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  Searching Index...
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Find My Photos
                </>
              )}
            </button>
          </>
        ) : !cameraError ? (
          <>
            <button
              onClick={capturePhoto}
              className="px-6 py-2.5 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-700 hover:to-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition flex items-center gap-2"
            >
              <Camera className="w-4 h-4" />
              Snap Photo
            </button>
            <label className="px-3 py-2 text-xs text-slate-500 hover:text-slate-800 rounded-xl border border-slate-200 hover:bg-slate-50 cursor-pointer flex items-center gap-1.5 transition">
              <Upload className="w-3.5 h-3.5" />
              Upload file instead
              <input type="file" accept="image/*" onChange={handleFileUpload} className="hidden" />
            </label>
          </>
        ) : null}
      </div>
    </div>
  );
}
