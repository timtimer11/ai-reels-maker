"use client"

import { useRouter } from 'next/navigation';
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import CTA from "@/components/CTA";
import Footer from "@/components/Footer";

export default function Home() {
  const router = useRouter();
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-purple-50">
      <Hero />
      <Features />
      <CTA />
      <Footer />
    </main>
  );
}