'use client';

import { Button } from "@/components/ui/button";
import { Linkedin, Mail, Coffee, Code } from "lucide-react";

export default function Contact() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-purple-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden px-4 py-20 lg:py-32">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-600/10 via-blue-600/5 to-indigo-600/10"></div>
        <div className="relative mx-auto max-w-4xl text-center">
          <h2 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl lg:text-6xl mb-6">
            Some
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent"> Context</span>
          </h2>
          
          <div className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            <p className="mb-4">
                Lately, I&apos;ve been seeing a ton of brain-rot videos everywhere. You know, those mindless reels that somehow monetize.
            </p>

            <p className="mb-4">
                So naturally, I thought, what if I built a pipeline that produces and posts these videos 24/7 while I&apos;m sleeping and making a &quot;bank&quot;?
            </p>

            <p className="mb-4">
                However, I&apos;ve changed my mind once I had to dive into TikTok, Instagram, and YouTube API docs, cause I ain&apos;t got time to read all of that.
            </p>

            <p className="mb-4">
                Instead, I just slapped together this app where you drop a Reddit post link and it spits out a video.
            </p>

            <p className="mb-4">
            To make things worse, I put $5 into my OpenAI account (Sam Altman can thank me later). Technically, that makes me an investor too.
            </p>

            <p className="mb-4">
             If you have read this far, you may want to check out my LinkedIn too.
            </p>
            </div>
          <div className="flex justify-center gap-4 mb-16">
            <a 
              href="https://www.linkedin.com/in/timur-kulbuzhev/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              <Linkedin className="h-5 w-5" />
              Let&apos;s connect on LinkedIn
            </a>
          </div>
        </div>
      </section>
    </main>
  );
} 