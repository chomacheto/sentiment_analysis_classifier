"""
Input validation and sanitization for sentiment analysis pipeline.

This module provides comprehensive validation for text inputs, including
length checks, content sanitization, and error handling.
"""

import re
import logging
from typing import Optional, Tuple, Dict, Any
from .models import SentimentAnalysisRequest

logger = logging.getLogger(__name__)

class TextValidator:
    """
    Comprehensive text validation for sentiment analysis.
    
    Features:
    - Length validation
    - Content sanitization
    - Language detection hints
    - Malicious content detection
    """
    
    # Validation constants
    MIN_TEXT_LENGTH = 1
    MAX_TEXT_LENGTH = 10000
    MAX_WORDS = 2000
    MAX_LINES = 100
    
    def __init__(self):
        """Initialize the text validator."""
        # Common patterns for validation
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.html_pattern = re.compile(r'<[^>]+>')
        
    def validate_text(self, text: str) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """
        Comprehensive text validation.
        
        Args:
            text: Text to validate
            
        Returns:
            Tuple of (is_valid, error_message, validation_metadata)
        """
        try:
            # Basic validation
            if not text:
                return False, "Text cannot be empty", {}
            
            if not isinstance(text, str):
                return False, "Text must be a string", {}
            
            # Length validation
            length_validation = self._validate_length(text)
            if not length_validation[0]:
                return length_validation
            
            # Content validation
            content_validation = self._validate_content(text)
            if not content_validation[0]:
                return content_validation
            
            # Sanitization
            sanitized_text = self._sanitize_text(text)
            
            # Prepare metadata
            metadata = {
                "original_length": len(text),
                "sanitized_length": len(sanitized_text),
                "length": length_validation[2].get("length", len(text)),  # Include length from validation
                "word_count": len(sanitized_text.split()),
                "line_count": len(sanitized_text.splitlines()),
                "contains_urls": bool(self.url_pattern.search(text)),
                "contains_emails": bool(self.email_pattern.search(text)),
                "contains_html": bool(self.html_pattern.search(text))
            }
            
            return True, None, metadata
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False, f"Validation failed: {str(e)}", {}
    
    def _validate_length(self, text: str) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """Validate text length constraints."""
        text_length = len(text.strip())
        
        if text_length < self.MIN_TEXT_LENGTH:
            return False, f"Text too short (minimum {self.MIN_TEXT_LENGTH} characters)", {}
        
        if text_length > self.MAX_TEXT_LENGTH:
            return False, f"Text too long (maximum {self.MAX_TEXT_LENGTH} characters)", {}
        
        return True, None, {"length": text_length}
    
    def _validate_content(self, text: str) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """Validate text content for appropriateness."""
        # Check for excessive whitespace
        if text.strip() == "":
            return False, "Text contains only whitespace", {}
        
        # Check word count
        words = text.split()
        if len(words) > self.MAX_WORDS:
            return False, f"Text contains too many words (maximum {self.MAX_WORDS})", {}
        
        # Check line count
        lines = text.splitlines()
        if len(lines) > self.MAX_LINES:
            return False, f"Text contains too many lines (maximum {self.MAX_LINES})", {}
        
        # Check for suspicious patterns (basic security)
        suspicious_patterns = [
            (r'<script', "HTML script tags not allowed"),
            (r'javascript:', "JavaScript code not allowed"),
            (r'data:text/html', "Data URLs not allowed"),
            (r'vbscript:', "VBScript not allowed"),
            (r'on\w+\s*=', "Event handlers not allowed")
        ]
        
        for pattern, message in suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False, message, {}
        
        return True, None, {}
    
    def _sanitize_text(self, text: str) -> str:
        """
        Sanitize text for safe processing.
        
        Args:
            text: Raw text to sanitize
            
        Returns:
            Sanitized text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove HTML tags
        text = re.sub(self.html_pattern, '', text)
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Trim whitespace
        text = text.strip()
        
        return text
    
    def validate_request(self, request: SentimentAnalysisRequest) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """
        Validate a complete sentiment analysis request.
        
        Args:
            request: SentimentAnalysisRequest object
            
        Returns:
            Tuple of (is_valid, error_message, validation_metadata)
        """
        try:
            # Validate text
            text_valid, text_error, text_metadata = self.validate_text(request.text)
            if not text_valid:
                return text_valid, text_error, text_metadata
            
            # Validate model name if provided
            if request.model_name:
                model_valid, model_error, model_metadata = self._validate_model_name(request.model_name)
                if not model_valid:
                    return model_valid, model_error, model_metadata
            else:
                model_metadata = {}
            
            # Combine metadata
            combined_metadata = {**text_metadata, **model_metadata}
            
            return True, None, combined_metadata
            
        except Exception as e:
            logger.error(f"Request validation error: {str(e)}")
            return False, f"Request validation failed: {str(e)}", {}
    
    def _validate_model_name(self, model_name: str) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """Validate Hugging Face model name format."""
        if not model_name or not isinstance(model_name, str):
            return False, "Model name must be a non-empty string", {}
        
        # Basic Hugging Face model name validation
        if len(model_name) > 200:
            return False, "Model name too long", {}
        
        # Check for valid characters (basic validation)
        if not re.match(r'^[a-zA-Z0-9\-_/]+$', model_name):
            return False, "Model name contains invalid characters", {}
        
        return True, None, {"model_name": model_name}

class ValidationError(Exception):
    """Custom exception for validation errors."""
    
    def __init__(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        self.message = message
        self.metadata = metadata or {}
        super().__init__(self.message)

def create_validation_error(message: str, metadata: Optional[Dict[str, Any]] = None) -> ValidationError:
    """
    Create a validation error with optional metadata.
    
    Args:
        message: Error message
        metadata: Optional metadata about the validation failure
        
    Returns:
        ValidationError instance
    """
    return ValidationError(message, metadata)

def validate_and_sanitize_text(text: str) -> Tuple[str, Dict[str, Any]]:
    """
    Convenience function to validate and sanitize text.
    
    Args:
        text: Text to validate and sanitize
        
    Returns:
        Tuple of (sanitized_text, validation_metadata)
        
    Raises:
        ValidationError: If validation fails
    """
    validator = TextValidator()
    is_valid, error_message, metadata = validator.validate_text(text)
    
    if not is_valid:
        raise create_validation_error(error_message, metadata)
    
    sanitized_text = validator._sanitize_text(text)
    return sanitized_text, metadata

def validate_text_input(text: str) -> str:
    """
    Simple text validation function for CLI usage.
    
    Args:
        text: Text to validate
        
    Returns:
        Validated and sanitized text
        
    Raises:
        ValueError: If validation fails
    """
    if not text:
        raise ValueError("Text cannot be empty")
    
    # Basic sanitization
    sanitized = text.strip()
    if not sanitized:
        raise ValueError("Text contains only whitespace")
    
    if len(sanitized) > 10000:
        raise ValueError("Text too long (maximum 10,000 characters)")
    
    return sanitized
