'use client';

import { useState } from "react";
import { useRouter } from 'next/navigation'; // Импортируем useRouter для навигации между страницами
import { useVideoContext } from './context/VideoContext';

export default function Home() {
  const { updateVideoSettings } = useVideoContext();
  // Состояния (states) для хранения данных и состояния компонента
  const [script, setScript] = useState(""); // Хранит текст скрипта
  const [error, setError] = useState(""); // Хранит текст ошибки, если она возникла
  const [isLoading, setIsLoading] = useState(false); // Показывает, идёт ли загрузка
  
  const router = useRouter(); // Хук для навигации между страницами

  // Функция для получения скрипта с бэкенда
  const fetchVoiceoverScript = async () => {
    try {
      setIsLoading(true);
      setError("");
      console.log("Starting fetch...");
      
      // Отправляем GET запрос на наш FastAPI бэкенд
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
      
      // Преобразуем ответ в JSON и сохраняем скрипт
      const data = await response.json();
      console.log("Received data:", data);
      
      setScript(data.script || "No script generated.");
      // Save script to context
      updateVideoSettings({
        voice: 'voice1',
        video: 'video1',
        captions: false,
        script: data.script || "No script generated."
      });
    } catch (err) {
      console.error("Full error:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch script");
    } finally {
      setIsLoading(false);
    }
  };

  // Функция для перехода на следующую страницу
  const handleContinue = () => {
    router.push('/video-settings'); // Переход на страницу /next-page
  };

  return (
    // Основной контейнер страницы
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      {/* Кнопка для генерации скрипта */}
      <button 
        onClick={fetchVoiceoverScript} 
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400"
        disabled={isLoading}
      >
        {isLoading ? "Loading..." : "Get Voiceover Script"}
      </button>

      {/* Показываем ошибку, если она есть */}
      {error && <p className="mt-4 text-red-500">{error}</p>}
      
      {/* Показываем скрипт, если он есть */}
      {script && <p className="mt-4">{script}</p>}

      {/* Кнопка для перехода на следующую страницу */}
      {script && (
        <button 
          onClick={handleContinue}
          className="mt-4 px-4 py-2 bg-green-500 text-white rounded"
        >
          Continue
        </button>
      )}
    </main>
  );
}
