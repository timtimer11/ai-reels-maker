'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Video from 'next-video';

export default function CompletedGeneration() {
  const params = useParams();
  const taskId = params.taskId as string;
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchVideoUrl = async () => {
      try {
        const response = await fetch(`/api/py/reddit/reddit-commentary/status/${taskId}`);
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
        <h1 className="text-2xl font-bold mb-8 text-center">Your Video is Ready!</h1>
        
        {/* Video URL display */}
        <div className="mb-4 p-4 bg-gray-100 rounded">
          <p className="text-sm text-gray-600">Video URL:</p>
          <p className="break-all">{videoUrl}</p>
        </div>

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
            className="inline-block px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Download Video
          </a>
        </div>
      </div>
    </main>
  );
} 