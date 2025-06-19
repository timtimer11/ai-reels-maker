import "./globals.css";
import { Inter } from "next/font/google";
import { ClerkProvider } from '@clerk/nextjs'
import { Navigation } from "@/components/Navigation"
import { type Metadata } from 'next'

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Brain Rot App",
  description: "Generate your brain rot video",
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={inter.className}>
          <Navigation />
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
