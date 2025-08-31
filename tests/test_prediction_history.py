"""
Tests for the PredictionHistory Component

This module provides comprehensive testing for the prediction history component
including unit tests for session state management, filtering, and export functionality.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.ui_components.prediction_history import PredictionHistory


def create_mock_session_state(**kwargs):
    """Helper function to create a mock session state object."""
    mock_session = Mock()
    mock_session.__getitem__ = Mock(side_effect=lambda key: getattr(mock_session, key))
    mock_session.__setitem__ = Mock(side_effect=lambda key, value: setattr(mock_session, key, value))
    mock_session.__contains__ = Mock(side_effect=lambda key: hasattr(mock_session, key))
    
    # Set up the initial attributes with default values
    mock_session.prediction_history = kwargs.get('prediction_history', [])
    mock_session.history_filters = kwargs.get('history_filters', {
        'search_term': '',
        'sentiment_filter': 'all',
        'confidence_threshold': 0.0,
        'date_range': 'all'
    })
    
    # Set any additional attributes
    for key, value in kwargs.items():
        if key not in ['prediction_history', 'history_filters']:
            setattr(mock_session, key, value)
    
    return mock_session


class TestPredictionHistory:
    """Test cases for the PredictionHistory component."""
    
    def test_initialization(self):
        """Test component initialization."""
        component = PredictionHistory()
        
        # Check that session state is initialized
        assert hasattr(component, 'initialize_session_state')
    
    def test_initialize_session_state(self):
        """Test session state initialization."""
        component = PredictionHistory()
        
        # Mock streamlit session state
        mock_session = create_mock_session_state()
        
        with patch('streamlit.session_state', mock_session):
            component.initialize_session_state()
            
            # Check that session state is properly initialized
            assert hasattr(mock_session, 'prediction_history')
            assert hasattr(mock_session, 'history_filters')
            assert mock_session.prediction_history == []
            assert mock_session.history_filters['search_term'] == ''
            assert mock_session.history_filters['sentiment_filter'] == 'all'
            assert mock_session.history_filters['confidence_threshold'] == 0.0
            assert mock_session.history_filters['date_range'] == 'all'
    
    def test_add_prediction(self):
        """Test adding a new prediction to history."""
        component = PredictionHistory()
        
        # Mock streamlit session state
        mock_session = create_mock_session_state(prediction_history=[])
        with patch('streamlit.session_state', mock_session):
            # Mock datetime
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 0)
                
                result = {
                    'sentiment_label': 'positive',
                    'confidence_score': 0.85,
                    'processing_time_ms': 150.0,
                    'model_confidence': [{'label': 'positive', 'score': 0.85}]
                }
                
                component.add_prediction("This is a test", result, {'length': 18})
                
                # Check that prediction was added
                assert len(mock_session.prediction_history) == 1
                prediction = mock_session.prediction_history[0]
                
                assert prediction['id'] == 1
                assert prediction['input_text'] == "This is a test"
                assert prediction['sentiment_label'] == 'positive'
                assert prediction['confidence_score'] == 0.85
                assert prediction['processing_time_ms'] == 150.0
                assert prediction['metadata']['length'] == 18
    
    def test_add_prediction_history_limit(self):
        """Test that prediction history is limited to 50 entries."""
        component = PredictionHistory()
        
        # Mock streamlit session state with 50 existing predictions
        existing_history = [{'id': i} for i in range(1, 51)]
        mock_session = create_mock_session_state(prediction_history=existing_history)
        with patch('streamlit.session_state', mock_session):
            # Mock datetime
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 0)
                
                result = {'sentiment_label': 'positive', 'confidence_score': 0.85, 'processing_time_ms': 150.0}
                
                component.add_prediction("New prediction", result)
                
                # Check that oldest prediction was removed and new one added
                assert len(mock_session.prediction_history) == 50
                assert mock_session.prediction_history[0]['id'] == 2  # Oldest (id=1) was removed
                assert mock_session.prediction_history[-1]['id'] == 51  # Newest
    
    def test_render_empty_history(self):
        """Test rendering with empty prediction history."""
        component = PredictionHistory()
        
        # Mock streamlit session state with empty history
        mock_session = create_mock_session_state(prediction_history=[])
        with patch('streamlit.session_state', mock_session), \
             patch('streamlit.info') as mock_info:
            
            component.render()
            mock_info.assert_called_once_with("📚 No prediction history yet. Start analyzing text to build your history!")
    
    def test_render_with_history(self):
        """Test rendering with existing prediction history."""
        component = PredictionHistory()
        
        # Mock streamlit session state with some history
        mock_session = create_mock_session_state(
            prediction_history=[
                {
                    'id': 1,
                    'timestamp': datetime(2024, 1, 15, 10, 30, 0),
                    'input_text': 'Test text',
                    'sentiment_label': 'positive',
                    'confidence_score': 0.85,
                    'processing_time_ms': 150.0
                }
            ],
            history_filters={
                'search_term': '',
                'sentiment_filter': 'all',
                'confidence_threshold': 0.0,
                'date_range': 'all'
            }
        )
        
        with patch('streamlit.session_state', mock_session), \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.text_input') as mock_text_input, \
             patch('streamlit.selectbox') as mock_selectbox, \
             patch('streamlit.slider') as mock_slider, \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.expander') as mock_expander:
            
            # Mock return values
            mock_text_input.return_value = ''
            mock_selectbox.side_effect = ['all', 'all']
            mock_slider.return_value = 0.0
            mock_button.return_value = False
            
            # Create mock columns that support context manager protocol
            def create_mock_column():
                mock_col = Mock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=None)
                return mock_col
            
            mock_columns.side_effect = [
                [create_mock_column(), create_mock_column(), create_mock_column()],  # For filters (3 columns)
                [create_mock_column(), create_mock_column()],  # For date range (2 columns)
                [create_mock_column(), create_mock_column(), create_mock_column(), create_mock_column()],  # For summary (4 columns)
                [create_mock_column(), create_mock_column()],  # For prediction detail (2 columns)
                [create_mock_column(), create_mock_column()]   # For export (2 columns)
            ]
            mock_expander.return_value.__enter__ = Mock()
            mock_expander.return_value.__exit__ = Mock()
            
            component.render()
            
            # Should call markdown for headers
            assert mock_markdown.call_count >= 1
    
    def test_get_filtered_history(self):
        """Test filtering of prediction history."""
        component = PredictionHistory()
        
        # Create test data
        test_history = [
            {
                'id': 1,
                'timestamp': datetime(2024, 1, 15, 10, 30, 0),
                'input_text': 'Positive text',
                'sentiment_label': 'positive',
                'confidence_score': 0.9,
                'processing_time_ms': 150.0
            },
            {
                'id': 2,
                'timestamp': datetime(2024, 1, 15, 11, 30, 0),
                'input_text': 'Negative text',
                'sentiment_label': 'negative',
                'confidence_score': 0.7,
                'processing_time_ms': 200.0
            }
        ]
        
        # Test search filter
        mock_session = create_mock_session_state(
            prediction_history=test_history,
            history_filters={
                'search_term': 'Positive',
                'sentiment_filter': 'all',
                'confidence_threshold': 0.0,
                'date_range': 'all'
            }
        )
        with patch('streamlit.session_state', mock_session):
            filtered = component._get_filtered_history()
            assert len(filtered) == 1
            assert filtered[0]['input_text'] == 'Positive text'
        
        # Test sentiment filter
        mock_session = create_mock_session_state(
            prediction_history=test_history,
            history_filters={
                'search_term': '',
                'sentiment_filter': 'negative',
                'confidence_threshold': 0.0,
                'date_range': 'all'
            }
        )
        with patch('streamlit.session_state', mock_session):
            filtered = component._get_filtered_history()
            assert len(filtered) == 1
            assert filtered[0]['sentiment_label'] == 'negative'
        
        # Test confidence threshold filter
        mock_session = create_mock_session_state(
            prediction_history=test_history,
            history_filters={
                'search_term': '',
                'sentiment_filter': 'all',
                'confidence_threshold': 0.8,
                'date_range': 'all'
            }
        )
        with patch('streamlit.session_state', mock_session):
            filtered = component._get_filtered_history()
            assert len(filtered) == 1
            assert filtered[0]['confidence_score'] == 0.9
    
    def test_export_functionality(self):
        """Test export functionality."""
        component = PredictionHistory()
        
        # Mock streamlit session state
        test_history = [
            {
                'id': 1,
                'timestamp': datetime(2024, 1, 15, 10, 30, 0),
                'input_text': 'Test text',
                'sentiment_label': 'positive',
                'confidence_score': 0.85,
                'processing_time_ms': 150.0
            }
        ]
        
        mock_session = create_mock_session_state(
            prediction_history=test_history,
            history_filters={
                'search_term': '',
                'sentiment_filter': 'all',
                'confidence_threshold': 0.0,
                'date_range': 'all'
            }
        )
        with patch('streamlit.session_state', mock_session), \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.button') as mock_button, \
             patch('pandas.DataFrame') as mock_dataframe, \
             patch('streamlit.download_button') as mock_download:
            
            mock_button.return_value = True
            mock_dataframe.return_value.to_csv.return_value = "csv_data"
            
            # Test CSV export
            component._export_to_csv(test_history)
            
            # Should create download button
            mock_download.assert_called_once()
    
    def test_get_history_stats(self):
        """Test history statistics calculation."""
        component = PredictionHistory()
        
        # Mock streamlit session state with test data
        test_history = [
            {
                'id': 1,
                'timestamp': datetime(2024, 1, 15, 10, 30, 0),
                'input_text': 'Positive text',
                'sentiment_label': 'positive',
                'confidence_score': 0.9,
                'processing_time_ms': 100.0
            },
            {
                'id': 2,
                'timestamp': datetime(2024, 1, 15, 11, 30, 0),
                'input_text': 'Negative text',
                'sentiment_label': 'negative',
                'confidence_score': 0.7,
                'processing_time_ms': 200.0
            }
        ]
        
        mock_session = create_mock_session_state(prediction_history=test_history)
        with patch('streamlit.session_state', mock_session):
            stats = component.get_history_stats()
            
            assert stats['total_predictions'] == 2
            assert stats['average_confidence'] == 0.8
            assert stats['average_processing_time'] == 150.0
            assert stats['sentiment_distribution']['positive'] == 1
            assert stats['sentiment_distribution']['negative'] == 1
    
    def test_get_history_stats_empty(self):
        """Test history statistics with empty history."""
        component = PredictionHistory()
        
        # Mock streamlit session state with empty history
        mock_session = create_mock_session_state(prediction_history=[])
        with patch('streamlit.session_state', mock_session):
            stats = component.get_history_stats()
            
            assert stats['total_predictions'] == 0
            assert stats['average_confidence'] == 0.0
            assert stats['average_processing_time'] == 0.0
            assert stats['sentiment_distribution'] == {}
    
    def test_date_range_filtering(self):
        """Test date range filtering functionality."""
        component = PredictionHistory()
        
        # Create test data with different timestamps
        from datetime import datetime, timedelta
        now = datetime.now()
        recent_date = now
        old_date = now - timedelta(days=10)  # More than 7 days ago
        
        test_history = [
            {
                'id': 1,
                'timestamp': recent_date,
                'input_text': 'Recent text',
                'sentiment_label': 'positive',
                'confidence_score': 0.9,
                'processing_time_ms': 150.0
            },
            {
                'id': 2,
                'timestamp': old_date,  # More than 7 days ago
                'input_text': 'Old text',
                'sentiment_label': 'negative',
                'confidence_score': 0.7,
                'processing_time_ms': 200.0
            }
        ]
        
        # Test last 7 days filter
        mock_session = create_mock_session_state(
            prediction_history=test_history,
            history_filters={
                'search_term': '',
                'sentiment_filter': 'all',
                'confidence_threshold': 0.0,
                'date_range': 'last_7_days'
            }
        )
        with patch('streamlit.session_state', mock_session):
            filtered = component._get_filtered_history()
            assert len(filtered) == 1
            assert filtered[0]['input_text'] == 'Recent text'
    
    def test_component_integration(self):
        """Test full component integration."""
        component = PredictionHistory()
        
        # Create comprehensive test data
        test_history = [
            {
                'id': 1,
                'timestamp': datetime(2024, 1, 15, 10, 30, 0),
                'input_text': 'Positive text',
                'sentiment_label': 'positive',
                'confidence_score': 0.9,
                'processing_time_ms': 150.0,
                'model_confidence': [{'label': 'positive', 'score': 0.9}]
            }
        ]
        
        # Mock all streamlit components
        mock_session = create_mock_session_state(
            prediction_history=test_history,
            history_filters={
                'search_term': '',
                'sentiment_filter': 'all',
                'confidence_threshold': 0.0,
                'date_range': 'all'
            }
        )
        with patch('streamlit.session_state', mock_session), \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.text_input') as mock_text_input, \
             patch('streamlit.selectbox') as mock_selectbox, \
             patch('streamlit.slider') as mock_slider, \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.expander') as mock_expander, \
             patch('streamlit.dataframe') as mock_dataframe:
            
            # Mock return values
            mock_text_input.return_value = ''
            mock_selectbox.side_effect = ['all', 'all']
            mock_slider.return_value = 0.0
            mock_button.return_value = False
            
            # Create mock columns that support context manager protocol
            def create_mock_column():
                mock_col = Mock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=None)
                return mock_col
            
            mock_columns.side_effect = [
                [create_mock_column(), create_mock_column(), create_mock_column()],  # For filters (3 columns)
                [create_mock_column(), create_mock_column()],  # For date range (2 columns)
                [create_mock_column(), create_mock_column(), create_mock_column(), create_mock_column()],  # For summary (4 columns)
                [create_mock_column(), create_mock_column()],  # For prediction detail (2 columns)
                [create_mock_column(), create_mock_column()]   # For export (2 columns)
            ]
            mock_expander.return_value.__enter__ = Mock()
            mock_expander.return_value.__exit__ = Mock()
            mock_dataframe.return_value = Mock()
            
            # Render the component
            component.render()
            
            # Verify all major components were called
            assert mock_markdown.call_count >= 1
            mock_text_input.assert_called_once()
            assert mock_selectbox.call_count >= 2
            mock_slider.assert_called_once()
            assert mock_metric.call_count >= 4  # 4 metrics in summary


if __name__ == "__main__":
    pytest.main([__file__])
