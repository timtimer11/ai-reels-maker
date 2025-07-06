import { ClerkMiddlewareAuth, clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextRequest, NextResponse } from "next/server";

const isProtectedRoute = createRouteMatcher(['/generate-video(.*)','/completed-generation(.*)'])

export default clerkMiddleware(async (auth: ClerkMiddlewareAuth, request: NextRequest) => {
  if (isProtectedRoute(request)) await auth.protect()
  return NextResponse.next();
});
