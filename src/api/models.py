"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional


class SymptomRequest(BaseModel):
    """Request model for symptom analysis."""
    text: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Symptom description from user",
        examples=["У меня болит голова и температура"]
    )


class AnalysisResponse(BaseModel):
    """Response model for symptom analysis."""
    response: str = Field(
        ...,
        description="AI-generated response with doctor recommendations"
    )
    language: str = Field(
        ...,
        description="Detected language (ru/en)"
    )
    processing_time: Optional[float] = Field(
        None,
        description="Processing time in seconds"
    )


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(
        ...,
        description="Service status (healthy/unhealthy)"
    )
    service: str = Field(
        ...,
        description="Service name"
    )
    version: str = Field(
        ...,
        description="Service version"
    )
