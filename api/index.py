from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import router

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://ai-reels-maker.vercel.app"  # Your Vercel deployment
        "https://ai-reels-maker-production.up.railway.app/" # Railway deployment
    ],
    allow_credentials=True, # Allows cookies and authentication
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all HTTP headers
)

app.include_router(router.router, prefix="/api/py/reddit")

