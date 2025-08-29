"""
Tests for the sentiment analysis CLI.

This module tests the command line interface functionality including:
- Command parsing and argument handling
- Integration with sentiment pipeline
- Error handling and validation
- Output formatting
- Batch processing
"""

import pytest
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add the packages directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "packages"))

from ml_core.sentiment_pipeline import SentimentClassificationPipeline
from ml_core.models import SentimentAnalysis, SentimentLabel
from ml_core.validators import validate_text_input


class TestCLIValidation:
    """Test CLI input validation functionality."""
    
    def test_validate_text_input_valid(self):
        """Test validation of valid text input."""
        text = "This is a valid text for sentiment analysis."
        result = validate_text_input(text)
        assert result == text.strip()
    
    def test_validate_text_input_empty(self):
        """Test validation rejects empty text."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            validate_text_input("")
    
    def test_validate_text_input_whitespace_only(self):
        """Test validation rejects whitespace-only text."""
        with pytest.raises(ValueError, match="Text contains only whitespace"):
            validate_text_input("   \n\t  ")
    
    def test_validate_text_input_too_long(self):
        """Test validation rejects overly long text."""
        long_text = "a" * 10001
        with pytest.raises(ValueError, match="Text too long"):
            validate_text_input(long_text)
    
    def test_validate_text_input_strips_whitespace(self):
        """Test validation properly strips whitespace."""
        text = "  Hello World  \n"
        result = validate_text_input(text)
        assert result == "Hello World"


class TestCLICommands:
    """Test CLI command functionality."""
    
    @pytest.fixture
    def mock_pipeline(self):
        """Create a mock sentiment pipeline."""
        mock = Mock(spec=SentimentClassificationPipeline)
        mock.predict.return_value = {
            'sentiment_label': 'positive',
            'confidence_score': 0.8542,
            'processing_time_ms': 125.45,
            'input_text_length': 25,
            'model_confidence': [{'label': 'POSITIVE', 'score': 0.8542}]
        }
        mock.get_model_info.return_value = {
            'model_name': 'distilbert-base-uncased-finetuned-sst-2-english',
            'model_type': 'DistilBERT',
            'framework': 'PyTorch',
            'device': 'CPU',
            'status': 'initialized'
        }
        return mock
    
    @pytest.fixture
    def cli_runner(self):
        """Create a CLI runner for testing."""
        from click.testing import CliRunner
        return CliRunner()
    
    def test_cli_help(self, cli_runner):
        """Test CLI help command."""
        from apps.ml_pipeline.cli import cli
        
        result = cli_runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "Sentiment Analysis CLI" in result.output
        assert "analyze" in result.output
        assert "batch" in result.output
        assert "info" in result.output
    
    def test_cli_version(self, cli_runner):
        """Test CLI version command."""
        from apps.ml_pipeline.cli import cli
        
        result = cli_runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_analyze_command_success(self, mock_pipeline_class, cli_runner, mock_pipeline):
        """Test successful analyze command."""
        from apps.ml_pipeline.cli import cli
        
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['analyze', 'I love this product!'])
        assert result.exit_code == 0
        assert "POSITIVE" in result.output
        assert "0.8542" in result.output
        assert "125.45ms" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_analyze_command_no_text(self, mock_pipeline_class, cli_runner):
        """Test analyze command with no text provided."""
        from apps.ml_pipeline.cli import cli
        
        result = cli_runner.invoke(cli, ['analyze'])
        assert result.exit_code == 1
        assert "No text provided" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_analyze_command_invalid_text(self, mock_pipeline_class, cli_runner):
        """Test analyze command with invalid text."""
        from apps.ml_pipeline.cli import cli
        
        result = cli_runner.invoke(cli, ['analyze', ''])
        assert result.exit_code == 1
        assert "Text cannot be empty" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_analyze_command_detailed_output(self, mock_pipeline_class, cli_runner, mock_pipeline):
        """Test analyze command with detailed output format."""
        from apps.ml_pipeline.cli import cli
        
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['analyze', '--output-format', 'detailed', 'Great product!'])
        assert result.exit_code == 0
        assert "Sentiment Analysis Results" in result.output
        assert "Sentiment: positive" in result.output
        assert "Confidence: 0.8542" in result.output
        assert "Processing Time: 125.45ms" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_analyze_command_json_output(self, mock_pipeline_class, cli_runner, mock_pipeline):
        """Test analyze command with JSON output format."""
        from apps.ml_pipeline.cli import cli
        
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['analyze', '--output-format', 'json', 'Amazing!'])
        assert result.exit_code == 0
        assert '"sentiment_label": "positive"' in result.output
        assert '"confidence_score": 0.8542' in result.output
        assert '"processing_time_ms": 125.45' in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_analyze_command_no_color(self, mock_pipeline_class, cli_runner, mock_pipeline):
        """Test analyze command with color disabled."""
        from apps.ml_pipeline.cli import cli
        
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['analyze', '--no-color', 'Good product'])
        assert result.exit_code == 0
        assert "POSITIVE: 0.8542 (125.45ms)" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_analyze_command_custom_model(self, mock_pipeline_class, cli_runner, mock_pipeline):
        """Test analyze command with custom model."""
        from apps.ml_pipeline.cli import cli
        
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['analyze', '--model', 'roberta-base', 'Test text'])
        assert result.exit_code == 0
        mock_pipeline_class.assert_called_with('roberta-base')
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_info_command_success(self, mock_pipeline_class, cli_runner, mock_pipeline):
        """Test successful info command."""
        from apps.ml_pipeline.cli import cli
        
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['info'])
        assert result.exit_code == 0
        assert "Sentiment Analysis CLI - System Information" in result.output
        assert "Model: distilbert-base-uncased-finetuned-sst-2-english" in result.output
        assert "Type: DistilBERT" in result.output
        assert "Framework: PyTorch" in result.output
        assert "Device: CPU" in result.output
        assert "Status: initialized" in result.output


class TestCLIBatchProcessing:
    """Test CLI batch processing functionality."""
    
    @pytest.fixture
    def temp_input_file(self):
        """Create a temporary input file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("I love this product!\n")
            f.write("This is terrible.\n")
            f.write("It's okay, nothing special.\n")
            temp_file = f.name
        
        yield temp_file
        
        # Cleanup
        os.unlink(temp_file)
    
    @pytest.fixture
    def temp_output_file(self):
        """Create a temporary output file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        yield temp_file
        
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    @pytest.fixture
    def cli_runner(self):
        """Create a CLI runner for testing."""
        from click.testing import CliRunner
        return CliRunner()
    
    @pytest.fixture
    def mock_pipeline(self):
        """Create a mock sentiment pipeline."""
        mock = Mock(spec=SentimentClassificationPipeline)
        mock.predict.return_value = {
            'sentiment_label': 'positive',
            'confidence_score': 0.8542,
            'processing_time_ms': 125.45,
            'input_text_length': 20
        }
        mock.get_model_info.return_value = {
            'model_name': 'distilbert-base-uncased-finetuned-sst-2-english',
            'model_type': 'DistilBERT',
            'framework': 'PyTorch',
            'device': 'CPU',
            'status': 'initialized'
        }
        return mock
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_batch_command_success(self, mock_pipeline_class, cli_runner, temp_input_file, mock_pipeline):
        """Test successful batch command."""
        from apps.ml_pipeline.cli import cli
        
        # Mock pipeline to return different results for each text
        mock_pipeline.predict.side_effect = [
            {
                'sentiment_label': 'positive',
                'confidence_score': 0.8542,
                'processing_time_ms': 125.45,
                'input_text_length': 20
            },
            {
                'sentiment_label': 'negative',
                'confidence_score': 0.7234,
                'processing_time_ms': 98.12,
                'input_text_length': 18
            },
            {
                'sentiment_label': 'neutral',
                'confidence_score': 0.5123,
                'processing_time_ms': 87.65,
                'input_text_length': 25
            }
        ]
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['batch', temp_input_file])
        assert result.exit_code == 0
        assert "POSITIVE: 0.8542 (125.45ms)" in result.output
        assert "NEGATIVE: 0.7234 (98.12ms)" in result.output
        assert "NEUTRAL: 0.5123 (87.65ms)" in result.output
        assert "Summary: 3 texts processed" in result.output
        assert "Positive: 1, Negative: 1, Neutral: 1" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_batch_command_detailed_output(self, mock_pipeline_class, cli_runner, temp_input_file, mock_pipeline):
        """Test batch command with detailed output format."""
        from apps.ml_pipeline.cli import cli
        
        # Mock pipeline to return different results for each text
        mock_pipeline.predict.side_effect = [
            {
                'sentiment_label': 'positive',
                'confidence_score': 0.8542,
                'processing_time_ms': 125.45,
                'input_text_length': 20
            },
            {
                'sentiment_label': 'negative',
                'confidence_score': 0.7234,
                'processing_time_ms': 98.12,
                'input_text_length': 18
            },
            {
                'sentiment_label': 'neutral',
                'confidence_score': 0.5123,
                'processing_time_ms': 87.65,
                'input_text_length': 25
            }
        ]
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['batch', '--output-format', 'detailed', temp_input_file])
        assert result.exit_code == 0
        assert "Text 1: POSITIVE (confidence: 0.8542, time: 125.45ms)" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_batch_command_json_output(self, mock_pipeline_class, cli_runner, temp_input_file, mock_pipeline):
        """Test batch command with JSON output format."""
        from apps.ml_pipeline.cli import cli
        
        # Mock pipeline to return different results for each text
        mock_pipeline.predict.side_effect = [
            {
                'sentiment_label': 'positive',
                'confidence_score': 0.8542,
                'processing_time_ms': 125.45,
                'input_text_length': 20
            },
            {
                'sentiment_label': 'negative',
                'confidence_score': 0.7234,
                'processing_time_ms': 98.12,
                'input_text_length': 18
            },
            {
                'sentiment_label': 'neutral',
                'confidence_score': 0.5123,
                'processing_time_ms': 87.65,
                'input_text_length': 25
            }
        ]
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['batch', '--output-format', 'json', temp_input_file])
        assert result.exit_code == 0
        assert '"total_processed": 3' in result.output
        assert '"positive": 1' in result.output
        assert '"negative": 1' in result.output
        assert '"neutral": 1' in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_batch_command_output_file(self, mock_pipeline_class, cli_runner, temp_input_file, temp_output_file, mock_pipeline):
        """Test batch command with output file."""
        from apps.ml_pipeline.cli import cli
        
        mock_pipeline.predict.return_value = {
            'sentiment_label': 'positive',
            'confidence_score': 0.8542,
            'processing_time_ms': 125.45,
            'input_text_length': 20
        }
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['batch', '--output-file', temp_output_file, temp_input_file])
        assert result.exit_code == 0
        assert f"Results saved to {temp_output_file}" in result.output
        
        # Check output file contents
        with open(temp_output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "POSITIVE: 0.8542 (125.45ms)" in content
    
    def test_batch_command_file_not_found(self, cli_runner):
        """Test batch command with non-existent file."""
        from apps.ml_pipeline.cli import cli
        
        result = cli_runner.invoke(cli, ['batch', 'nonexistent.txt'])
        assert result.exit_code == 2  # Click error code for file not found
        assert "Path 'nonexistent.txt' does not exist" in result.output
    
    def test_batch_command_empty_file(self, cli_runner):
        """Test batch command with empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            from apps.ml_pipeline.cli import cli
            
            result = cli_runner.invoke(cli, ['batch', temp_file])
            assert result.exit_code == 1
            assert "File" in result.output
            assert "is empty" in result.output
        finally:
            os.unlink(temp_file)
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_batch_command_custom_delimiter(self, mock_pipeline_class, cli_runner, mock_pipeline):
        """Test batch command with custom delimiter."""
        from apps.ml_pipeline.cli import cli
        
        # Create file with comma delimiter
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("I love this product!,This is terrible.,It's okay")
            temp_file = f.name
        
        try:
            mock_pipeline.predict.return_value = {
                'sentiment_label': 'positive',
                'confidence_score': 0.8542,
                'processing_time_ms': 125.45,
                'input_text_length': 20
            }
            mock_pipeline_class.return_value = mock_pipeline
            
            result = cli_runner.invoke(cli, ['batch', '--delimiter', ',', temp_file])
            assert result.exit_code == 0
            assert "Summary: 3 texts processed" in result.output
        finally:
            os.unlink(temp_file)


