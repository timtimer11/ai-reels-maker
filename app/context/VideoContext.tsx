'use client';

import { createContext, useContext, useState, ReactNode } from 'react';

type VideoContextType = {
  videoSettings: {
    voice: string;
    video: string;
    captions: boolean;
    script: string;  // Added script field
  };
  updateVideoSettings: (settings: {
    voice: string;
    video: string;
    captions: boolean;
    script: string;  // Added script field
  }) => void;
};

const VideoContext = createContext<VideoContextType | undefined>(undefined);

export function VideoProvider({ children }: { children: ReactNode }) {
  const [videoSettings, setVideoSettings] = useState({
    voice: 'voice1',
    video: 'video1',
    captions: false,
    script: '',  // Initialize script as empty string
  });

  const updateVideoSettings = (settings: {
    voice: string;
    video: string;
    captions: boolean;
    script: string;  // Added script to match the type definition
  }) => {
    setVideoSettings(settings);
  };

  return (
    <VideoContext.Provider value={{ videoSettings, updateVideoSettings }}>
      {children}
    </VideoContext.Provider>
  );
}

export function useVideoContext() {
  const context = useContext(VideoContext);
  if (undefined === context) {
    throw new Error('useVideoContext must be used within a VideoProvider');
  }
  return context;
}