"""
Sentiment Classification Pipeline using Hugging Face Transformers.

This module provides a high-performance sentiment analysis pipeline using
pre-trained BERT models with automatic caching and confidence scoring.
"""

import time
import logging
from typing import Dict, Any, Optional, Tuple
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Configure logging
logger = logging.getLogger(__name__)

class SentimentClassificationPipeline:
    """
    High-performance sentiment classification pipeline using Hugging Face Transformers.
    
    Features:
    - Automatic model caching
    - Confidence scoring
    - Performance monitoring
    - Comprehensive error handling
    """
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize the sentiment classification pipeline.
        
        Args:
            model_name: Hugging Face model identifier for sentiment classification
        """
        self.model_name = model_name
        self.pipeline = None
        self.tokenizer = None
        self.model = None
        self._is_initialized = False
        
        # Sentiment label mapping
        self.label_mapping = {
            0: "negative",
            1: "positive"
        }
        
        logger.info(f"Initializing sentiment pipeline with model: {model_name}")
    
    def _initialize_pipeline(self) -> None:
        """Initialize the Hugging Face pipeline and model components."""
        try:
            logger.info("Loading sentiment classification pipeline...")
            
            # Create the pipeline with automatic caching
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                return_all_scores=True,
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Load tokenizer and model separately for additional control
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            
            self._is_initialized = True
            logger.info("Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {str(e)}")
            raise RuntimeError(f"Pipeline initialization failed: {str(e)}")
    
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predict sentiment for the given text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing sentiment analysis results:
            - sentiment_label: "positive", "negative", or "neutral"
            - confidence_score: Confidence score (0.0-1.0)
            - processing_time_ms: Processing time in milliseconds
            - model_confidence: Raw model confidence scores
        """
        start_time = time.time()
        
        try:
            # Ensure pipeline is initialized
            if not self._is_initialized:
                self._initialize_pipeline()
            
            # Validate input
            if not text or not text.strip():
                raise ValueError("Input text cannot be empty")
            
            if len(text) > 10000:  # Reasonable limit for BERT models
                raise ValueError("Input text too long (max 10,000 characters)")
            
            # Perform prediction
            results = self.pipeline(text)
            
            # Extract confidence scores
            if results and len(results) > 0:
                scores = results[0]
                
                # Find the highest confidence score
                max_score = max(scores, key=lambda x: x['score'])
                confidence_score = max_score['score']
                predicted_label = max_score['label']
                
                # Map to our standard labels
                sentiment_label = self._map_sentiment_label(predicted_label)
                
            else:
                # Fallback for edge cases
                sentiment_label = "neutral"
                confidence_score = 0.5
            
            # Calculate processing time
            processing_time_ms = (time.time() - start_time) * 1000
            
            # Prepare response
            result = {
                "sentiment_label": sentiment_label,
                "confidence_score": round(confidence_score, 4),
                "processing_time_ms": round(processing_time_ms, 2),
                "model_confidence": results if results else [],
                "input_text_length": len(text)
            }
            
            logger.info(f"Sentiment prediction completed in {processing_time_ms:.2f}ms")
            return result
            
        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000
            logger.error(f"Prediction failed after {processing_time_ms:.2f}ms: {str(e)}")
            raise
    
    def _map_sentiment_label(self, model_label: str) -> str:
        """
        Map model-specific labels to standard sentiment labels.
        
        Args:
            model_label: Raw label from the model
            
        Returns:
            Standardized sentiment label
        """
        # Handle common label variations
        label_lower = model_label.lower()
        
        if any(positive in label_lower for positive in ["positive", "pos", "1"]):
            return "positive"
        elif any(negative in label_lower for negative in ["negative", "neg", "0"]):
            return "negative"
        else:
            return "neutral"
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary containing model metadata
        """
        if not self._is_initialized:
            return {"status": "not_initialized"}
        
        return {
            "model_name": self.model_name,
            "model_type": "DistilBERT",
            "framework": "PyTorch",
            "device": "CUDA" if torch.cuda.is_available() else "CPU",
            "status": "initialized"
        }

# Convenience function for quick sentiment analysis
def analyze_sentiment(text: str, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english") -> Dict[str, Any]:
    """
    Convenience function for quick sentiment analysis.
    
    Args:
        text: Input text to analyze
        model_name: Hugging Face model identifier
        
    Returns:
        Sentiment analysis results
    """
    pipeline = SentimentClassificationPipeline(model_name)
    return pipeline.predict(text)
