'use client';

import { useState } from "react";

export default function Home() {
  const [script, setScript] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const fetchVoiceoverScript = async () => {
    try {
      setIsLoading(true);
      setError("");
      console.log("Starting fetch...");
      
      const response = await fetch("/api/py/reddit/reddit-commentary/?url=https://www.reddit.com/r/YouShouldKnow/comments/1jvnvvg/ysk_that_your_alarm_ringtone_might_be_doing_more/", {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
      
      console.log("Response status:", response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("Received data:", data);
      
      setScript(data.script || "No script generated.");
    } catch (err) {
      console.error("Full error:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch script");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <button 
        onClick={fetchVoiceoverScript} 
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400"
        disabled={isLoading}
      >
        {isLoading ? "Loading..." : "Get Voiceover Script"}
      </button>

      {error && <p className="mt-4 text-red-500">{error}</p>}
      {script && <p className="mt-4">{script}</p>}
    </main>
  );
}
