"""
Configuration management for sentiment analysis pipeline.

This module provides centralized configuration management with environment-based
settings, performance tuning, and model configuration options.
"""

import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for ML models."""
    
    default_model: str = field(
        default="distilbert-base-uncased-finetuned-sst-2-english",
        metadata={"description": "Default Hugging Face model for sentiment analysis"}
    )
    
    cache_dir: str = field(
        default="~/.cache/huggingface",
        metadata={"description": "Directory for caching downloaded models"}
    )
    
    max_text_length: int = field(
        default=10000,
        metadata={"description": "Maximum text length for processing"}
    )
    
    batch_size: int = field(
        default=1,
        metadata={"description": "Batch size for inference"}
    )

@dataclass
class PerformanceConfig:
    """Configuration for performance tuning."""
    
    max_processing_time_ms: int = field(
        default=2000,
        metadata={"description": "Maximum processing time in milliseconds"}
    )
    
    enable_caching: bool = field(
        default=True,
        metadata={"description": "Enable model and result caching"}
    )
    
    cache_ttl_seconds: int = field(
        default=3600,
        metadata={"description": "Cache time-to-live in seconds"}
    )
    
    enable_gpu: bool = field(
        default=True,
        metadata={"description": "Enable GPU acceleration if available"}
    )

@dataclass
class LoggingConfig:
    """Configuration for logging and monitoring."""
    
    log_level: str = field(
        default="INFO",
        metadata={"description": "Logging level"}
    )
    
    enable_performance_logging: bool = field(
        default=True,
        metadata={"description": "Enable performance metrics logging"}
    )
    
    enable_validation_logging: bool = field(
        default=True,
        metadata={"description": "Enable validation logging"}
    )

@dataclass
class SentimentAnalysisConfig:
    """Main configuration for sentiment analysis pipeline."""
    
    model: ModelConfig = field(default_factory=ModelConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Sentiment label configuration
    sentiment_labels: Dict[str, str] = field(
        default_factory=lambda: {
            "positive": "positive",
            "negative": "negative",
            "neutral": "neutral"
        },
        metadata={"description": "Mapping of sentiment labels"}
    )
    
    # Confidence thresholds
    high_confidence_threshold: float = field(
        default=0.8,
        metadata={"description": "Threshold for high confidence predictions"}
    )
    
    low_confidence_threshold: float = field(
        default=0.6,
        metadata={"description": "Threshold for low confidence predictions"}
    )

class ConfigManager:
    """Manages configuration loading and access."""
    
    def __init__(self, config: Optional[SentimentAnalysisConfig] = None):
        """
        Initialize configuration manager.
        
        Args:
            config: Optional custom configuration
        """
        self.config = config or self._load_config()
        self._setup_logging()
    
    def _load_config(self) -> SentimentAnalysisConfig:
        """Load configuration from environment variables and defaults."""
        config = SentimentAnalysisConfig()
        
        # Model configuration
        config.model.default_model = os.getenv(
            "SENTIMENT_MODEL_NAME",
            config.model.default_model
        )
        
        config.model.cache_dir = os.getenv(
            "SENTIMENT_CACHE_DIR",
            config.model.cache_dir
        )
        
        cache_dir = os.path.expanduser(config.model.cache_dir)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
            logger.info(f"Created cache directory: {cache_dir}")
        
        # Performance configuration
        config.performance.max_processing_time_ms = int(os.getenv(
            "SENTIMENT_MAX_PROCESSING_TIME_MS",
            config.performance.max_processing_time_ms
        ))
        
        config.performance.enable_caching = os.getenv(
            "SENTIMENT_ENABLE_CACHING",
            str(config.performance.enable_caching)
        ).lower() == "true"
        
        config.performance.enable_gpu = os.getenv(
            "SENTIMENT_ENABLE_GPU",
            str(config.performance.enable_gpu)
        ).lower() == "true"
        
        # Logging configuration
        config.logging.log_level = os.getenv(
            "SENTIMENT_LOG_LEVEL",
            config.logging.log_level
        )
        
        config.logging.enable_performance_logging = os.getenv(
            "SENTIMENT_ENABLE_PERFORMANCE_LOGGING",
            str(config.logging.enable_performance_logging)
        ).lower() == "true"
        
        return config
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_level = getattr(logging, self.config.logging.log_level.upper(), logging.INFO)
        logging.basicConfig(level=log_level)
        
        logger.info(f"Configuration loaded with log level: {self.config.logging.log_level}")
    
    def get_model_config(self) -> ModelConfig:
        """Get model configuration."""
        return self.config.model
    
    def get_performance_config(self) -> PerformanceConfig:
        """Get performance configuration."""
        return self.config.performance
    
    def get_logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self.config.logging
    
    def get_sentiment_labels(self) -> Dict[str, str]:
        """Get sentiment label mapping."""
        return self.config.sentiment_labels
    
    def get_confidence_thresholds(self) -> Dict[str, float]:
        """Get confidence thresholds."""
        return {
            "high": self.config.high_confidence_threshold,
            "low": self.config.low_confidence_threshold
        }
    
    def validate_config(self) -> bool:
        """Validate configuration values."""
        try:
            # Validate model configuration
            if not self.config.model.default_model:
                logger.error("Default model name cannot be empty")
                return False
            
            if self.config.model.max_text_length <= 0:
                logger.error("Max text length must be positive")
                return False
            
            # Validate performance configuration
            if self.config.performance.max_processing_time_ms <= 0:
                logger.error("Max processing time must be positive")
                return False
            
            if self.config.performance.cache_ttl_seconds <= 0:
                logger.error("Cache TTL must be positive")
                return False
            
            # Validate confidence thresholds
            if not (0.0 <= self.config.high_confidence_threshold <= 1.0):
                logger.error("High confidence threshold must be between 0.0 and 1.0")
                return False
            
            if not (0.0 <= self.config.low_confidence_threshold <= 1.0):
                logger.error("Low confidence threshold must be between 0.0 and 1.0")
                return False
            
            if self.config.low_confidence_threshold >= self.config.high_confidence_threshold:
                logger.error("Low confidence threshold must be less than high confidence threshold")
                return False
            
            logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "model": {
                "default_model": self.config.model.default_model,
                "cache_dir": self.config.model.cache_dir,
                "max_text_length": self.config.model.max_text_length,
                "batch_size": self.config.model.batch_size
            },
            "performance": {
                "max_processing_time_ms": self.config.performance.max_processing_time_ms,
                "enable_caching": self.config.performance.enable_caching,
                "cache_ttl_seconds": self.config.performance.cache_ttl_seconds,
                "enable_gpu": self.config.performance.enable_gpu
            },
            "logging": {
                "log_level": self.config.logging.log_level,
                "enable_performance_logging": self.config.logging.enable_performance_logging,
                "enable_validation_logging": self.config.logging.enable_validation_logging
            },
            "sentiment_labels": self.config.sentiment_labels,
            "confidence_thresholds": {
                "high": self.config.high_confidence_threshold,
                "low": self.config.low_confidence_threshold
            }
        }

# Global configuration instance
config_manager = ConfigManager()

def get_config() -> SentimentAnalysisConfig:
    """Get the global configuration instance."""
    return config_manager.config

def get_model_config() -> ModelConfig:
    """Get model configuration."""
    return config_manager.get_model_config()

def get_performance_config() -> PerformanceConfig:
    """Get performance configuration."""
    return config_manager.get_performance_config()

def get_logging_config() -> LoggingConfig:
    """Get logging configuration."""
    return config_manager.get_logging_config()
