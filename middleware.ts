import { ClerkMiddlewareAuth, clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";
import { NextRequest, NextResponse } from "next/server";

const isProtectedRoute = createRouteMatcher(['/generate-video(.*)','/completed-generation(.*)'])

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

const ratelimit = new Ratelimit({
    redis: redis,
    limiter: Ratelimit.slidingWindow(1, "86400 s"),
    ephemeralCache: new Map(),
    analytics: true,
  });

const isAPI = (path: string) => {
  return path.includes("/api/py/reddit/reddit-commentary")
      || path.includes("/api/py/reddit/test-rate-limit");
}

// export default clerkMiddleware(async (auth: ClerkMiddlewareAuth, request: NextRequest) => {
//     if (isAPI(request.nextUrl.pathname)) {
//         const {userId} = await auth();
//         const { success, limit, reset, remaining } = await ratelimit.limit(`${userId}`);

//         const res = success ? NextResponse.next() : NextResponse.json({ errorMessage: "Rate limit exceeded" }, { status: 429 });

//         res.headers.set("X-RateLimit-Limit", limit.toString());
//         res.headers.set("X-RateLimit-Remaining", remaining.toString());
//         res.headers.set("X-RateLimit-Reset", reset.toString());


//         if (!success) return res;
//         return res;
//     }
//     if (isProtectedRoute(request)) await auth.protect()
//     return NextResponse.next();
// });

export default clerkMiddleware(async (auth, req) => {
  if (isAPI(req.nextUrl.pathname)) {
    const { userId } = await auth();
    let meta: any;
    let success = false;
    try {
      const result = await ratelimit.limit(userId!);
      success = result.success;
      meta = result;
    } catch (e) {
      console.error("Upstash limit() threw error:", e);
      // Fail‐open: still allow the request
      success = true;
      meta = { limit: "?", remaining: "?", reset: "?" };
    }

    console.log("Rate limit check:", { userId, ...meta });

    const res = success
      ? NextResponse.next()
      : NextResponse.json({ errorMessage: "Rate limit exceeded" }, { status: 429 });

    res.headers.set("X-RateLimit-Limit", String(meta.limit));
    res.headers.set("X-RateLimit-Remaining", String(meta.remaining));
    res.headers.set("X-RateLimit-Reset", String(meta.reset));

    return res;
  }

  if (isProtectedRoute(req)) await auth.protect();
  return NextResponse.next();
});


export const config = {
    matcher: [
      // Skip Next.js internals and all static files, unless found in search params
      '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
      // Always run for API routes
      '/(api|trpc)(.*)',
    ],
  };