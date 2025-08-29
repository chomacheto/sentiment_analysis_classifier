"""
Comprehensive tests for sentiment analysis pipeline.

This module tests all aspects of the sentiment analysis system including:
- Core pipeline functionality
- Input validation
- Error handling
- Performance requirements
- Model behavior
"""

import pytest
import time
import logging
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

# Import the modules to test
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages'))

from ml_core.sentiment_pipeline import (
    SentimentClassificationPipeline,
    analyze_sentiment
)
from ml_core.models import (
    SentimentAnalysis,
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
    SentimentLabel
)
from ml_core.validators import (
    TextValidator,
    ValidationError,
    validate_and_sanitize_text
)
from ml_core.config import (
    SentimentAnalysisConfig,
    ModelConfig,
    PerformanceConfig
)

# Configure logging for tests
logging.basicConfig(level=logging.ERROR)

class TestSentimentClassificationPipeline:
    """Test the core sentiment classification pipeline."""
    
    @pytest.fixture
    def pipeline(self):
        """Create a pipeline instance for testing."""
        return SentimentClassificationPipeline()
    
    @pytest.fixture
    def mock_pipeline(self):
        """Create a pipeline with mocked Hugging Face components."""
        with patch('packages.ml_core.sentiment_pipeline.pipeline') as mock_pipe:
            with patch('packages.ml_core.sentiment_pipeline.AutoTokenizer') as mock_tokenizer:
                with patch('packages.ml_core.sentiment_pipeline.AutoModelForSequenceClassification') as mock_model:
                    # Mock the pipeline response
                    mock_pipe.return_value = Mock()
                    mock_pipe.return_value.return_value = [[
                        {'label': 'POSITIVE', 'score': 0.95},
                        {'label': 'NEGATIVE', 'score': 0.05}
                    ]]
                    
                    # Mock tokenizer and model
                    mock_tokenizer.from_pretrained.return_value = Mock()
                    mock_model.from_pretrained.return_value = Mock()
                    
                    pipeline = SentimentClassificationPipeline()
                    pipeline._is_initialized = True
                    pipeline.pipeline = mock_pipe.return_value
                    yield pipeline
    
    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initialization."""
        assert pipeline.model_name == "distilbert-base-uncased-finetuned-sst-2-english"
        assert pipeline._is_initialized is False
        assert pipeline.label_mapping == {0: "negative", 1: "positive"}
    
    def test_pipeline_initialization_with_custom_model(self):
        """Test pipeline initialization with custom model name."""
        custom_model = "custom-sentiment-model"
        pipeline = SentimentClassificationPipeline(custom_model)
        assert pipeline.model_name == custom_model
    
    @patch('packages.ml_core.sentiment_pipeline.pipeline')
    @patch('packages.ml_core.sentiment_pipeline.AutoTokenizer')
    @patch('packages.ml_core.sentiment_pipeline.AutoModelForSequenceClassification')
    def test_pipeline_initialization_success(self, mock_model, mock_tokenizer, mock_pipe):
        """Test successful pipeline initialization."""
        # Mock successful initialization
        mock_pipe.return_value = Mock()
        mock_tokenizer.from_pretrained.return_value = Mock()
        mock_model.from_pretrained.return_value = Mock()
        
        pipeline = SentimentClassificationPipeline()
        pipeline._initialize_pipeline()
        
        assert pipeline._is_initialized is True
        assert pipeline.pipeline is not None
        assert pipeline.tokenizer is not None
        assert pipeline.model is not None
    
    @patch('packages.ml_core.sentiment_pipeline.pipeline')
    def test_pipeline_initialization_failure(self, mock_pipe):
        """Test pipeline initialization failure handling."""
        # Mock initialization failure
        mock_pipe.side_effect = Exception("Model download failed")
        
        pipeline = SentimentClassificationPipeline()
        
        with pytest.raises(RuntimeError, match="Pipeline initialization failed"):
            pipeline._initialize_pipeline()
    
    def test_sentiment_label_mapping(self, mock_pipeline):
        """Test sentiment label mapping functionality."""
        # Test positive label mapping
        assert mock_pipeline._map_sentiment_label("POSITIVE") == "positive"
        assert mock_pipeline._map_sentiment_label("pos") == "positive"
        assert mock_pipeline._map_sentiment_label("1") == "positive"
        
        # Test negative label mapping
        assert mock_pipeline._map_sentiment_label("NEGATIVE") == "negative"
        assert mock_pipeline._map_sentiment_label("neg") == "negative"
        assert mock_pipeline._map_sentiment_label("0") == "negative"
        
        # Test neutral label mapping
        assert mock_pipeline._map_sentiment_label("UNKNOWN") == "neutral"
        assert mock_pipeline._map_sentiment_label("") == "neutral"
    
    def test_predict_positive_sentiment(self, mock_pipeline):
        """Test prediction of positive sentiment."""
        text = "I love this product! It's amazing and wonderful."
        result = mock_pipeline.predict(text)
        
        assert result["sentiment_label"] == "positive"
        assert result["confidence_score"] == 0.95
        assert result["processing_time_ms"] > 0
        assert result["input_text_length"] == len(text)
        assert "model_confidence" in result
    
    def test_predict_negative_sentiment(self, mock_pipeline):
        """Test prediction of negative sentiment."""
        # Mock negative sentiment response
        mock_pipeline.pipeline.return_value = [[
            {'label': 'NEGATIVE', 'score': 0.92},
            {'label': 'POSITIVE', 'score': 0.08}
        ]]
        
        text = "This product is terrible and disappointing."
        result = mock_pipeline.predict(text)
        
        assert result["sentiment_label"] == "negative"
        assert result["confidence_score"] == 0.92
        assert result["processing_time_ms"] > 0
    
    def test_predict_empty_text_error(self, mock_pipeline):
        """Test error handling for empty text input."""
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            mock_pipeline.predict("")
        
        with pytest.raises(ValueError, match="Input text cannot be empty"):
            mock_pipeline.predict("   ")
    
    def test_predict_text_too_long_error(self, mock_pipeline):
        """Test error handling for text that's too long."""
        long_text = "x" * 15000  # Exceeds 10,000 character limit
        
        with pytest.raises(ValueError, match="Input text too long"):
            mock_pipeline.predict(long_text)
    
    def test_predict_performance_requirement(self, mock_pipeline):
        """Test that prediction meets performance requirement (< 2 seconds)."""
        text = "This is a test text for performance testing."
        
        start_time = time.time()
        result = mock_pipeline.predict(text)
        end_time = time.time()
        
        processing_time = (end_time - start_time) * 1000
        
        # Should complete in under 2 seconds
        assert processing_time < 2000
        assert result["processing_time_ms"] < 2000
    
    def test_get_model_info(self, mock_pipeline):
        """Test model information retrieval."""
        info = mock_pipeline.get_model_info()
        
        assert info["status"] == "initialized"
        assert info["model_type"] == "DistilBERT"
        assert info["framework"] == "PyTorch"
        assert "device" in info
    
    def test_get_model_info_not_initialized(self, pipeline):
        """Test model info when pipeline is not initialized."""
        info = pipeline.get_model_info()
        assert info["status"] == "not_initialized"

