"""
Tests for the StatisticsPanel Component

This module provides comprehensive testing for the statistics panel component
including unit tests for metrics calculation, chart rendering, and data processing.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.ui_components.statistics_panel import StatisticsPanel


class TestStatisticsPanel:
    """Test cases for the StatisticsPanel component."""
    
    def test_initialization(self):
        """Test component initialization."""
        component = StatisticsPanel()
        
        # Check that chart colors are initialized
        assert hasattr(component, 'chart_colors')
        assert 'primary' in component.chart_colors
        assert 'success' in component.chart_colors
        assert 'warning' in component.chart_colors
        assert 'danger' in component.chart_colors
    
    def test_render_empty_history(self):
        """Test rendering with empty prediction history."""
        component = StatisticsPanel()
        
        with patch('streamlit.info') as mock_info:
            component.render([])
            mock_info.assert_called_once_with("📊 No prediction data available yet. Start analyzing text to see statistics!")
    
    def test_render_with_history(self):
        """Test rendering with existing prediction history."""
        component = StatisticsPanel()
        
        # Create test data
        test_history = [
            {
                'id': 1,
                'timestamp': datetime.now(),
                'input_text': 'Positive text',
                'sentiment_label': 'positive',
                'confidence_score': 0.9,
                'processing_time_ms': 150.0,
                'model_confidence': [{'label': 'positive', 'score': 0.9}]
            },
            {
                'id': 2,
                'timestamp': datetime.now() - timedelta(hours=1),
                'input_text': 'Negative text',
                'sentiment_label': 'negative',
                'confidence_score': 0.7,
                'processing_time_ms': 200.0,
                'model_confidence': [{'label': 'negative', 'score': 0.7}]
            }
        ]
        
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.columns') as mock_columns:
            
            # Mock tabs to return context managers
            mock_tab1 = Mock()
            mock_tab1.__enter__ = Mock(return_value=mock_tab1)
            mock_tab1.__exit__ = Mock(return_value=None)
            
            mock_tab2 = Mock()
            mock_tab2.__enter__ = Mock(return_value=mock_tab2)
            mock_tab2.__exit__ = Mock(return_value=None)
            
            mock_tab3 = Mock()
            mock_tab3.__enter__ = Mock(return_value=mock_tab3)
            mock_tab3.__exit__ = Mock(return_value=None)
            
            mock_tab4 = Mock()
            mock_tab4.__enter__ = Mock(return_value=mock_tab4)
            mock_tab4.__exit__ = Mock(return_value=None)
            
            mock_tabs.return_value = [mock_tab1, mock_tab2, mock_tab3, mock_tab4]
            
            # Mock columns to return context managers
            def create_mock_column():
                mock_col = Mock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=None)
                return mock_col
            
            # Provide enough columns for all calls: 2, 5, 2, 4, 3, 2, 2, variable
            mock_columns.side_effect = [
                [create_mock_column(), create_mock_column()],  # 2 columns
                [create_mock_column(), create_mock_column(), create_mock_column(), create_mock_column(), create_mock_column()],  # 5 columns
                [create_mock_column(), create_mock_column()],  # 2 columns
                [create_mock_column(), create_mock_column(), create_mock_column(), create_mock_column()],  # 4 columns
                [create_mock_column(), create_mock_column(), create_mock_column()],  # 3 columns
                [create_mock_column(), create_mock_column()],  # 2 columns
                [create_mock_column(), create_mock_column()],  # 2 columns
                [create_mock_column(), create_mock_column()]   # 2 columns (for variable length)
            ]
            
            component.render(test_history)
            
            # Should call markdown for header
            assert mock_markdown.call_count >= 1
    
    def test_overview_metrics_calculation(self):
        """Test overview metrics calculation."""
        component = StatisticsPanel()
        
        # Create test data
        test_history = [
            {
                'confidence_score': 0.9,
                'processing_time_ms': 150.0,
                'sentiment_label': 'positive'
            },
            {
                'confidence_score': 0.7,
                'processing_time_ms': 200.0,
                'sentiment_label': 'negative'
            },
            {
                'confidence_score': 0.8,
                'processing_time_ms': 175.0,
                'sentiment_label': 'positive'
            }
        ]
        
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.columns') as mock_columns:
            
            # Mock columns to return context managers
            def create_mock_column():
                mock_col = Mock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=None)
                return mock_col
            
            # Provide enough columns for all calls in this method: 2, 5
            mock_columns.side_effect = [
                [create_mock_column(), create_mock_column()],  # 2 columns
                [create_mock_column(), create_mock_column(), create_mock_column(), create_mock_column(), create_mock_column()]  # 5 columns
            ]
            
            # Mock helper methods
            with patch.object(component, '_get_recent_count', return_value=2), \
                 patch.object(component, '_get_confidence_trend', return_value=5.0):
                
                component._render_overview_metrics(test_history)
                
                # Should call metric for total predictions, average confidence, etc.
                assert mock_metric.call_count >= 3
    
    def test_confidence_distribution_rendering(self):
        """Test confidence distribution chart rendering."""
        component = StatisticsPanel()
        
        # Create test data
        test_history = [
            {'confidence_score': 0.95},  # Very High
            {'confidence_score': 0.80},  # High
            {'confidence_score': 0.65},  # Medium
            {'confidence_score': 0.45},  # Low
            {'confidence_score': 0.25}   # Very Low
        ]
        
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.plotly_chart') as mock_plotly:
            
            # Mock columns to return context managers
            def create_mock_column():
                mock_col = Mock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=None)
                return mock_col
            
            # Provide enough columns for all calls in this method: 2, 4, 3
            mock_columns.side_effect = [
                [create_mock_column(), create_mock_column()],  # 2 columns
                [create_mock_column(), create_mock_column(), create_mock_column(), create_mock_column()],  # 4 columns
                [create_mock_column(), create_mock_column(), create_mock_column()]  # 3 columns
            ]
            
            component._render_confidence_distribution(test_history)
            
            # Should create plotly charts
            assert mock_plotly.call_count >= 1
    
    def test_performance_trends_rendering(self):
        """Test performance trends chart rendering."""
        component = StatisticsPanel()
        
        # Create test data with timestamps
        now = datetime.now()
        test_history = [
            {
                'timestamp': now,
                'confidence_score': 0.9,
                'processing_time_ms': 150.0
            },
            {
                'timestamp': now - timedelta(hours=1),
                'confidence_score': 0.8,
                'processing_time_ms': 200.0
            },
            {
                'timestamp': now - timedelta(hours=2),
                'confidence_score': 0.7,
                'processing_time_ms': 250.0
            }
        ]
        
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.plotly_chart') as mock_plotly:
            
            component._render_performance_trends(test_history)
            
            # Should create plotly charts
            assert mock_plotly.call_count >= 1
    
    def test_sentiment_analysis_rendering(self):
        """Test sentiment analysis chart rendering."""
        component = StatisticsPanel()
        
        # Create test data
        test_history = [
            {'sentiment_label': 'positive', 'confidence_score': 0.9},
            {'sentiment_label': 'negative', 'confidence_score': 0.7},
            {'sentiment_label': 'positive', 'confidence_score': 0.8},
            {'sentiment_label': 'neutral', 'confidence_score': 0.6}
        ]
        
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.plotly_chart') as mock_plotly:
            
            # Mock columns to return context managers
            def create_mock_column():
                mock_col = Mock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=None)
                return mock_col
            
            # Mock columns to always return a list that supports indexing
            def mock_columns_side_effect(num_cols):
                return [create_mock_column() for _ in range(num_cols)]
            
            mock_columns.side_effect = mock_columns_side_effect
            
            component._render_sentiment_analysis(test_history)
            
            # Should create plotly charts
            assert mock_plotly.call_count >= 1
    
    def test_get_recent_count(self):
        """Test recent count calculation."""
        component = StatisticsPanel()
        
        # Create test data with timestamps
        now = datetime.now()
        test_history = [
            {'timestamp': now},  # Recent (within 24h)
            {'timestamp': now - timedelta(hours=12)},  # Recent (within 24h)
            {'timestamp': now - timedelta(days=2)},  # Old (more than 24h)
            {'timestamp': now - timedelta(days=3)}   # Old (more than 24h)
        ]
        
        recent_count = component._get_recent_count(test_history, 1)
        assert recent_count == 2
    
    def test_get_confidence_trend(self):
        """Test confidence trend calculation."""
        component = StatisticsPanel()
        
        # Create test data with timestamps
        now = datetime.now()
        test_history = [
            {
                'timestamp': now,
                'confidence_score': 0.9
            },
            {
                'timestamp': now - timedelta(hours=1),
                'confidence_score': 0.8
            },
            {
                'timestamp': now - timedelta(hours=2),
                'confidence_score': 0.7
            }
        ]
        
        trend = component._get_confidence_trend(test_history)
        # Should return a trend value (positive or negative)
        assert isinstance(trend, (int, float))
    
    def test_get_processing_time_trend(self):
        """Test processing time trend calculation."""
        component = StatisticsPanel()
        
        # Create test data with timestamps
        now = datetime.now()
        test_history = [
            {
                'timestamp': now,
                'processing_time_ms': 150.0
            },
            {
                'timestamp': now - timedelta(hours=1),
                'processing_time_ms': 200.0
            },
            {
                'timestamp': now - timedelta(hours=2),
                'processing_time_ms': 250.0
            }
        ]
        
        trend = component._get_processing_time_trend(test_history)
        # Should return a trend value (positive or negative)
        assert isinstance(trend, (int, float))
    
    def test_component_integration(self):
        """Test full component integration."""
        component = StatisticsPanel()
        
        # Create comprehensive test data
        now = datetime.now()
        test_history = [
            {
                'id': 1,
                'timestamp': now,
                'input_text': 'Positive text',
                'sentiment_label': 'positive',
                'confidence_score': 0.9,
                'processing_time_ms': 150.0,
                'model_confidence': [{'label': 'positive', 'score': 0.9}]
            },
            {
                'id': 2,
                'timestamp': now - timedelta(hours=1),
                'input_text': 'Negative text',
                'sentiment_label': 'negative',
                'confidence_score': 0.7,
                'processing_time_ms': 200.0,
                'model_confidence': [{'label': 'negative', 'score': 0.7}]
            },
            {
                'id': 3,
                'timestamp': now - timedelta(hours=2),
                'input_text': 'Neutral text',
                'sentiment_label': 'neutral',
                'confidence_score': 0.6,
                'processing_time_ms': 180.0,
                'model_confidence': [{'label': 'neutral', 'score': 0.6}]
            }
        ]
        
        # Mock all streamlit components
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.plotly_chart') as mock_plotly:
            
            # Mock tabs
            mock_tabs_list = []
            for i in range(4):
                mock_tab = Mock()
                mock_tab.__enter__ = Mock(return_value=mock_tab)
                mock_tab.__exit__ = Mock(return_value=None)
                mock_tabs_list.append(mock_tab)
            
            mock_tabs.return_value = mock_tabs_list
            
                        # Mock columns to return context managers
            def create_mock_column():
                mock_col = Mock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=None)
                return mock_col
            
            # Mock columns to always return a list that supports indexing
            def mock_columns_side_effect(num_cols):
                return [create_mock_column() for _ in range(num_cols)]
            
            mock_columns.side_effect = mock_columns_side_effect
            
            # Render the component
            component.render(test_history)
            
            # Verify all major components were called
            assert mock_markdown.call_count >= 1
            assert mock_tabs.call_count == 1
            assert mock_columns.call_count >= 4  # Multiple column calls in different methods
            assert mock_metric.call_count >= 3   # At least 3 metrics in overview
            assert mock_plotly.call_count >= 4   # Charts in each tab


if __name__ == "__main__":
    pytest.main([__file__])
