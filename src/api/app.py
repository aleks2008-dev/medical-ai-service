"""FastAPI application for Medical AI Service."""

import time
from fastapi import FastAPI, HTTPException

from src.api.models import SymptomRequest, AnalysisResponse, HealthResponse
from src.services.ai_service import AIService
from src import __version__, __description__


app = FastAPI(
    title="Medical AI Service API",
    description="REST API for symptom analysis and doctor recommendation",
    version="1.0.0"
)

ai_service = AIService()


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_symptoms(request: SymptomRequest):
    """Analyze symptoms and get doctor recommendations.
    - **text**: Symptom description (3-1000 characters)
    Return AI-generated response with doctor recommendations."""
    try:
        start_time = time.time()
        response = ai_service.analyze_and_respond(request.text)
        language = ai_service._detect_language(request.text)
        processing_time = round(time.time() - start_time, 2)
        return AnalysisResponse(
            response=response,
            language=language,
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check service health status.
    Return basic service information and status."""
    return HealthResponse(
        status="healthy",
        service=__description__,
        version=__version__
    )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Medical AI Service API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
