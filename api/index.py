import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import router

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")
frontend_host_url = os.getenv("FRONTEND_HOST_URL")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        frontend_host_url
    ],
    allow_credentials=True, # Allows cookies and authentication
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all HTTP headers
)

app.include_router(router.router, prefix="/api/py/reddit")

