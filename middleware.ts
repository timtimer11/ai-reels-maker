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
  return path.includes("/api/py/reddit/reddit-commentary");
};

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
export default clerkMiddleware(async (auth: ClerkMiddlewareAuth, request: NextRequest) => {
  console.log('Middleware triggered for path:', request.nextUrl.pathname);
  
  if (isAPI(request.nextUrl.pathname)) {
      console.log('API route detected');
      const {userId} = await auth();
      console.log('User ID:', userId);
      
      const { success, limit, reset, remaining } = await ratelimit.limit(`${userId}`);
      console.log('Rate limit result:', { success, limit, reset, remaining });

      const res = success ? NextResponse.next() : NextResponse.json({ errorMessage: "Rate limit exceeded" }, { status: 429 });

      res.headers.set("X-RateLimit-Limit", limit.toString());
      res.headers.set("X-RateLimit-Remaining", remaining.toString());
      res.headers.set("X-RateLimit-Reset", reset.toString());

      if (!success) {
          console.log('Rate limit exceeded for user:', userId);
          return res;
      }
      return res;
  }
  if (isProtectedRoute(request)) await auth.protect()
  return NextResponse.next();
});