class TestCLIErrorHandling:
    """Test CLI error handling and edge cases."""
    
    @pytest.fixture
    def cli_runner(self):
        """Create a CLI runner for testing."""
        from click.testing import CliRunner
        return CliRunner()
    
    @pytest.fixture
    def mock_pipeline(self):
        """Create a mock sentiment pipeline."""
        mock = Mock(spec=SentimentClassificationPipeline)
        mock.predict.return_value = {
            'sentiment_label': 'positive',
            'confidence_score': 0.8542,
            'processing_time_ms': 125.45,
            'input_text_length': 20
        }
        mock.get_model_info.return_value = {
            'model_name': 'distilbert-base-uncased-finetuned-sst-2-english',
            'model_type': 'DistilBERT',
            'framework': 'PyTorch',
            'device': 'CPU',
            'status': 'initialized'
        }
        return mock
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_pipeline_initialization_error(self, mock_pipeline_class, cli_runner):
        """Test CLI handles pipeline initialization errors."""
        from apps.ml_pipeline.cli import cli
        
        mock_pipeline_class.side_effect = RuntimeError("Model loading failed")
        
        result = cli_runner.invoke(cli, ['analyze', 'Test text'])
        assert result.exit_code == 1
        assert "Model loading failed" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_pipeline_prediction_error(self, mock_pipeline_class, cli_runner, mock_pipeline):
        """Test CLI handles pipeline prediction errors."""
        from apps.ml_pipeline.cli import cli
        
        mock_pipeline.predict.side_effect = Exception("Prediction failed")
        mock_pipeline_class.return_value = mock_pipeline
        
        result = cli_runner.invoke(cli, ['analyze', 'Test text'])
        assert result.exit_code == 1
        assert "Prediction failed" in result.output
    
    @patch('apps.ml_pipeline.cli.SentimentClassificationPipeline')
    def test_batch_partial_failure(self, mock_pipeline_class, cli_runner, mock_pipeline):
        """Test CLI handles partial batch processing failures."""
        from apps.ml_pipeline.cli import cli
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Good text\nBad text\nAnother good text")
            temp_file = f.name
        
        try:
            # Mock pipeline to fail on second text
            def mock_predict(text):
                if "Bad text" in text:
                    raise Exception("Processing failed")
                return {
                    'sentiment_label': 'positive',
                    'confidence_score': 0.8542,
                    'processing_time_ms': 125.45,
                    'input_text_length': len(text)
                }
            
            mock_pipeline.predict.side_effect = mock_predict
            mock_pipeline_class.return_value = mock_pipeline
            
            result = cli_runner.invoke(cli, ['batch', temp_file])
            assert result.exit_code == 0  # Should still succeed
            assert "Warning: Failed to process text 2" in result.output
            assert "Summary: 2 texts processed" in result.output
        finally:
            os.unlink(temp_file)
    
    def test_invalid_output_format(self, cli_runner):
        """Test CLI rejects invalid output format."""
        from apps.ml_pipeline.cli import cli
        
        result = cli_runner.invoke(cli, ['analyze', '--output-format', 'invalid', 'Test text'])
        assert result.exit_code == 2  # Click error code for invalid choice


class TestCLIIntegration:
    """Integration tests for CLI with actual sentiment pipeline."""
    
    @pytest.fixture
    def cli_runner(self):
        """Create a CLI runner for testing."""
        from click.testing import CliRunner
        return CliRunner()
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_cli_integration_with_real_pipeline(self, cli_runner):
        """Test CLI integration with actual sentiment pipeline (slow test)."""
        from apps.ml_pipeline.cli import cli
        
        # This test requires the actual ML model to be downloaded
        # It's marked as slow and integration test
        result = cli_runner.invoke(cli, ['analyze', 'I love this product!'])
        
        # Should either succeed or fail gracefully with model download message
        assert result.exit_code in [0, 1]
        if result.exit_code == 1:
            # Check if it's a model download issue
            assert any(msg in result.output.lower() for msg in 
                      ['model', 'download', 'huggingface', 'transformers'])


if __name__ == '__main__':
    pytest.main([__file__])
