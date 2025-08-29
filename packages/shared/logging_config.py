"""
Logging configuration for the sentiment analysis classifier.

This module provides structured logging configuration using structlog,
supporting both development and production environments.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import structlog
from structlog.types import Processor


def configure_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    log_file: Optional[Path] = None,
    environment: str = "development",
) -> None:
    """
    Configure structured logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Output format ('json' or 'console')
        log_file: Optional file path for logging
        environment: Environment name ('development' or 'production')
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )
    
    # Set root logger level explicitly
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Configure structlog processors
    processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Add environment-specific processors
    if environment == "development":
        processors.extend([
            structlog.dev.ConsoleRenderer(colors=True),
        ])
    else:
        processors.extend([
            structlog.processors.JSONRenderer(),
        ])
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Add file handler if specified
    if log_file:
        _add_file_handler(log_file, log_level, environment)
    
    # Log configuration completion
    logger = structlog.get_logger(__name__)
    logger.info(
        "Logging configured",
        level=log_level,
        format=log_format,
        environment=environment,
        file=str(log_file) if log_file else None,
    )


def _add_file_handler(log_file: Path, log_level: str, environment: str) -> None:
    """Add file handler to the logging configuration."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Set formatter based on environment
    if environment == "development":
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        formatter = logging.Formatter("%(message)s")
    
    file_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    # Store reference for cleanup
    if not hasattr(root_logger, '_file_handlers'):
        root_logger._file_handlers = []
    root_logger._file_handlers.append(file_handler)


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured structlog logger
    """
    logger = structlog.get_logger(name)
    # Ensure the logger is properly bound
    if not structlog.is_configured():
        configure_logging()
    return logger


def log_function_call(func_name: str, **kwargs: Any) -> None:
    """
    Log function call with parameters.
    
    Args:
        func_name: Name of the function being called
        **kwargs: Function parameters to log
    """
    logger = structlog.get_logger(__name__)
    logger.debug(
        "Function call",
        function=func_name,
        parameters=kwargs,
    )


def log_function_result(func_name: str, result: Any, execution_time: float) -> None:
    """
    Log function execution result and timing.
    
    Args:
        func_name: Name of the function that was called
        result: Function return value
        execution_time: Execution time in seconds
    """
    logger = structlog.get_logger(__name__)
    logger.info(
        "Function completed",
        function=func_name,
        execution_time=execution_time,
        result_type=type(result).__name__,
    )


def log_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """
    Log error with context information.
    
    Args:
        error: Exception that occurred
        context: Additional context information
    """
    logger = structlog.get_logger(__name__)
    logger.error(
        "Error occurred",
        error_type=type(error).__name__,
        error_message=str(error),
        context=context or {},
        exc_info=True,
    )


def log_ml_operation(
    operation: str,
    model_name: str,
    input_shape: Optional[tuple] = None,
    output_shape: Optional[tuple] = None,
    **kwargs: Any,
) -> None:
    """
    Log ML operation details.
    
    Args:
        operation: Type of ML operation (e.g., 'inference', 'training')
        model_name: Name of the ML model
        input_shape: Shape of input data
        output_shape: Shape of output data
        **kwargs: Additional operation-specific parameters
    """
    logger = structlog.get_logger(__name__)
    logger.info(
        "ML operation",
        operation=operation,
        model=model_name,
        input_shape=input_shape,
        output_shape=output_shape,
        **kwargs,
    )


def cleanup_file_handlers() -> None:
    """Clean up file handlers to prevent file access issues."""
    root_logger = logging.getLogger()
    if hasattr(root_logger, '_file_handlers'):
        for handler in root_logger._file_handlers:
            try:
                handler.close()
                root_logger.removeHandler(handler)
            except Exception:
                pass
        root_logger._file_handlers.clear()


# Default configuration for quick setup
def setup_default_logging() -> None:
    """Set up default logging configuration for development."""
    configure_logging(
        log_level="DEBUG",
        log_format="console",
        environment="development",
    )


if __name__ == "__main__":
    # Example usage
    setup_default_logging()
    
    logger = get_logger(__name__)
    logger.info("Logging system initialized")
    
    # Example ML operation logging
    log_ml_operation(
        operation="inference",
        model_name="bert-base-uncased",
        input_shape=(1, 512),
        output_shape=(1, 3),
        batch_size=1,
    )