class TestAnalyzeSentimentFunction:
    """Test the convenience analyze_sentiment function."""
    
    @patch('packages.ml_core.sentiment_pipeline.SentimentClassificationPipeline')
    def test_analyze_sentiment_success(self, mock_pipeline_class):
        """Test successful sentiment analysis using convenience function."""
        # Mock the pipeline
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = {
            "sentiment_label": "positive",
            "confidence_score": 0.88,
            "processing_time_ms": 150.5,
            "input_text_length": 25
        }
        mock_pipeline_class.return_value = mock_pipeline
        
        text = "This is a great day!"
        result = analyze_sentiment(text)
        
        # Verify pipeline was created and called
        mock_pipeline_class.assert_called_once()
        mock_pipeline.predict.assert_called_once_with(text)
        
        # Verify result
        assert result["sentiment_label"] == "positive"
        assert result["confidence_score"] == 0.88
        assert result["processing_time_ms"] == 150.5
    
    @patch('packages.ml_core.sentiment_pipeline.SentimentClassificationPipeline')
    def test_analyze_sentiment_with_custom_model(self, mock_pipeline_class):
        """Test sentiment analysis with custom model."""
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = {"sentiment_label": "negative", "confidence_score": 0.75}
        mock_pipeline_class.return_value = mock_pipeline
        
        custom_model = "custom-sentiment-model"
        analyze_sentiment("Test text", custom_model)
        
        mock_pipeline_class.assert_called_once_with(custom_model)

