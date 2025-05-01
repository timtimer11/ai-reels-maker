'use client';

import { useState } from "react"; // Импортируем хук для управления состоянием
import { useRouter } from 'next/navigation'; // Импорт роутера для навигации между страницами
import { useVideoContext } from '../context/VideoContext';

export default function VideoSettings() {
  const { videoSettings, updateVideoSettings } = useVideoContext();
  // Инициализация состояний компонента
  const [selectedVoice, setSelectedVoice] = useState('voice1'); // Состояние для выбранного голоса
  const [selectedVideo, setSelectedVideo] = useState('video1'); // Состояние для выбранного стиля видео
  const [addCaptions, setAddCaptions] = useState(false); // Состояние для включения/выключения субтитров
  
  const router = useRouter(); // Инициализация роутера

  // Функция для перехода на следующую страницу
  const generateVideo = () => {
    updateVideoSettings({
      voice: selectedVoice,
      video: selectedVideo,
      captions: addCaptions,
      script: videoSettings.script  // Preserve the script when updating settings
    });
    
  };

  return (
    // Основной контейнер страницы с центрированием содержимого
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      {/* Show the script at the top */}
      <div className="mb-8 max-w-2xl">
        <h2 className="text-xl font-bold mb-2">Generated Script:</h2>
        <p className="text-gray-700">{videoSettings.script}</p>
      </div>

      {/* Секция выбора голоса (вертикальное расположение) */}
      <div className="flex flex-col gap-4 mb-8">
        <h2 className="text-xl font-bold mb-4">Select Voice</h2>
        {/* Радио-кнопки для выбора голоса */}
        <div className="flex items-center gap-2">
          <input
            type="radio"
            id="voice1"
            name="voice" // name группирует радио-кнопки
            value="voice1"
            checked={selectedVoice === 'voice1'}
            onChange={(e) => setSelectedVoice(e.target.value)}
            className="w-4 h-4"
          />
          <label htmlFor="voice1">Voice 1</label>
        </div>
        {/* Аналогичные радио-кнопки для остальных голосов */}
        <div className="flex items-center gap-2">
          <input
            type="radio"
            id="voice2"
            name="voice"
            value="voice2"
            checked={selectedVoice === 'voice2'}
            onChange={(e) => setSelectedVoice(e.target.value)}
            className="w-4 h-4"
          />
          <label htmlFor="voice2">Voice 2</label>
        </div>
        <div className="flex items-center gap-2">
          <input
            type="radio"
            id="voice3"
            name="voice"
            value="voice3"
            checked={selectedVoice === 'voice3'}
            onChange={(e) => setSelectedVoice(e.target.value)}
            className="w-4 h-4"
          />
          <label htmlFor="voice3">Voice 3</label>
        </div>
      </div>

      {/* Секция выбора стиля видео (горизонтальное расположение) */}
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">Select Video Style</h2>
        <div className="flex gap-8">
          {/* Радио-кнопки для выбора стиля видео */}
          <div className="flex flex-col items-center">
            <label htmlFor="video1">Video 1</label>
            <input
              type="radio"
              id="video1"
              name="video"
              value="video1"
              checked={selectedVideo === 'video1'}
              onChange={(e) => setSelectedVideo(e.target.value)}
              className="mt-2 w-4 h-4"
            />
          </div>
          {/* Аналогичные радио-кнопки для остальных стилей */}
          <div className="flex flex-col items-center">
            <label htmlFor="video2">Video 2</label>
            <input
              type="radio"
              id="video2"
              name="video"
              value="video2"
              checked={selectedVideo === 'video2'}
              onChange={(e) => setSelectedVideo(e.target.value)}
              className="mt-2 w-4 h-4"
            />
          </div>
          <div className="flex flex-col items-center">
            <label htmlFor="video3">Video 3</label>
            <input
              type="radio"
              id="video3"
              name="video"
              value="video3"
              checked={selectedVideo === 'video3'}
              onChange={(e) => setSelectedVideo(e.target.value)}
              className="mt-2 w-4 h-4"
            />
          </div>
        </div>
      </div>

      {/* Чекбокс для включения/выключения субтитров */}
      <div className="flex items-center gap-2 mb-8">
        <input
          type="checkbox"
          id="captions"
          checked={addCaptions}
          onChange={(e) => setAddCaptions(e.target.checked)}
          className="w-4 h-4"
        />
        <label htmlFor="captions">Add captions?</label>
      </div>

      {/* Кнопка для перехода на следующую страницу */}
      <button 
        onClick={generateVideo}
        className="mt-4 px-4 py-2 bg-green-500 text-white rounded"
      >
        Generate
      </button>
    </main>
  );
}
