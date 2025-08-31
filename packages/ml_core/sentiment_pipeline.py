"""
Sentiment Classification Pipeline using Hugging Face Transformers.

This module provides a high-performance sentiment analysis pipeline using
pre-trained BERT models with automatic caching and confidence scoring.
"""

import time
import logging
from typing import Dict, Any, Optional, Tuple, List
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

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
    
    def predict(self, text: str, include_attention: bool = False) -> Dict[str, Any]:
        """
        Predict sentiment for the given text.
        
        Args:
            text: Input text to analyze
            include_attention: Whether to include attention weights in the response
            
        Returns:
            Dictionary containing sentiment analysis results:
            - sentiment_label: "positive", "negative", or "neutral"
            - confidence_score: Confidence score (0.0-1.0)
            - processing_time_ms: Processing time in milliseconds
            - model_confidence: Raw model confidence scores
            - attention_weights: Word-level attention weights (if include_attention=True)
            - word_contributions: Individual word contribution scores (if include_attention=True)
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
            
            # Extract attention weights if requested
            attention_data = {}
            if include_attention:
                attention_data = self._extract_attention_weights(text)
            
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
            
            # Add attention data if available
            if attention_data:
                result.update(attention_data)
            
            logger.info(f"Sentiment prediction completed in {processing_time_ms:.2f}ms")
            return result
            
        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000
            logger.error(f"Prediction failed after {processing_time_ms:.2f}ms: {str(e)}")
            raise
    
    def _extract_attention_weights(self, text: str) -> Dict[str, Any]:
        """
        Extract attention weights and word contributions from the model.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing attention analysis data
        """
        try:
            # Tokenize the input text
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            # Get model outputs with attention
            with torch.no_grad():
                outputs = self.model(**inputs, output_attentions=True)
                attentions = outputs.attentions  # Tuple of attention tensors
                logits = outputs.logits
            
            # Get the last layer attention weights (most relevant for classification)
            last_layer_attention = attentions[-1]  # Shape: (batch_size, num_heads, seq_len, seq_len)
            
            # Average attention across all heads
            avg_attention = torch.mean(last_layer_attention, dim=1)  # Shape: (batch_size, seq_len, seq_len)
            
            # Get attention weights for the [CLS] token (classification token)
            cls_attention = avg_attention[0, 0, :]  # Shape: (seq_len,)
            
            # Get tokens for visualization
            tokens = self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
            
            # Calculate word-level attention scores
            word_attention_scores = []
            word_contributions = []
            
            for i, token in enumerate(tokens):
                if token in ['[CLS]', '[SEP]', '[PAD]']:
                    continue
                    
                # Get attention score for this token
                attention_score = float(cls_attention[i])
                
                # Calculate contribution score (attention * sentiment influence)
                sentiment_influence = 1.0 if self.label_mapping[torch.argmax(logits[0]).item()] == "positive" else -1.0
                contribution_score = attention_score * sentiment_influence
                
                word_attention_scores.append({
                    "token": token,
                    "attention_score": round(attention_score, 4),
                    "contribution_score": round(contribution_score, 4)
                })
                
                word_contributions.append({
                    "token": token,
                    "score": round(contribution_score, 4)
                })
            
            # Sort by absolute contribution score for ranking
            word_contributions.sort(key=lambda x: abs(x["score"]), reverse=True)
            
            return {
                "attention_weights": word_attention_scores,
                "word_contributions": word_contributions,
                "top_contributing_words": word_contributions[:10]  # Top 10 words
            }
            
        except Exception as e:
            logger.error(f"Failed to extract attention weights: {str(e)}")
            return {
                "attention_weights": [],
                "word_contributions": [],
                "top_contributing_words": []
            }
    
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
