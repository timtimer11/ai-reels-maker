import { NextRequest, NextResponse } from 'next/server';
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";
import { auth } from "@clerk/nextjs/server";

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

const ratelimit = new Ratelimit({
  redis: redis,
  limiter: Ratelimit.slidingWindow(3, "86400 s"),
  ephemeralCache: new Map(),
  analytics: true,
});

export async function POST(request: NextRequest) {
  try {
    console.log('Proxy request started');
    
    // Get user authentication
    const { userId } = await auth();
    if (!userId) {
      console.log('Unauthorized request');
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    console.log('User authenticated:', userId);

    // Apply rate limiting
    const { success, limit, reset, remaining } = await ratelimit.limit(userId);
    console.log('Rate limit check:', { success, remaining });
    
    if (!success) {
      console.log('Rate limit exceeded');
      return NextResponse.json(
        { errorMessage: "Rate limit exceeded" }, 
        { 
          status: 429,
          headers: {
            "X-RateLimit-Limit": limit.toString(),
            "X-RateLimit-Remaining": remaining.toString(),
            "X-RateLimit-Reset": reset.toString(),
          }
        }
      );
    }

    // Get the backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_HOST;
    if (!backendUrl) {
      console.error('Backend URL not configured');
      return NextResponse.json({ error: "Backend URL not configured" }, { status: 500 });
    }
    console.log('Backend URL:', backendUrl);

    // Get the URL parameter from the request
    const { searchParams } = new URL(request.url);
    const url = searchParams.get('url');
    
    if (!url) {
      console.error('URL parameter missing');
      return NextResponse.json({ error: "URL parameter is required" }, { status: 400 });
    }
    console.log('Reddit URL:', url);

    // Forward the request to the backend
    const backendResponse = await fetch(`${backendUrl}/backend/py/reddit/reddit-commentary?url=${encodeURIComponent(url)}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Backend response status:', backendResponse.status);

    // Get the response data
    const data = await backendResponse.json();
    console.log('Backend response data:', data);

    // Return the response with rate limit headers
    return NextResponse.json(data, {
      status: backendResponse.status,
      headers: {
        "X-RateLimit-Limit": limit.toString(),
        "X-RateLimit-Remaining": remaining.toString(),
        "X-RateLimit-Reset": reset.toString(),
      }
    });

  } catch (error) {
    console.error('Proxy error details:', error);
    return NextResponse.json({ 
      error: "Internal server error", 
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
} 