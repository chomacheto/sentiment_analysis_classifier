"""
Pytest configuration and common fixtures for the sentiment analysis classifier.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import structlog


@pytest.fixture(scope="session")
def temp_dir():
    """Create a temporary directory for the test session."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture(scope="function")
def mock_logger():
    """Provide a mock logger for testing."""
    return MagicMock(spec=structlog.BoundLogger)


@pytest.fixture(scope="function")
def sample_text_data():
    """Provide sample text data for testing."""
    return [
        "I love this product! It's amazing.",
        "This is terrible. I hate it.",
        "The quality is okay, nothing special.",
        "Absolutely fantastic experience!",
        "Very disappointing and poor service.",
    ]


@pytest.fixture(scope="function")
def sample_sentiment_labels():
    """Provide sample sentiment labels for testing."""
    return ["positive", "negative", "neutral", "positive", "negative"]


@pytest.fixture(scope="function")
def mock_ml_model():
    """Provide a mock ML model for testing."""
    model = MagicMock()
    model.name = "test-bert-model"
    model.predict.return_value = [0.8, 0.1, 0.1]  # Mock prediction
    return model


@pytest.fixture(scope="function")
def mock_database():
    """Provide a mock database connection for testing."""
    db = MagicMock()
    db.execute.return_value = MagicMock()
    db.commit.return_value = None
    db.rollback.return_value = None
    return db


@pytest.fixture(scope="function")
def mock_cache():
    """Provide a mock cache for testing."""
    cache = MagicMock()
    cache.get.return_value = None
    cache.set.return_value = True
    cache.delete.return_value = True
    return cache


@pytest.fixture(scope="function")
def sample_api_request():
    """Provide sample API request data for testing."""
    return {
        "text": "This is a test text for sentiment analysis.",
        "model": "bert-base-uncased",
        "confidence_threshold": 0.8,
    }


@pytest.fixture(scope="function")
def sample_api_response():
    """Provide sample API response data for testing."""
    return {
        "sentiment": "positive",
        "confidence": 0.92,
        "model": "bert-base-uncased",
        "processing_time": 0.15,
        "timestamp": "2025-08-29T23:43:00Z",
    }


@pytest.fixture(scope="function")
def mock_streamlit_session_state():
    """Provide a mock Streamlit session state for testing."""
    session_state = MagicMock()
    session_state.get.return_value = None
    session_state.__setitem__ = MagicMock()
    session_state.__getitem__ = MagicMock(return_value=None)
    return session_state


@pytest.fixture(scope="function")
def mock_environment_variables():
    """Provide mock environment variables for testing."""
    return {
        "ENVIRONMENT": "test",
        "LOG_LEVEL": "DEBUG",
        "DATABASE_URL": "postgresql://test:test@localhost:5432/testdb",
        "REDIS_URL": "redis://localhost:6379/0",
        "MODEL_CACHE_DIR": "/tmp/models",
    }


@pytest.fixture(scope="function", autouse=True)
def reset_structlog():
    """Reset structlog configuration before each test."""
    structlog.reset_defaults()
    yield
    structlog.reset_defaults()


@pytest.fixture(scope="function")
def sample_logging_config():
    """Provide sample logging configuration for testing."""
    return {
        "log_level": "DEBUG",
        "log_format": "console",
        "environment": "test",
        "log_file": None,
    }


@pytest.fixture(scope="function")
def mock_file_system():
    """Provide a mock file system for testing."""
    fs = MagicMock()
    fs.exists.return_value = True
    fs.mkdir.return_value = None
    fs.write_text.return_value = None
    fs.read_text.return_value = "test content"
    return fs


@pytest.fixture(scope="function")
def sample_error_context():
    """Provide sample error context for testing."""
    return {
        "user_id": "test_user_123",
        "operation": "sentiment_analysis",
        "input_text": "test text",
        "model_version": "1.0.0",
        "timestamp": "2025-08-29T23:43:00Z",
    }


@pytest.fixture(scope="function")
def mock_http_client():
    """Provide a mock HTTP client for testing."""
    client = MagicMock()
    client.get.return_value = MagicMock(status_code=200, json=lambda: {"status": "ok"})
    client.post.return_value = MagicMock(status_code=200, json=lambda: {"status": "ok"})
    return client


@pytest.fixture(scope="function")
def sample_ml_operation_data():
    """Provide sample ML operation data for testing."""
    return {
        "operation": "inference",
        "model_name": "bert-base-uncased",
        "input_shape": (1, 512),
        "output_shape": (1, 3),
        "batch_size": 32,
        "device": "cpu",
        "framework": "pytorch",
        "version": "2.8.0",
    }


@pytest.fixture(scope="function")
def mock_async_context():
    """Provide a mock async context for testing."""
    context = MagicMock()
    context.__aenter__ = MagicMock(return_value=context)
    context.__aexit__ = MagicMock(return_value=None)
    return context


@pytest.fixture(scope="function")
def sample_validation_error():
    """Provide a sample validation error for testing."""
    from pydantic import ValidationError
    
    try:
        # This will raise a ValidationError
        raise ValidationError.from_exception_data(
            "ValidationError",
            [
                {
                    "loc": ("field_name",),
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
            {},
        )
    except ValidationError as e:
        return e


@pytest.fixture(scope="function")
def mock_metrics_collector():
    """Provide a mock metrics collector for testing."""
    collector = MagicMock()
    collector.increment.return_value = None
    collector.timing.return_value = None
    collector.gauge.return_value = None
    collector.histogram.return_value = None
    return collector


@pytest.fixture(scope="function")
def sample_performance_metrics():
    """Provide sample performance metrics for testing."""
    return {
        "inference_time_ms": 150.5,
        "memory_usage_mb": 512.0,
        "cpu_usage_percent": 25.3,
        "gpu_usage_percent": 0.0,
        "throughput_requests_per_second": 6.67,
        "error_rate_percent": 0.1,
    }
