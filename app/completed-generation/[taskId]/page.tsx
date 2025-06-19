'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

export default function CompletedGeneration() {
  const params = useParams();
  const taskId = params.taskId as string;
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchVideoUrl = async () => {
      try {
        const response = await fetch(`https://ai-reels-maker.vercel.app/api/py/reddit/reddit-commentary/status/${taskId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch video URL');
        }
        const data = await response.json();
        if (data.video_url) {
          setVideoUrl(data.video_url);
        } else {
          setError('No video URL found');
        }
      } catch (err: any) {
        setError(err.message);
      }
    };

    fetchVideoUrl();
  }, [taskId]);

  if (error) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <div className="text-red-500">{error}</div>
      </main>
    );
  }

  if (!videoUrl) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <div className="text-blue-500">Loading...</div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-2xl">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl lg:text-4xl mb-6 text-center">
          <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">Your video is ready!</span>
        </h1>

        {/* Video player */}
        <div className="mb-8">
          <video 
            src={videoUrl}
            controls
            className="w-full rounded-lg shadow-lg"
            style={{ maxHeight: '500px' }}
            preload="metadata"
          >
            Your browser does not support the video tag.
          </video>
        </div>

        {/* Download button */}
        <div className="text-center">
          <a 
            href={videoUrl}
            download
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-8 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 inline-block"
          >
            Download Video
          </a>
        </div>
      </div>
    </main>
  );
} 