"""
Tests for the logging configuration module.
"""

import logging
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import structlog

from packages.shared.logging_config import (
    configure_logging,
    get_logger,
    log_error,
    log_function_call,
    log_function_result,
    log_ml_operation,
    setup_default_logging,
)


class TestLoggingConfiguration:
    """Test logging configuration functionality."""

    def test_configure_logging_development(self):
        """Test logging configuration for development environment."""
        with patch("sys.stdout") as mock_stdout:
            configure_logging(
                log_level="DEBUG",
                log_format="console",
                environment="development",
            )
            
            # Verify structlog is configured
            assert structlog.is_configured()
            
            # Verify logging level is set
            root_logger = logging.getLogger()
            assert root_logger.level == logging.DEBUG

    def test_configure_logging_production(self):
        """Test logging configuration for production environment."""
        with patch("sys.stdout") as mock_stdout:
            configure_logging(
                log_level="INFO",
                log_format="json",
                environment="production",
            )
            
            # Verify structlog is configured
            assert structlog.is_configured()
            
            # Verify logging level is set
            root_logger = logging.getLogger()
            assert root_logger.level == logging.INFO

    def test_configure_logging_with_file(self):
        """Test logging configuration with file handler."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            
            configure_logging(
                log_level="WARNING",
                log_format="json",
                log_file=log_file,
                environment="production",
            )
            
            # Verify log file is created
            assert log_file.exists()
            
            # Verify file handler is added
            root_logger = logging.getLogger()
            file_handlers = [h for h in root_logger.handlers if isinstance(h, logging.FileHandler)]
            assert len(file_handlers) > 0

    def test_get_logger(self):
        """Test getting a logger instance."""
        configure_logging()
        logger = get_logger("test_module")
        
        assert isinstance(logger, structlog.BoundLogger)
        assert logger.name == "test_module"

    def test_log_function_call(self):
        """Test logging function calls."""
        configure_logging(log_level="DEBUG")
        
        with patch("structlog.get_logger") as mock_get_logger:
            mock_logger = mock_get_logger.return_value
            
            log_function_call("test_function", param1="value1", param2=42)
            
            mock_logger.debug.assert_called_once()
            call_args = mock_logger.debug.call_args[1]
            assert call_args["function"] == "test_function"
            assert call_args["parameters"]["param1"] == "value1"
            assert call_args["parameters"]["param2"] == 42

    def test_log_function_result(self):
        """Test logging function results."""
        configure_logging()
        
        with patch("structlog.get_logger") as mock_get_logger:
            mock_logger = mock_get_logger.return_value
            
            log_function_result("test_function", "result_value", 1.5)
            
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[1]
            assert call_args["function"] == "test_function"
            assert call_args["execution_time"] == 1.5
            assert call_args["result_type"] == "str"

    def test_log_error(self):
        """Test logging errors."""
        configure_logging()
        
        with patch("structlog.get_logger") as mock_get_logger:
            mock_logger = mock_get_logger.return_value
            
            test_error = ValueError("Test error message")
            context = {"user_id": 123, "operation": "test"}
            
            log_error(test_error, context)
            
            mock_logger.error.assert_called_once()
            call_args = mock_logger.error.call_args[1]
            assert call_args["error_type"] == "ValueError"
            assert call_args["error_message"] == "Test error message"
            assert call_args["context"] == context
            assert call_args["exc_info"] is True

    def test_log_ml_operation(self):
        """Test logging ML operations."""
        configure_logging()
        
        with patch("structlog.get_logger") as mock_get_logger:
            mock_logger = mock_get_logger.return_value
            
            log_ml_operation(
                operation="inference",
                model_name="bert-base-uncased",
                input_shape=(1, 512),
                output_shape=(1, 3),
                batch_size=32,
                device="cuda",
            )
            
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[1]
            assert call_args["operation"] == "inference"
            assert call_args["model"] == "bert-base-uncased"
            assert call_args["input_shape"] == (1, 512)
            assert call_args["output_shape"] == (1, 3)
            assert call_args["batch_size"] == 32
            assert call_args["device"] == "cuda"

    def test_setup_default_logging(self):
        """Test default logging setup."""
        with patch("packages.shared.logging_config.configure_logging") as mock_configure:
            setup_default_logging()
            
            mock_configure.assert_called_once_with(
                log_level="DEBUG",
                log_format="console",
                environment="development",
            )

    def test_invalid_log_level(self):
        """Test handling of invalid log level."""
        with pytest.raises(AttributeError):
            configure_logging(log_level="INVALID_LEVEL")

    def test_logging_integration(self):
        """Test that logging actually works end-to-end."""
        configure_logging(log_level="INFO")
        
        logger = get_logger("test_integration")
        
        # This should not raise any exceptions
        logger.info("Test message", extra_data="test_value")
        logger.warning("Warning message")
        logger.error("Error message")


if __name__ == "__main__":
    pytest.main([__file__])
