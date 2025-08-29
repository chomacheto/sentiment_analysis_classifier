"""
Data models for sentiment analysis pipeline.

This module defines the core data structures used throughout the sentiment
analysis system, including input validation and output formatting.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum

class SentimentLabel(str, Enum):
    """Enumeration of possible sentiment labels."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class ModelType(str, Enum):
    """Enumeration of supported model types."""
    BERT = "BERT"
    DISTILBERT = "DistilBERT"
    ROBERTA = "RoBERTa"

class SentimentAnalysis(BaseModel):
    """
    Core sentiment analysis result model.
    
    Attributes:
        sentiment_label: Predicted sentiment (positive/negative/neutral)
        confidence_score: Confidence score from 0.0000 to 1.0000
        processing_time_ms: Processing time in milliseconds
        input_text: Original input text (optional, for reference)
        input_text_length: Length of input text
        model_confidence: Raw model confidence scores
        timestamp: When the analysis was performed
    """
    
    sentiment_label: SentimentLabel = Field(..., description="Predicted sentiment label")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    processing_time_ms: float = Field(..., ge=0.0, description="Processing time in milliseconds")
    input_text: Optional[str] = Field(None, description="Original input text")
    input_text_length: int = Field(..., ge=0, description="Length of input text")
    model_confidence: List[Dict[str, Any]] = Field(default_factory=list, description="Raw model confidence scores")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    
    @validator('confidence_score')
    def validate_confidence_score(cls, v):
        """Ensure confidence score is properly formatted to 4 decimal places."""
        return round(v, 4)
    
    @validator('processing_time_ms')
    def validate_processing_time(cls, v):
        """Ensure processing time is properly formatted to 2 decimal places."""
        return round(v, 2)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ModelVersion(BaseModel):
    """
    Model metadata and version information.
    
    Attributes:
        huggingface_id: Hugging Face model identifier
        model_type: Type of model (BERT, DistilBERT, RoBERTa)
        version: Model version string
        description: Human-readable description
        parameters: Number of model parameters
        last_updated: When the model was last updated
        performance_metrics: Dictionary of performance metrics
    """
    
    huggingface_id: str = Field(..., description="Hugging Face model identifier")
    model_type: ModelType = Field(..., description="Type of transformer model")
    version: str = Field(..., description="Model version")
    description: str = Field(..., description="Human-readable description")
    parameters: Optional[int] = Field(None, description="Number of model parameters")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    performance_metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SentimentAnalysisRequest(BaseModel):
    """
    Input request model for sentiment analysis.
    
    Attributes:
        text: Text to analyze for sentiment
        model_name: Optional specific model to use
        include_metadata: Whether to include additional metadata in response
    """
    
    text: str = Field(..., min_length=1, max_length=10000, description="Text to analyze")
    model_name: Optional[str] = Field(None, description="Specific model to use")
    include_metadata: bool = Field(default=False, description="Include additional metadata")
    
    @validator('text')
    def validate_text(cls, v):
        """Ensure text is not empty and properly trimmed."""
        if not v or not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()

class SentimentAnalysisResponse(BaseModel):
    """
    Response model for sentiment analysis API.
    
    Attributes:
        success: Whether the analysis was successful
        data: Sentiment analysis results
        error: Error message if analysis failed
        metadata: Additional metadata about the request/response
    """
    
    success: bool = Field(..., description="Whether the analysis was successful")
    data: Optional[SentimentAnalysis] = Field(None, description="Analysis results")
    error: Optional[str] = Field(None, description="Error message if failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PipelineHealth(BaseModel):
    """
    Pipeline health and status information.
    
    Attributes:
        status: Overall pipeline status
        model_loaded: Whether the model is loaded
        last_activity: Last activity timestamp
        performance_stats: Performance statistics
        error_count: Number of errors encountered
    """
    
    status: str = Field(..., description="Pipeline status (healthy, degraded, error)")
    model_loaded: bool = Field(..., description="Whether the model is loaded")
    last_activity: datetime = Field(..., description="Last activity timestamp")
    performance_stats: Dict[str, Any] = Field(default_factory=dict, description="Performance statistics")
    error_count: int = Field(default=0, ge=0, description="Number of errors encountered")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
