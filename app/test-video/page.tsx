'use client';

import { useState } from 'react';

export default function TestVideo() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-2xl">
        <h1 className="text-2xl font-bold mb-4">Test Video Display</h1>
        
        {/* Video player */}
        <video 
          className="w-full rounded-lg shadow-lg mb-4"
          controls
          src="/output_video_2074e4cb-dfea-49a6-b2bd-c168f13c90e8.mp4"
        >
          Your browser does not support the video tag.
        </video>

        {/* Download button */}
        <a 
          href="/output_video_2074e4cb-dfea-49a6-b2bd-c168f13c90e8.mp4"
          download
          className="inline-block px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Download Video
        </a>
      </div>
    </main>
  );
} 