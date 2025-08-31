"""
Prediction History Component

This module provides prediction history tracking with session state management,
timestamp tracking, and filtering/search capabilities.
"""

import streamlit as st
from typing import Dict, Any, List
from datetime import datetime
import pandas as pd

class PredictionHistory:
    """
    Component for tracking and displaying prediction history.
    
    Features:
    - Session state management for prediction history
    - Prediction history display with scrollable list
    - Timestamp tracking for each prediction
    - History filtering and search capabilities
    - Export functionality for historical data
    """
    
    def __init__(self):
        """Initialize the prediction history component."""
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state for prediction history."""
        if 'prediction_history' not in st.session_state:
            st.session_state.prediction_history = []
        
        if 'history_filters' not in st.session_state:
            st.session_state.history_filters = {
                'search_term': '',
                'sentiment_filter': 'all',
                'confidence_threshold': 0.0,
                'date_range': 'all'
            }
    
    def add_prediction(self, input_text: str, result: Dict[str, Any], metadata: Dict[str, Any] = None):
        """
        Add a new prediction to the history.
        
        Args:
            input_text: The input text that was analyzed
            result: The sentiment analysis result
            metadata: Additional metadata about the prediction
        """
        prediction_entry = {
            'id': len(st.session_state.prediction_history) + 1,
            'timestamp': datetime.now(),
            'input_text': input_text,
            'sentiment_label': result.get('sentiment_label', 'unknown'),
            'confidence_score': result.get('confidence_score', 0.0),
            'processing_time_ms': result.get('processing_time_ms', 0.0),
            'model_confidence': result.get('model_confidence', []),
            'metadata': metadata or {}
        }
        
        st.session_state.prediction_history.append(prediction_entry)
        
        # Keep only last 50 predictions to manage memory
        if len(st.session_state.prediction_history) > 50:
            st.session_state.prediction_history.pop(0)
    
    def render(self) -> None:
        """Render the prediction history component."""
        if not st.session_state.prediction_history:
            st.info("📚 No prediction history yet. Start analyzing text to build your history!")
            return
        
        st.markdown("## 📚 Prediction History")
        
        # Render filters
        self._render_filters()
        
        # Get filtered history
        filtered_history = self._get_filtered_history()
        
        if not filtered_history:
            st.warning("🔍 No predictions match your current filters. Try adjusting the search criteria.")
            return
        
        # Render history summary
        self._render_history_summary(filtered_history)
        
        # Render history list
        self._render_history_list(filtered_history)
        
        # Export functionality
        self._render_export_section(filtered_history)
    
    def _render_filters(self) -> None:
        """Render the filtering and search controls."""
        st.markdown("**🔍 Filter & Search History**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Search by text content
            search_term = st.text_input(
                "Search in text",
                value=st.session_state.history_filters['search_term'],
                placeholder="Enter search term...",
                help="Search for predictions containing specific text"
            )
            if search_term != st.session_state.history_filters['search_term']:
                st.session_state.history_filters['search_term'] = search_term
        
        with col2:
            # Filter by sentiment
            sentiment_options = ['all'] + list(set([
                pred['sentiment_label'] for pred in st.session_state.prediction_history
            ]))
            sentiment_filter = st.selectbox(
                "Sentiment",
                options=sentiment_options,
                index=sentiment_options.index(st.session_state.history_filters['sentiment_filter']),
                help="Filter by predicted sentiment"
            )
            if sentiment_filter != st.session_state.history_filters['sentiment_filter']:
                st.session_state.history_filters['sentiment_filter'] = sentiment_filter
        
        with col3:
            # Filter by confidence threshold
            confidence_threshold = st.slider(
                "Min Confidence",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.history_filters['confidence_threshold'],
                step=0.05,
                help="Show only predictions above this confidence level"
            )
            if confidence_threshold != st.session_state.history_filters['confidence_threshold']:
                st.session_state.history_filters['confidence_threshold'] = confidence_threshold
        
        # Date range filter
        col4, col5 = st.columns(2)
        with col4:
            date_range = st.selectbox(
                "Date Range",
                options=['all', 'today', 'last_7_days', 'last_30_days'],
                index=['all', 'today', 'last_7_days', 'last_30_days'].index(
                    st.session_state.history_filters['date_range']
                ),
                help="Filter by time period"
            )
            if date_range != st.session_state.history_filters['date_range']:
                st.session_state.history_filters['date_range'] = date_range
        
        with col5:
            # Clear filters button
            if st.button("🗑️ Clear Filters", help="Reset all filters to default values"):
                st.session_state.history_filters = {
                    'search_term': '',
                    'sentiment_filter': 'all',
                    'confidence_threshold': 0.0,
                    'date_range': 'all'
                }
                st.rerun()
    
    def _get_filtered_history(self) -> List[Dict[str, Any]]:
        """Get filtered prediction history based on current filters."""
        filters = st.session_state.history_filters
        history = st.session_state.prediction_history
        
        filtered = history.copy()
        
        # Apply search filter
        if filters['search_term']:
            search_lower = filters['search_term'].lower()
            filtered = [
                pred for pred in filtered
                if search_lower in pred['input_text'].lower()
            ]
        
        # Apply sentiment filter
        if filters['sentiment_filter'] != 'all':
            filtered = [
                pred for pred in filtered
                if pred['sentiment_label'].lower() == filters['sentiment_filter'].lower()
            ]
        
        # Apply confidence threshold filter
        if filters['confidence_threshold'] > 0:
            filtered = [
                pred for pred in filtered
                if pred['confidence_score'] >= filters['confidence_threshold']
            ]
        
        # Apply date range filter
        if filters['date_range'] != 'all':
            now = datetime.now()
            if filters['date_range'] == 'today':
                filtered = [
                    pred for pred in filtered
                    if pred['timestamp'].date() == now.date()
                ]
            elif filters['date_range'] == 'last_7_days':
                from datetime import timedelta
                week_ago = now - timedelta(days=7)
                filtered = [
                    pred for pred in filtered
                    if pred['timestamp'] >= week_ago
                ]
            elif filters['date_range'] == 'last_30_days':
                from datetime import timedelta
                month_ago = now - timedelta(days=30)
                filtered = [
                    pred for pred in filtered
                    if pred['timestamp'] >= month_ago
                ]
        
        # Sort by timestamp (newest first)
        filtered.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return filtered
    
    def _render_history_summary(self, filtered_history: List[Dict[str, Any]]) -> None:
        """Render a summary of the filtered history."""
        if not filtered_history:
            return
        
        st.markdown("**📊 History Summary**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Predictions",
                value=len(filtered_history),
                delta=f"of {len(st.session_state.prediction_history)} total"
            )
        
        with col2:
            avg_confidence = sum(pred['confidence_score'] for pred in filtered_history) / len(filtered_history)
            st.metric(
                label="Avg Confidence",
                value=f"{avg_confidence*100:.1f}%"
            )
        
        with col3:
            sentiment_counts = {}
            for pred in filtered_history:
                sentiment = pred['sentiment_label']
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            
            most_common = max(sentiment_counts.items(), key=lambda x: x[1]) if sentiment_counts else ('none', 0)
            st.metric(
                label="Most Common",
                value=most_common[0].title(),
                delta=f"{most_common[1]} predictions"
            )
        
        with col4:
            avg_time = sum(pred['processing_time_ms'] for pred in filtered_history) / len(filtered_history)
            st.metric(
                label="Avg Processing",
                value=f"{avg_time:.1f} ms"
            )
    
    def _render_history_list(self, filtered_history: List[Dict[str, Any]]) -> None:
        """Render the list of prediction history entries."""
        st.markdown("**📝 Recent Predictions**")
        
        # Show only first 20 to avoid overwhelming the UI
        display_history = filtered_history[:20]
        
        for i, prediction in enumerate(display_history):
            with st.expander(
                f"#{prediction['id']} - {prediction['sentiment_label'].title()} "
                f"({prediction['confidence_score']*100:.1f}%) - "
                f"{prediction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
            ):
                self._render_prediction_detail(prediction)
        
        if len(filtered_history) > 20:
            st.info(f"📄 Showing 20 of {len(filtered_history)} predictions. Use filters to narrow down results.")
    
    def _render_prediction_detail(self, prediction: Dict[str, Any]) -> None:
        """Render detailed view of a single prediction."""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Input Text:**")
            st.text_area(
                "Input",
                value=prediction['input_text'],
                height=100,
                disabled=True,
                key=f"input_{prediction['id']}"
            )
        
        with col2:
            st.markdown("**Prediction Details:**")
            
            # Sentiment with color coding
            sentiment_colors = {
                "positive": "#28a745",
                "negative": "#dc3545",
                "neutral": "#ffc107"
            }
            sentiment_color = sentiment_colors.get(prediction['sentiment_label'].lower(), "#6c757d")
            
            st.markdown(
                f"<div style='color: {sentiment_color}; font-weight: 600; font-size: 1.1rem;'>"
                f"Sentiment: {prediction['sentiment_label'].title()}</div>",
                unsafe_allow_html=True
            )
            
            st.metric(
                label="Confidence",
                value=f"{prediction['confidence_score']*100:.1f}%"
            )
            
            st.metric(
                label="Processing Time",
                value=f"{prediction['processing_time_ms']:.1f} ms"
            )
            
            st.markdown(f"**Timestamp:** {prediction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show model confidence breakdown if available
        if prediction.get('model_confidence'):
            st.markdown("**📊 Model Confidence Breakdown:**")
            
            confidence_data = []
            for score_data in prediction['model_confidence']:
                label = score_data.get('label', 'Unknown')
                score = score_data.get('score', 0.0)
                confidence_data.append({
                    'Sentiment': label.title(),
                    'Confidence': f"{score*100:.1f}%",
                    'Score': f"{score:.4f}"
                })
            
            # Create a DataFrame for better display
            df = pd.DataFrame(confidence_data)
            st.dataframe(df, use_container_width=True)
    
    def _render_export_section(self, filtered_history: List[Dict[str, Any]]) -> None:
        """Render the export functionality section."""
        if not filtered_history:
            return
        
        st.markdown("**💾 Export History**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV export
            if st.button("📊 Export to CSV", help="Download filtered history as CSV file"):
                self._export_to_csv(filtered_history)
        
        with col2:
            # JSON export
            if st.button("📄 Export to JSON", help="Download filtered history as JSON file"):
                self._export_to_json(filtered_history)
    
    def _export_to_csv(self, filtered_history: List[Dict[str, Any]]) -> None:
        """Export filtered history to CSV format."""
        try:
            # Prepare data for CSV export
            export_data = []
            for pred in filtered_history:
                export_data.append({
                    'ID': pred['id'],
                    'Timestamp': pred['timestamp'].isoformat(),
                    'Input_Text': pred['input_text'],
                    'Sentiment_Label': pred['sentiment_label'],
                    'Confidence_Score': pred['confidence_score'],
                    'Processing_Time_MS': pred['processing_time_ms'],
                    'Text_Length': len(pred['input_text']),
                    'Word_Count': len(pred['input_text'].split())
                })
            
            # Create DataFrame and convert to CSV
            df = pd.DataFrame(export_data)
            csv_data = df.to_csv(index=False)
            
            # Create download button
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"sentiment_analysis_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            st.success("✅ CSV export ready for download!")
            
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")
    
    def _export_to_json(self, filtered_history: List[Dict[str, Any]]) -> None:
        """Export filtered history to JSON format."""
        try:
            import json
            
            # Prepare data for JSON export (convert datetime to string)
            export_data = []
            for pred in filtered_history:
                pred_copy = pred.copy()
                pred_copy['timestamp'] = pred_copy['timestamp'].isoformat()
                export_data.append(pred_copy)
            
            # Convert to JSON string
            json_data = json.dumps(export_data, indent=2, default=str)
            
            # Create download button
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"sentiment_analysis_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            st.success("✅ JSON export ready for download!")
            
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")
    
    def get_history_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the prediction history.
        
        Returns:
            Dictionary containing history statistics
        """
        if not st.session_state.prediction_history:
            return {
                'total_predictions': 0,
                'average_confidence': 0.0,
                'sentiment_distribution': {},
                'average_processing_time': 0.0
            }
        
        history = st.session_state.prediction_history
        
        # Calculate statistics
        total_predictions = len(history)
        average_confidence = sum(pred['confidence_score'] for pred in history) / total_predictions
        average_processing_time = sum(pred['processing_time_ms'] for pred in history) / total_predictions
        
        # Sentiment distribution
        sentiment_distribution = {}
        for pred in history:
            sentiment = pred['sentiment_label']
            sentiment_distribution[sentiment] = sentiment_distribution.get(sentiment, 0) + 1
        
        return {
            'total_predictions': total_predictions,
            'average_confidence': average_confidence,
            'sentiment_distribution': sentiment_distribution,
            'average_processing_time': average_processing_time
        }
