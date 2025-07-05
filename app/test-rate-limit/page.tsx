'use client';

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/loadingSpinner";

export default function TestRateLimit() {
  const [clickCount, setClickCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const testRateLimit = async () => {
    try {
      setIsLoading(true);
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_HOST;
      const response = await fetch(`${backendUrl}/api/py/reddit/test-rate-limit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setClickCount(data.click_count);
      console.log(`Button clicked! Count: ${data.click_count}`);
    } catch (err: any) {
      console.error('Error testing rate limit:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-8">Rate Limit Test</h1>
        <div className="text-2xl font-bold text-purple-600 mb-8">
          Count: {clickCount}
        </div>
        <Button 
          onClick={testRateLimit}
          disabled={isLoading}
          className="bg-purple-600 hover:bg-purple-700 text-white font-medium py-3 px-8 rounded-lg transition-colors"
        >
          {isLoading ? (
            <div className="flex items-center gap-2">
              <Spinner size="small" show />
              Testing...
            </div>
          ) : (
            'Test Rate Limit'
          )}
        </Button>
      </div>
    </main>
  );
}
