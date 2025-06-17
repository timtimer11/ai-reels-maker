import { ClerkMiddlewareAuth, clerkMiddleware } from "@clerk/nextjs/server";
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";
import { NextRequest, NextResponse } from "next/server";

const redis = Redis.fromEnv();

const ratelimit = new Ratelimit({
    redis: redis,
    limiter: Ratelimit.slidingWindow(3, "86400 s"),
    ephemeralCache: new Map(),
    analytics: true,
  });

const isAPI = (path: string) => {
    return path.startsWith("/api/py/reddit/reddit-commentary?url=")
}

export default clerkMiddleware(async (auth: ClerkMiddlewareAuth, request: NextRequest) => {
    if (isAPI(request.nextUrl.pathname)) {
        const {userId} = await auth();
        const { success, limit, reset, remaining } = await ratelimit.limit(`${userId}`);

        const res = success ? NextResponse.next() : NextResponse.json({ errorMessage: "Rate limit exceeded" }, { status: 429 });

        res.headers.set("X-RateLimit-Limit", limit.toString());
        res.headers.set("X-RateLimit-Remaining", remaining.toString());
        res.headers.set("X-RateLimit-Reset", reset.toString());


        if (!success) return res;
        return res;
    }
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