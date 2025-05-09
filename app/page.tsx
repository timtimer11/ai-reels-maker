'use client';

import { useState } from "react";

export default function Home() {
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const fetchVoiceoverScript = async () => {
    try {
      console.log("Fetching voiceover script...");
      setIsLoading(true);
      setError("");
      setSuccess(false);

      const response = await fetch("/api/py/reddit/reddit-commentary?url=https://www.reddit.com/r/YouShouldKnow/comments/1jvnvvg/ysk_that_your_alarm_ringtone_might_be_doing_more/", {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();

      if (result === true) {
        setSuccess(true);
      } else {
        throw new Error("Operation failed");
      }
    } catch (err) {
      console.error("Error:", err);
      setError(err instanceof Error ? err.message : "Unknown error");
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
        {isLoading ? "Processing..." : "Generate"}
      </button>

      {success && <p className="mt-4 text-green-500">Success!</p>}
      {error && <p className="mt-4 text-red-500">Failed: {error}</p>}
    </main>
  );
}
