"use client"

import { Button } from "@/components/ui/button"
import Image from "next/image";
import { useRouter } from 'next/navigation';


export default function Home() {
  const router = useRouter();
  return (
    <main className="flex flex-col items-center p-8">
      {/* Hero Section */}
      <div className="mt-12 text-center">
        <div>
          <span>some fancy text about </span>
          <span className="font-bold">CHANGING THE GAME</span>
        </div>
        <div>
          <span className="italic text-sm">*don&apos;t forget to mention &quot;AI&quot;</span>
        </div>
      </div>

      {/* CTA Button */}
      <div className="my-8">
        <Button variant="outline" onClick={() => router.push('/generate-video')}>Generate AI Reels</Button>
      </div>

      {/* Divider */}
      <div className="w-full border-t my-8 max-w-xl" />

      {/* For Who Section */}
      <div className="text-center mb-4 font-semibold">for Who?</div>
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="border rounded px-6 py-4 text-center">Content Creators</div>
        <div className="border rounded px-6 py-4 text-center">Casual Scrollers</div>
        <div className="border rounded px-6 py-4 text-center">somebody else</div>
      </div>

      {/* Divider */}
      <div className="w-full border-t my-8 max-w-xl" />

      {/* Reviews Section */}
      <div className="text-center font-semibold mb-6 mt-12">Reviews</div>
      <div className="flex flex-col md:flex-row justify-center items-center gap-8 mb-8">
        {/* Customer face */}
        <div className="w-48 h-48 rounded-full border flex items-center justify-center text-center overflow-hidden">
          <Image
            src="/grandpa_coffee.webp"
            alt="happy customer face"
            className="w-full h-full object-cover object-right"
            width={192}
            height={192}
          />
        </div>
        {/* Positive review */}
        <div className="min-h-32 max-w-md w-full rounded-xl border flex items-center justify-center text-left p-4 break-words bg-gray-50">
          <span>
            generate super short positive review about my app<br />
            <br />
            <span>
            ChatGPT said: This app is insanely cool—turns Reddit posts into TikTok-style videos with AI voiceovers and captions, complete with Subway Surfers in the background. Instant viral content!
            </span>
          </span>
        </div>
      </div>

      {/* Divider */}
      <div className="w-full border-t my-8 max-w-xl" />

      {/* Partners Section */}
      <div className="text-center font-semibold mb-2">Partners</div>
      <div className="text-center mb-4">
        signup for free AWS credits and paste their logo here &lt;TODO&gt;
      </div>

      {/* Divider */}
      <div className="w-full border-t my-8 max-w-xl" />

      {/* Pricing Section */}
      <div className="text-center font-semibold mb-4">Pricing Plans</div>
      <div className="flex flex-col md:flex-row justify-center gap-4 mb-8">
        <div className="w-32 h-24 rounded-xl border flex items-center justify-center text-center">
          <span>Broke</span>
        </div>
        <div className="w-32 h-24 rounded-xl border flex items-center justify-center text-center">
          <span>Paycheck-to-Paycheck</span>
        </div>
        <div className="w-32 h-24 rounded-xl border flex items-center justify-center text-center">
          <span>RICH. MILLIONAIRE.</span>
        </div>
      </div>

      {/* Divider */}
      <div className="w-full border-t my-8 max-w-xl" />

      {/* Footer */}
      <div className="w-full flex flex-col md:flex-row justify-between items-center p-8 mt-12">
        <div className="mb-4 md:mb-0">
          <div>another fancy text with</div>
          <div>words like:</div>
          <div className="font-mono">
            &quot;STREAMLINE&quot;, &quot;SCALEABLE&quot;,<br />
            &quot;CONTENT ECOSYSTEM&quot;
          </div>
        </div>
        <div>
          <button className="border rounded px-8 py-2">cta</button>
        </div>
      </div>
    </main>
  );
}