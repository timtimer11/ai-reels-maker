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
  limiter: Ratelimit.slidingWindow(2, "86400 s"), // 1 request per day
  ephemeralCache: new Map(),
  analytics: true,
});

export async function POST(request: NextRequest) {
  try {
    // Get user authentication
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Apply rate limiting
    const { success, limit, reset, remaining } = await ratelimit.limit(userId);
    
    if (!success) {
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
    const backendUrl = process.env.BACKEND_HOST_URL;
    if (!backendUrl) {
      return NextResponse.json({ error: "Backend URL not configured" }, { status: 500 });
    }

    // Get the request body
    const body = await request.json();
    
    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/api/py/reddit/reddit-commentary`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    // Get the response data
    const data = await response.json();

    // Return the response with rate limit headers
    return NextResponse.json(data, {
      status: response.status,
      headers: {
        "X-RateLimit-Limit": limit.toString(),
        "X-RateLimit-Remaining": remaining.toString(),
        "X-RateLimit-Reset": reset.toString(),
      }
    });

  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
} 