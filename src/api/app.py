"""FastAPI application for Medical AI Service."""

from fastapi import FastAPI

app = FastAPI(
    title="Medical AI Service API",
    description="REST API for symptom analysis and doctor recommendation",
    version="1.0.0"
)