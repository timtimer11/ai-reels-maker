'use client';

import { useState, useEffect, useCallback } from "react";
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  const [taskId, setTaskId] = useState("");
  const [status, setStatus] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [pollCount, setPollCount] = useState(0);
  const [redditUrl, setRedditUrl] = useState("");

  const startProcessing = async () => {
    try {
      setIsLoading(true);
      setStatus("");
      setMessage("");
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
      setStatus("processing");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const checkTaskStatus = useCallback(async () => {
    if (!taskId || status !== "processing") return;

    try {
      console.log('Checking status for task:', taskId);
      const response = await fetch(`/api/py/reddit/reddit-commentary/status/${taskId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Raw task status response:', data);
      console.log('Current status:', status);
      console.log('New status from API:', data.status);
      
      setStatus(data.status);
      setMessage(data.message || "");
      if (data.error) setError(data.error);
      
      if (data.status === "completed") {
        console.log('Task completed, redirecting to:', `/completed-generation/${taskId}`);
        setIsLoading(false);
        router.push(`/completed-generation/${taskId}`);
      } else if (data.status === "failed") {
        console.log('Task failed:', data.error);
        setIsLoading(false);
      }
    } catch (err: any) {
      console.error('Error checking task status:', err);
      setPollCount(prev => prev + 1);
    }
  }, [taskId, status, router]);

  useEffect(() => {
    if (status !== "processing" || !taskId) return;

    const pollInterval = setInterval(checkTaskStatus, 2000);
    
    return () => {
      clearInterval(pollInterval);
    };
  }, [status, taskId, checkTaskStatus, pollCount]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-2xl">
        {/* Input field for Reddit URL */}
        <div className="w-full mb-4">
          <input
            type="text"
            value={redditUrl}
            onChange={(e) => setRedditUrl(e.target.value)}
            placeholder="Enter Reddit post URL"
            className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Generate button */}
        <button 
          onClick={startProcessing} 
          className="w-full px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400 mb-4"
          disabled={isLoading || status === "processing" || !redditUrl}
        >
          {isLoading ? "Starting..." : status === "processing" ? "Processing..." : "Generate Video"}
        </button>

        {/* Status and error messages */}
        {status && (
          <div className="mb-4">
            <p className={`text-${status === "completed" ? "green" : "blue"}-500`}>
              Status: {status}
            </p>
            {message && (
              <p className="text-gray-600 text-sm mt-1">
                {message}
              </p>
            )}
          </div>
        )}
        {error && <p className="text-red-500 mb-4">Error: {error}</p>}
      </div>
    </main>
  );
}