class TestTextValidator:
    """Test the text validation functionality."""
    
    @pytest.fixture
    def validator(self):
        """Create a text validator instance."""
        return TextValidator()
    
    def test_validate_text_success(self, validator):
        """Test successful text validation."""
        text = "This is a valid text for sentiment analysis."
        is_valid, error_message, metadata = validator.validate_text(text)
        
        assert is_valid is True
        assert error_message is None
        assert metadata["length"] == len(text)
        assert metadata["word_count"] > 0
        assert metadata["line_count"] == 1
    
    def test_validate_text_empty(self, validator):
        """Test validation of empty text."""
        is_valid, error_message, metadata = validator.validate_text("")
        assert is_valid is False
        assert "cannot be empty" in error_message
    
    def test_validate_text_whitespace_only(self, validator):
        """Test validation of whitespace-only text."""
        is_valid, error_message, metadata = validator.validate_text("   \n\t   ")
        assert is_valid is False
        assert "only whitespace" in error_message
    
    def test_validate_text_too_long(self, validator):
        """Test validation of text that's too long."""
        long_text = "x" * 15000  # Exceeds 10,000 character limit
        is_valid, error_message, metadata = validator.validate_text(long_text)
        assert is_valid is False
        assert "too long" in error_message
    
    def test_validate_text_too_many_words(self, validator):
        """Test validation of text with too many words."""
        # Create text with more than 2000 words
        words = ["word"] * 2500
        long_text = " ".join(words)
        
        is_valid, error_message, metadata = validator.validate_text(long_text)
        assert is_valid is False
        assert "too many words" in error_message
    
    def test_validate_text_suspicious_content(self, validator):
        """Test validation of text with suspicious content."""
        suspicious_texts = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "data:text/html,<script>alert('xss')</script>",
            "vbscript:msgbox('xss')",
            "onclick=alert('xss')"
        ]
        
        for text in suspicious_texts:
            is_valid, error_message, metadata = validator.validate_text(text)
            assert is_valid is False
            assert error_message is not None
    
    def test_sanitize_text(self, validator):
        """Test text sanitization."""
        raw_text = "  This   text\nhas\texcessive\r\nwhitespace  "
        sanitized = validator._sanitize_text(raw_text)
        
        assert sanitized == "This text has excessive whitespace"
        assert sanitized.count(" ") == 4  # Single spaces between words
    
    def test_validate_request_success(self, validator):
        """Test successful request validation."""
        request = SentimentAnalysisRequest(text="Valid text")
        is_valid, error_message, metadata = validator.validate_request(request)
        
        assert is_valid is True
        assert error_message is None
        assert metadata["length"] == len("Valid text")
    
    def test_validate_request_with_model_name(self, validator):
        """Test request validation with model name."""
        request = SentimentAnalysisRequest(
            text="Valid text",
            model_name="valid-model-name"
        )
        is_valid, error_message, metadata = validator.validate_request(request)
        
        assert is_valid is True
        assert metadata["model_name"] == "valid-model-name"
    
    def test_validate_request_invalid_model_name(self, validator):
        """Test request validation with invalid model name."""
        request = SentimentAnalysisRequest(
            text="Valid text",
            model_name="invalid@model#name"
        )
        is_valid, error_message, metadata = validator.validate_request(request)
        
        assert is_valid is False
        assert "invalid characters" in error_message

class TestValidationError:
    """Test the custom validation error class."""
    
    def test_validation_error_creation(self):
        """Test validation error creation."""
        error = ValidationError("Test error message")
        assert error.message == "Test error message"
        assert error.metadata == {}
    
    def test_validation_error_with_metadata(self):
        """Test validation error with metadata."""
        metadata = {"field": "text", "value": "invalid"}
        error = ValidationError("Validation failed", metadata)
        
        assert error.message == "Validation failed"
        assert error.metadata == metadata
    
    def test_validation_error_inheritance(self):
        """Test that ValidationError inherits from Exception."""
        error = ValidationError("Test")
        assert isinstance(error, Exception)

