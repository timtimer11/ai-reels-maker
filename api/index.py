from fastapi import FastAPI
from .routers import router

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

app.include_router(router.router, prefix="/api/py/reddit")