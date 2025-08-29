"""
ML Core Package for Sentiment Analysis.

This package provides the core machine learning functionality for sentiment
analysis, including the pipeline, models, validation, and configuration.
"""

from .sentiment_pipeline import SentimentClassificationPipeline, analyze_sentiment
from .models import (
    SentimentAnalysis,
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
    ModelVersion,
    PipelineHealth,
    SentimentLabel,
    ModelType
)
from .validators import TextValidator, ValidationError, validate_and_sanitize_text
from .config import (
    SentimentAnalysisConfig,
    ModelConfig,
    PerformanceConfig,
    LoggingConfig,
    ConfigManager,
    get_config,
    get_model_config,
    get_performance_config,
    get_logging_config
)

__version__ = "1.0.0"
__author__ = "Sentiment Analysis Team"

__all__ = [
    # Core pipeline
    "SentimentClassificationPipeline",
    "analyze_sentiment",
    
    # Data models
    "SentimentAnalysis",
    "SentimentAnalysisRequest", 
    "SentimentAnalysisResponse",
    "ModelVersion",
    "PipelineHealth",
    "SentimentLabel",
    "ModelType",
    
    # Validation
    "TextValidator",
    "ValidationError",
    "validate_and_sanitize_text",
    
    # Configuration
    "SentimentAnalysisConfig",
    "ModelConfig",
    "PerformanceConfig", 
    "LoggingConfig",
    "ConfigManager",
    "get_config",
    "get_model_config",
    "get_performance_config",
    "get_logging_config"
]