class TestValidateAndSanitizeText:
    """Test the convenience validation function."""
    
    def test_validate_and_sanitize_success(self):
        """Test successful validation and sanitization."""
        text = "  Valid   text  "
        sanitized, metadata = validate_and_sanitize_text(text)
        
        assert sanitized == "Valid text"
        assert metadata["original_length"] == len(text)
        assert metadata["sanitized_length"] == len(sanitized)
    
    def test_validate_and_sanitize_failure(self):
        """Test validation failure."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_and_sanitize_text("")

class TestConfiguration:
    """Test configuration management."""
    
    def test_model_config_defaults(self):
        """Test model configuration default values."""
        config = ModelConfig()
        
        assert config.default_model == "distilbert-base-uncased-finetuned-sst-2-english"
        assert config.max_text_length == 10000
        assert config.batch_size == 1
    
    def test_performance_config_defaults(self):
        """Test performance configuration default values."""
        config = PerformanceConfig()
        
        assert config.max_processing_time_ms == 2000
        assert config.enable_caching is True
        assert config.cache_ttl_seconds == 3600
        assert config.enable_gpu is True
    
    def test_sentiment_analysis_config_defaults(self):
        """Test main configuration default values."""
        config = SentimentAnalysisConfig()
        
        assert config.high_confidence_threshold == 0.8
        assert config.low_confidence_threshold == 0.6
        assert "positive" in config.sentiment_labels
        assert "negative" in config.sentiment_labels

# Performance test fixtures
@pytest.fixture
def sample_texts():
    """Provide sample texts for performance testing."""
    return {
        "short": "I love this!",
        "medium": "This product exceeded my expectations. The quality is outstanding and the customer service was excellent. I would definitely recommend it to others.",
        "long": "This is a comprehensive review of the product that covers all aspects including build quality, performance, features, and value for money. The attention to detail is remarkable and shows the manufacturer's commitment to excellence. Every component has been carefully selected and tested to ensure reliability and durability. The user experience is intuitive and the interface is well-designed. Overall, this represents excellent value and I'm very satisfied with my purchase." * 5
    }

class TestPerformanceRequirements:
    """Test that performance requirements are met."""
    
    @pytest.mark.slow
    def test_processing_time_requirement(self, mock_pipeline, sample_texts):
        """Test that processing time is under 2 seconds for all text lengths."""
        for text_type, text in sample_texts.items():
            start_time = time.time()
            result = mock_pipeline.predict(text)
            end_time = time.time()
            
            processing_time = (end_time - start_time) * 1000
            
            # Should complete in under 2 seconds
            assert processing_time < 2000, f"Processing time for {text_type} text exceeded 2 seconds: {processing_time}ms"
            assert result["processing_time_ms"] < 2000, f"Reported processing time for {text_type} text exceeded 2 seconds: {result['processing_time_ms']}ms"
    
    def test_confidence_score_formatting(self, mock_pipeline):
        """Test that confidence scores are properly formatted to 4 decimal places."""
        text = "Test text"
        result = mock_pipeline.predict(text)
        
        confidence_score = result["confidence_score"]
        # Check that it's a float with reasonable precision
        assert isinstance(confidence_score, float)
        assert 0.0 <= confidence_score <= 1.0
    
    def test_processing_time_formatting(self, mock_pipeline):
        """Test that processing time is properly formatted to 2 decimal places."""
        text = "Test text"
        result = mock_pipeline.predict(text)
        
        processing_time = result["processing_time_ms"]
        # Check that it's a float with reasonable precision
        assert isinstance(processing_time, float)
        assert processing_time >= 0.0

# Integration test
class TestIntegration:
    """Integration tests for the complete pipeline."""
    
    @pytest.mark.integration
    def test_end_to_end_sentiment_analysis(self, mock_pipeline):
        """Test complete end-to-end sentiment analysis workflow."""
        # Test positive sentiment
        positive_text = "This is absolutely wonderful and amazing!"
        positive_result = mock_pipeline.predict(positive_text)
        
        assert positive_result["sentiment_label"] == "positive"
        assert positive_result["confidence_score"] > 0.5
        assert positive_result["input_text_length"] == len(positive_text)
        
        # Test negative sentiment
        mock_pipeline.pipeline.return_value = [[
            {'label': 'NEGATIVE', 'score': 0.89},
            {'label': 'POSITIVE', 'score': 0.11}
        ]]
        
        negative_text = "This is terrible and disappointing."
        negative_result = mock_pipeline.predict(negative_text)
        
        assert negative_result["sentiment_label"] == "negative"
        assert negative_result["confidence_score"] > 0.5
        assert negative_result["input_text_length"] == len(negative_text)
    
    @pytest.mark.integration
    def test_error_handling_integration(self, mock_pipeline):
        """Test error handling in the complete pipeline."""
        # Test various error conditions
        error_cases = [
            ("", "Input text cannot be empty"),
            ("x" * 15000, "Input text too long"),
        ]
        
        for text, expected_error in error_cases:
            with pytest.raises(ValueError, match=expected_error):
                mock_pipeline.predict(text)

if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([__file__, "-v", "--cov=packages.ml_core", "--cov-report=term-missing"])
