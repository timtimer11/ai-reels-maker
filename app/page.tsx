'use client';

import { useState } from "react";

export default function Home() {
  const [script, setScript] = useState("");

  const fetchVoiceoverScript = async () => {
    const response = await fetch("/api/py/reddit/reddit-commentary/?url=https://www.reddit.com/r/YouShouldKnow/comments/1jvnvvg/ysk_that_your_alarm_ringtone_might_be_doing_more/");
    const data = await response.json();
    setScript(data.script || "No script generated.");
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <button onClick={fetchVoiceoverScript} className="px-4 py-2 bg-blue-500 text-white rounded">
        Get Voiceover Script
      </button>

      {script && <p className="mt-4">{script}</p>}
    </main>
  );
}
