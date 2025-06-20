from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .ticketing import router as ticketing_router

app = FastAPI(
    title="Anonymous Ticketing API",
    description="REST API for anonymous support ticket submission and management.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the ticketing endpoints
app.include_router(ticketing_router)

@app.get("/")
def health_check():
    """Check API health."""
    return {"message": "Healthy"}
