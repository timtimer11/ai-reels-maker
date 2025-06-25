'use client';

import { useState, useEffect, useCallback } from "react";
import { useRouter } from 'next/navigation';
import RedditVideoGenerator from '@/components/RedditVideoGenerator';
import { Spinner } from "@/components/ui/loadingSpinner";
import { Sparkles } from "lucide-react";

export default function Home() {
  const router = useRouter();
  const [taskId, setTaskId] = useState("");
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const onGenerate = async (redditUrl: string) => {
    try {
      setIsLoading(true);
      setStatus("");
      setError("");

      const response = await fetch("https://ai-reels-maker.vercel.app/api/py/reddit/reddit-commentary?url=" + encodeURIComponent(redditUrl), {
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
      console.log(err)
    } finally {
      setIsLoading(false); 
    }
  };

  const checkTaskStatus = useCallback(async () => {
    if (!taskId) return;

    try {
      const response = await fetch(`https://ai-reels-maker.vercel.app/api/py/reddit/reddit-commentary/status/${taskId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setStatus(data.status);
      
      if (data.error && data.status === "failed") {
        setError(data.error);
      }
      
      if (data.status === "completed") {
        router.push(`/completed-generation/${taskId}`);
      } else if (data.status === "failed") {
        // Error message is already set above
      }
    } catch (err: any) {
      console.log(err)
    }
  }, [taskId,router]);

  useEffect(() => {
    if (!taskId || status === "completed" || status === "failed") return;
    
    const pollInterval = setInterval(checkTaskStatus, 2000);
    
    return () => {
      clearInterval(pollInterval);
    };
  }, [status, taskId, checkTaskStatus]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl lg:text-4xl mb-6">
          Add link to Reddit post to
          <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent"> Generate</span>
        </h1>
        <p className="mx-auto max-w-2xl text-lg text-gray-600">
         Pull the text from Reddit post, generate a compelling voiceover with captions, and sync it with high-retention background video - all in one click.
        </p>
      </div>
      <div className="w-full max-w-2xl">
        <RedditVideoGenerator onGenerate={onGenerate} />
        {(isLoading || (status !== "" && status !== "completed" && status !== "failed")) && (
          <div
            className="
              fixed inset-0 z-50
              flex items-center justify-center
              bg-black/40 backdrop-blur-sm
            "
          >
            <div className="flex flex-col items-center gap-4 bg-white p-8 rounded-xl shadow-xl max-w-md w-full mx-4">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-purple-600" />
                <p className="text-sm font-medium text-purple-800">
                  The generation may take up to 30 seconds - depending on the internet speed
                </p>
              </div>
              <div className="flex items-center gap-5">
                {status !== "failed" && <Spinner size="medium" show />}
                <p className={`text-${status === "failed" ? "red" : status === "completed" ? "green" : "blue"}-500 font-medium`}>
                  {status === "failed" ? "Failed - Check error message below" :
                  status === "fetching_reddit_post" ? "Fetching Reddit Post..." :
                  status === "generating_script" ? "Generating Script..." :
                  status === "generating_voiceover" ? "Generating Voiceover..." :
                  status === "fetching_background_video" ? "Fetching Background Video..." :
                  status === "processing_video" ? "Processing Video..." :
                  status === "getting_video_url" ? "Getting Video URL..." :
                  status === "processing" ? "Processing..." :
                  isLoading ? "Starting..." :
                  status}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* INLINE ERROR */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 font-medium">Error occurred:</p>
            <p className="text-red-500 text-sm mt-1">{error}</p>
          </div>
        )}
      </div>
    </main>
  );
}
