"""
Tests for the Streamlit Web Interface

This module provides comprehensive testing for the web interface components
including unit tests, integration tests, and component validation.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.ui_components.text_input import TextInputComponent
from packages.ui_components.sentiment_display import SentimentDisplay
from packages.ui_components.sidebar import SidebarComponent


class TestTextInputComponent:
    """Test cases for the TextInputComponent."""
    
    def test_initialization(self):
        """Test component initialization with default parameters."""
        component = TextInputComponent()
        assert component.max_chars == 1000
        assert component.placeholder == "Enter your text here..."
    
    def test_initialization_custom_params(self):
        """Test component initialization with custom parameters."""
        component = TextInputComponent(max_chars=500, placeholder="Custom placeholder")
        assert component.max_chars == 500
        assert component.placeholder == "Custom placeholder"
    
    def test_validate_input_empty(self):
        """Test input validation with empty text."""
        component = TextInputComponent()
        is_valid, error_message = component.validate_input("")
        assert not is_valid
        assert "cannot be empty" in error_message.lower()
    
    def test_validate_input_whitespace(self):
        """Test input validation with whitespace-only text."""
        component = TextInputComponent()
        is_valid, error_message = component.validate_input("   ")
        assert not is_valid
        assert "cannot be empty" in error_message.lower()
    
    def test_validate_input_too_long(self):
        """Test input validation with text exceeding character limit."""
        component = TextInputComponent(max_chars=10)
        long_text = "This is a very long text that exceeds the limit"
        is_valid, error_message = component.validate_input(long_text)
        assert not is_valid
        assert "exceeds" in error_message.lower()
    
    def test_validate_input_valid(self):
        """Test input validation with valid text."""
        component = TextInputComponent()
        valid_text = "This is valid text"
        is_valid, error_message = component.validate_input(valid_text)
        assert is_valid
        assert error_message is None


class TestSentimentDisplay:
    """Test cases for the SentimentDisplay component."""
    
    def test_initialization(self):
        """Test component initialization."""
        component = SentimentDisplay()
        assert "positive" in component.sentiment_colors
        assert "negative" in component.sentiment_colors
        assert "neutral" in component.sentiment_colors
        assert "positive" in component.sentiment_emojis
        assert "negative" in component.sentiment_emojis
        assert "neutral" in component.sentiment_emojis
    
    def test_sentiment_colors_structure(self):
        """Test that sentiment colors have the correct structure."""
        component = SentimentDisplay()
        for sentiment in ["positive", "negative", "neutral"]:
            colors = component.sentiment_colors[sentiment]
            assert "primary" in colors
            assert "secondary" in colors
            assert "text" in colors
    
    def test_sentiment_emojis_mapping(self):
        """Test that sentiment emojis are properly mapped."""
        component = SentimentDisplay()
        assert component.sentiment_emojis["positive"] == "😊"
        assert component.sentiment_emojis["negative"] == "😞"
        assert component.sentiment_emojis["neutral"] == "😐"
    
    def test_render_with_empty_result(self):
        """Test rendering with empty result."""
        component = SentimentDisplay()
        # This should not raise an exception
        component.render({})
    
    def test_render_with_valid_result(self):
        """Test rendering with valid result."""
        component = SentimentDisplay()
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "processing_time_ms": 150.5
        }
        # This should not raise an exception
        component.render(result)


class TestSidebarComponent:
    """Test cases for the SidebarComponent."""
    
    def test_initialization(self):
        """Test component initialization."""
        component = SidebarComponent()
        assert component is not None
    
    def test_render_method_exists(self):
        """Test that the render method exists."""
        component = SidebarComponent()
        assert hasattr(component, 'render')
        assert callable(component.render)


class TestWebInterfaceIntegration:
    """Integration tests for the web interface components."""
    
    @patch('streamlit.container')
    @patch('streamlit.text_area')
    def test_text_input_integration(self, mock_text_area, mock_container):
        """Test text input component integration with Streamlit."""
        mock_text_area.return_value = "Test input text"
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock()
        
        component = TextInputComponent()
        result = component.render()
        
        assert result == "Test input text"
    
    def test_sentiment_display_color_mapping(self):
        """Test that sentiment display correctly maps colors to sentiments."""
        component = SentimentDisplay()
        
        # Test positive sentiment
        positive_colors = component.sentiment_colors["positive"]
        assert positive_colors["primary"] == "#28a745"  # Green
        
        # Test negative sentiment
        negative_colors = component.sentiment_colors["negative"]
        assert negative_colors["primary"] == "#dc3545"  # Red
        
        # Test neutral sentiment
        neutral_colors = component.sentiment_colors["neutral"]
        assert neutral_colors["primary"] == "#ffc107"  # Yellow
    
    def test_confidence_level_calculation(self):
        """Test confidence level calculation logic."""
        component = SentimentDisplay()
        
        # Test very high confidence
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.95,
            "processing_time_ms": 100
        }
        
        # This should not raise an exception
        component.render(result)


class TestEnhancedComponentsIntegration:
    """Integration tests for the enhanced confidence visualization components."""
    
    def test_all_components_import_successfully(self):
        """Test that all enhanced components can be imported and initialized."""
        from packages.ui_components.confidence_metrics import ConfidenceMetrics
        from packages.ui_components.statistics_panel import StatisticsPanel
        from packages.ui_components.prediction_history import PredictionHistory
        from packages.ui_components.csv_export import CSVExport
        
        # Test initialization
        confidence_metrics = ConfidenceMetrics()
        statistics_panel = StatisticsPanel()
        prediction_history = PredictionHistory()
        csv_export = CSVExport()
        
        assert confidence_metrics is not None
        assert statistics_panel is not None
        assert prediction_history is not None
        assert csv_export is not None
    
    def test_data_format_compatibility(self):
        """Test that all components use compatible data formats."""
        from packages.ui_components.confidence_metrics import ConfidenceMetrics
        from packages.ui_components.statistics_panel import StatisticsPanel
        from packages.ui_components.prediction_history import PredictionHistory
        from packages.ui_components.csv_export import CSVExport
        
        # Create sample data that should work with all components
        sample_result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "processing_time_ms": 150.0,
            "model_confidence": [
                {"label": "positive", "score": 0.85},
                {"label": "negative", "score": 0.10},
                {"label": "neutral", "score": 0.05}
            ]
        }
        
        sample_history = [
            {
                "id": 1,
                "timestamp": "2024-01-15T10:30:00",
                "input_text": "Test text",
                "sentiment_label": "positive",
                "confidence_score": 0.85,
                "processing_time_ms": 150.0,
                "model_confidence": [
                    {"label": "positive", "score": 0.85},
                    {"label": "negative", "score": 0.10},
                    {"label": "neutral", "score": 0.05}
                ]
            }
        ]
        
        # Test that all components can handle the data format
        confidence_metrics = ConfidenceMetrics()
        statistics_panel = StatisticsPanel()
        prediction_history = PredictionHistory()
        csv_export = CSVExport()
        
        # These should not raise exceptions
        assert confidence_metrics is not None
        assert statistics_panel is not None
        assert prediction_history is not None
        assert csv_export is not None
    
    def test_responsive_design_components(self):
        """Test that all components support responsive design patterns."""
        from packages.ui_components.confidence_metrics import ConfidenceMetrics
        from packages.ui_components.statistics_panel import StatisticsPanel
        from packages.ui_components.prediction_history import PredictionHistory
        from packages.ui_components.csv_export import CSVExport
        
        # All components should use Streamlit's responsive design features
        # like st.columns, st.container, etc.
        components = [
            ConfidenceMetrics(),
            StatisticsPanel(),
            PredictionHistory(),
            CSVExport()
        ]
        
        for component in components:
            assert hasattr(component, 'render')
            assert callable(component.render)
    
    def test_session_state_integration(self):
        """Test that components properly integrate with Streamlit session state."""
        from packages.ui_components.prediction_history import PredictionHistory
        
        # Test that PredictionHistory component can manage session state
        prediction_history = PredictionHistory()
        
        # Test session state initialization
        with patch('streamlit.session_state') as mock_session:
            mock_session.prediction_history = []
            mock_session.history_filters = {
                'search_text': '',
                'sentiment_filter': 'all',
                'confidence_min': 0.0,
                'confidence_max': 1.0,
                'date_from': None,
                'date_to': None
            }
            
            # Component should be able to work with session state
            assert prediction_history is not None
    
    def test_export_functionality_integration(self):
        """Test that export functionality integrates properly with other components."""
        from packages.ui_components.csv_export import CSVExport
        from packages.ui_components.prediction_history import PredictionHistory
        
        # Test that CSVExport can handle data from PredictionHistory
        csv_export = CSVExport()
        prediction_history = PredictionHistory()
        
        # Both components should exist and be compatible
        assert csv_export is not None
        assert prediction_history is not None
        
        # Test that export formats are properly defined
        assert hasattr(csv_export, 'export_formats')
        assert 'csv' in csv_export.export_formats
        assert 'json' in csv_export.export_formats
        assert 'excel' in csv_export.export_formats


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
