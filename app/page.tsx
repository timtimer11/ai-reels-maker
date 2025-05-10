'use client';

import { useState, useEffect, useCallback } from "react";

export default function Home() {
  const [taskId, setTaskId] = useState("");
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [pollCount, setPollCount] = useState(0);
  const [redditUrl, setRedditUrl] = useState("");

  const startProcessing = async () => {
    try {
      setIsLoading(true);
      setStatus("");
      setError("");
      setPollCount(0);

      const response = await fetch("/api/py/reddit/reddit-commentary?url=" + encodeURIComponent(redditUrl), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) throw new Error("Failed to start task");

      const data = await response.json();
      setTaskId(data.task_id);
      setStatus("PROCESSING");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const checkTaskStatus = useCallback(async () => {
    if (!taskId || status !== "PROCESSING") return;

    try {
      const response = await fetch(`/api/py/reddit/reddit-commentary/status/${taskId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      
      setStatus(data.status);
      if (data.error) setError(data.error);
      
      if (data.status === "COMPLETED" || data.status === "FAILED") {
        setIsLoading(false);
      }
    } catch (err: any) {
      console.error('Error checking task status:', err);
      setPollCount(prev => prev + 1);
    }
  }, [taskId, status]);

  useEffect(() => {
    if (status !== "PROCESSING" || !taskId) return;

    const pollInterval = setInterval(checkTaskStatus, 2000);
    
    return () => {
      clearInterval(pollInterval);
    };
  }, [status, taskId, checkTaskStatus, pollCount]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md mb-4">
        <input
          type="text"
          value={redditUrl}
          onChange={(e) => setRedditUrl(e.target.value)}
          placeholder="Enter Reddit post URL"
          className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
        />
      </div>
      <button 
        onClick={startProcessing} 
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400 mb-4"
        disabled={isLoading || status === "PROCESSING" || !redditUrl}
      >
        {isLoading ? "Starting..." : status === "PROCESSING" ? "Processing..." : "Generate Video"}
      </button>

      {status && <p className={`text-${status === "COMPLETED" ? "green" : "blue"}-500`}>{status}</p>}
      {error && <p className="text-red-500 mt-4">Error: {error}</p>}
    </main>
  );
}
