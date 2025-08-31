"""
Statistics Panel Component

This module provides a comprehensive statistics dashboard showing average confidence,
prediction count, success rate metrics, and confidence distribution charts.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StatisticsPanel:
    """
    Component for displaying comprehensive statistics and metrics.
    
    Features:
    - Statistics dashboard showing average confidence
    - Display prediction count and success rate metrics
    - Confidence distribution charts (histogram/box plot)
    - Real-time statistics updates
    - Performance metrics and trends
    """
    
    def __init__(self):
        """Initialize the statistics panel component."""
        self.chart_colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'info': '#17a2b8'
        }
    
    def render(self, prediction_history: List[Dict[str, Any]] = None) -> None:
        """
        Render the statistics panel component.
        
        Args:
            prediction_history: List of prediction history entries
        """
        if not prediction_history:
            st.info("📊 No prediction data available yet. Start analyzing text to see statistics!")
            return
        
        st.markdown("## 📊 Statistics Dashboard")
        
        # Create tabs for different statistical views
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Overview Metrics", 
            "📊 Confidence Distribution", 
            "⏱️ Performance Trends",
            "🎯 Sentiment Analysis"
        ])
        
        with tab1:
            self._render_overview_metrics(prediction_history)
        
        with tab2:
            self._render_confidence_distribution(prediction_history)
        
        with tab3:
            self._render_performance_trends(prediction_history)
        
        with tab4:
            self._render_sentiment_analysis(prediction_history)
    
    def _render_overview_metrics(self, prediction_history: List[Dict[str, Any]]) -> None:
        """
        Render overview metrics including counts, averages, and key statistics.
        
        Args:
            prediction_history: List of prediction history entries
        """
        if not prediction_history:
            return
        
        # Calculate key metrics
        total_predictions = len(prediction_history)
        avg_confidence = sum(pred['confidence_score'] for pred in prediction_history) / total_predictions
        avg_processing_time = sum(pred['processing_time_ms'] for pred in prediction_history) / total_predictions
        
        # Sentiment distribution
        sentiment_counts = {}
        for pred in prediction_history:
            sentiment = pred['sentiment_label']
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        # Most common sentiment
        most_common_sentiment = max(sentiment_counts.items(), key=lambda x: x[1]) if sentiment_counts else ('none', 0)
        
        # Confidence level distribution
        confidence_levels = {
            'Very High': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0,
            'Very Low': 0
        }
        
        for pred in prediction_history:
            confidence_percentage = pred['confidence_score'] * 100
            if confidence_percentage >= 90:
                confidence_levels['Very High'] += 1
            elif confidence_percentage >= 75:
                confidence_levels['High'] += 1
            elif confidence_percentage >= 60:
                confidence_levels['Medium'] += 1
            elif confidence_percentage >= 40:
                confidence_levels['Low'] += 1
            else:
                confidence_levels['Very Low'] += 1
        
        # Display metrics in a grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Core Metrics**")
            
            # Total predictions
            st.metric(
                label="Total Predictions",
                value=total_predictions,
                delta=f"Last 24h: {self._get_recent_count(prediction_history, 1)}"
            )
            
            # Average confidence
            st.metric(
                label="Average Confidence",
                value=f"{avg_confidence*100:.1f}%",
                delta=f"{self._get_confidence_trend(prediction_history):+.1f}%"
            )
            
            # Most common sentiment
            st.metric(
                label="Most Common Sentiment",
                value=most_common_sentiment[0].title(),
                delta=f"{most_common_sentiment[1]} predictions"
            )
        
        with col2:
            st.markdown("**⚡ Performance Metrics**")
            
            # Average processing time
            st.metric(
                label="Avg Processing Time",
                value=f"{avg_processing_time:.1f} ms",
                delta=f"{self._get_processing_time_trend(prediction_history):+.1f} ms"
            )
            
            # Success rate (confidence > 0.7)
            high_confidence_count = sum(1 for pred in prediction_history if pred['confidence_score'] > 0.7)
            success_rate = (high_confidence_count / total_predictions) * 100
            st.metric(
                label="High Confidence Rate",
                value=f"{success_rate:.1f}%",
                delta=f"{high_confidence_count} of {total_predictions}"
            )
            
            # Model efficiency
            efficient_predictions = sum(1 for pred in prediction_history if pred['processing_time_ms'] < 1000)
            efficiency_rate = (efficient_predictions / total_predictions) * 100
            st.metric(
                label="Fast Predictions (<1s)",
                value=f"{efficiency_rate:.1f}%",
                delta=f"{efficient_predictions} of {total_predictions}"
            )
        
        # Confidence level distribution
        st.markdown("**🎯 Confidence Level Distribution**")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        confidence_colors = {
            'Very High': '#28a745',
            'High': '#17a2b8',
            'Medium': '#ffc107',
            'Low': '#fd7e14',
            'Very Low': '#dc3545'
        }
        
        for i, (level, count) in enumerate(confidence_levels.items()):
            with [col1, col2, col3, col4, col5][i]:
                percentage = (count / total_predictions) * 100 if total_predictions > 0 else 0
                color = confidence_colors[level]
                
                st.markdown(
                    f"""
                    <div style="
                        background: white;
                        border: 2px solid {color};
                        border-radius: 10px;
                        padding: 1rem;
                        text-align: center;
                        margin: 0.5rem 0;
                    ">
                        <div style="
                            font-size: 1.5rem;
                            font-weight: 700;
                            color: {color};
                        ">{count}</div>
                        <div style="
                            font-size: 0.9rem;
                            color: #6c757d;
                            margin-bottom: 0.5rem;
                        ">{level}</div>
                        <div style="
                            font-size: 0.8rem;
                            color: {color};
                            font-weight: 600;
                        ">{percentage:.1f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    def _render_confidence_distribution(self, prediction_history: List[Dict[str, Any]]) -> None:
        """
        Render confidence distribution charts including histogram and box plot.
        
        Args:
            prediction_history: List of prediction history entries
        """
        if not prediction_history:
            return
        
        st.markdown("**📊 Confidence Score Distribution**")
        
        # Extract confidence scores
        confidence_scores = [pred['confidence_score'] for pred in prediction_history]
        
        # Create histogram
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📈 Confidence Histogram**")
            
            fig_hist = px.histogram(
                x=confidence_scores,
                nbins=20,
                title="Distribution of Confidence Scores",
                labels={'x': 'Confidence Score', 'y': 'Frequency'},
                color_discrete_sequence=[self.chart_colors['primary']]
            )
            
            fig_hist.update_layout(
                xaxis=dict(range=[0, 1]),
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            st.markdown("**📦 Confidence Box Plot**")
            
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(
                y=confidence_scores,
                name="Confidence Scores",
                marker_color=self.chart_colors['secondary'],
                boxpoints='outliers'
            ))
            
            fig_box.update_layout(
                title="Confidence Score Distribution",
                yaxis_title="Confidence Score",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Statistical summary
        st.markdown("**📋 Statistical Summary**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Mean",
                value=f"{np.mean(confidence_scores):.3f}"
            )
        
        with col2:
            st.metric(
                label="Median",
                value=f"{np.median(confidence_scores):.3f}"
            )
        
        with col3:
            st.metric(
                label="Std Dev",
                value=f"{np.std(confidence_scores):.3f}"
            )
        
        with col4:
            st.metric(
                label="Range",
                value=f"{np.max(confidence_scores) - np.min(confidence_scores):.3f}"
            )
        
        # Confidence intervals
        st.markdown("**🎯 Confidence Intervals**")
        
        sorted_scores = sorted(confidence_scores)
        n = len(sorted_scores)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            percentile_25 = sorted_scores[int(0.25 * n)] if n > 0 else 0
            st.metric(
                label="25th Percentile",
                value=f"{percentile_25:.3f}"
            )
        
        with col2:
            percentile_75 = sorted_scores[int(0.75 * n)] if n > 0 else 0
            st.metric(
                label="75th Percentile",
                value=f"{percentile_75:.3f}"
            )
        
        with col3:
            iqr = percentile_75 - percentile_25
            st.metric(
                label="Interquartile Range",
                value=f"{iqr:.3f}"
            )
    
    def _render_performance_trends(self, prediction_history: List[Dict[str, Any]]) -> None:
        """
        Render performance trends and time-based analysis.
        
        Args:
            prediction_history: List of prediction history entries
        """
        if not prediction_history:
            return
        
        st.markdown("**⏱️ Performance Trends**")
        
        # Group predictions by time periods
        now = datetime.now()
        time_periods = {
            'Last Hour': now - timedelta(hours=1),
            'Last 6 Hours': now - timedelta(hours=6),
            'Last 24 Hours': now - timedelta(days=1),
            'Last 7 Days': now - timedelta(days=7),
            'Last 30 Days': now - timedelta(days=30)
        }
        
        # Calculate metrics for each time period
        period_metrics = {}
        for period_name, cutoff_time in time_periods.items():
            period_predictions = [
                pred for pred in prediction_history
                if pred['timestamp'] >= cutoff_time
            ]
            
            if period_predictions:
                avg_confidence = sum(pred['confidence_score'] for pred in period_predictions) / len(period_predictions)
                avg_time = sum(pred['processing_time_ms'] for pred in period_predictions) / len(period_predictions)
                count = len(period_predictions)
            else:
                avg_confidence = 0
                avg_time = 0
                count = 0
            
            period_metrics[period_name] = {
                'count': count,
                'avg_confidence': avg_confidence,
                'avg_time': avg_time
            }
        
        # Display time-based metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Predictions by Time Period**")
            
            for period_name, metrics in period_metrics.items():
                st.metric(
                    label=period_name,
                    value=metrics['count'],
                    delta=f"Avg: {metrics['avg_confidence']*100:.1f}% confidence"
                )
        
        with col2:
            st.markdown("**⚡ Processing Time by Period**")
            
            for period_name, metrics in period_metrics.items():
                if metrics['count'] > 0:
                    st.metric(
                        label=period_name,
                        value=f"{metrics['avg_time']:.1f} ms",
                        delta=f"{metrics['count']} predictions"
                    )
        
        # Performance over time chart
        st.markdown("**📈 Performance Over Time**")
        
        # Create time series data
        if len(prediction_history) > 1:
            # Sort by timestamp and group by hour
            sorted_history = sorted(prediction_history, key=lambda x: x['timestamp'])
            
            # Group by hour for the last 24 hours
            hourly_data = {}
            for pred in sorted_history:
                if pred['timestamp'] >= now - timedelta(hours=24):
                    hour_key = pred['timestamp'].replace(minute=0, second=0, microsecond=0)
                    if hour_key not in hourly_data:
                        hourly_data[hour_key] = []
                    hourly_data[hour_key].append(pred)
            
            if hourly_data:
                hours = sorted(hourly_data.keys())
                avg_confidences = []
                avg_times = []
                counts = []
                
                for hour in hours:
                    hour_predictions = hourly_data[hour]
                    avg_confidences.append(
                        sum(pred['confidence_score'] for pred in hour_predictions) / len(hour_predictions)
                    )
                    avg_times.append(
                        sum(pred['processing_time_ms'] for pred in hour_predictions) / len(hour_predictions)
                    )
                    counts.append(len(hour_predictions))
                
                # Create dual-axis chart
                fig = go.Figure()
                
                # Add confidence line
                fig.add_trace(go.Scatter(
                    x=hours,
                    y=avg_confidences,
                    mode='lines+markers',
                    name='Avg Confidence',
                    yaxis='y',
                    line=dict(color=self.chart_colors['primary'])
                ))
                
                # Add processing time line
                fig.add_trace(go.Scatter(
                    x=hours,
                    y=avg_times,
                    mode='lines+markers',
                    name='Avg Processing Time (ms)',
                    yaxis='y2',
                    line=dict(color=self.chart_colors['secondary'])
                ))
                
                fig.update_layout(
                    title="Performance Metrics Over Time (Last 24 Hours)",
                    xaxis_title="Time",
                    yaxis=dict(title="Confidence Score", side="left"),
                    yaxis2=dict(title="Processing Time (ms)", side="right", overlaying="y"),
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_sentiment_analysis(self, prediction_history: List[Dict[str, Any]]) -> None:
        """
        Render sentiment analysis statistics and trends.
        
        Args:
            prediction_history: List of prediction history entries
        """
        if not prediction_history:
            return
        
        st.markdown("**🎯 Sentiment Analysis Statistics**")
        
        # Sentiment distribution
        sentiment_counts = {}
        sentiment_confidences = {}
        
        for pred in prediction_history:
            sentiment = pred['sentiment_label']
            confidence = pred['confidence_score']
            
            if sentiment not in sentiment_counts:
                sentiment_counts[sentiment] = 0
                sentiment_confidences[sentiment] = []
            
            sentiment_counts[sentiment] += 1
            sentiment_confidences[sentiment].append(confidence)
        
        # Display sentiment distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Sentiment Distribution**")
            
            # Create pie chart
            if sentiment_counts:
                fig_pie = px.pie(
                    values=list(sentiment_counts.values()),
                    names=[sent.title() for sent in sentiment_counts.keys()],
                    title="Sentiment Distribution",
                    color_discrete_sequence=[self.chart_colors['success'], self.chart_colors['danger'], self.chart_colors['warning']]
                )
                
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("**📈 Sentiment Confidence Comparison**")
            
            # Create bar chart for average confidence by sentiment
            if sentiment_confidences:
                sentiment_avg_confidences = {
                    sent: sum(confs) / len(confs) 
                    for sent, confs in sentiment_confidences.items()
                }
                
                fig_bar = px.bar(
                    x=list(sentiment_avg_confidences.keys()),
                    y=list(sentiment_avg_confidences.values()),
                    title="Average Confidence by Sentiment",
                    labels={'x': 'Sentiment', 'y': 'Average Confidence'},
                    color=list(sentiment_avg_confidences.values()),
                    color_continuous_scale='RdYlGn'
                )
                
                fig_bar.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Detailed sentiment metrics
        st.markdown("**🔍 Detailed Sentiment Metrics**")
        
        if sentiment_counts:
            # Create metrics grid
            cols = st.columns(len(sentiment_counts))
            
            for i, (sentiment, count) in enumerate(sentiment_counts.items()):
                with cols[i]:
                    percentage = (count / len(prediction_history)) * 100
                    avg_confidence = sum(sentiment_confidences[sentiment]) / len(sentiment_confidences[sentiment])
                    
                    # Color based on sentiment
                    sentiment_colors = {
                        'positive': self.chart_colors['success'],
                        'negative': self.chart_colors['danger'],
                        'neutral': self.chart_colors['warning']
                    }
                    color = sentiment_colors.get(sentiment.lower(), self.chart_colors['info'])
                    
                    st.markdown(
                        f"""
                        <div style="
                            background: white;
                            border: 2px solid {color};
                            border-radius: 10px;
                            padding: 1rem;
                            text-align: center;
                            margin: 0.5rem 0;
                        ">
                            <div style="
                                font-size: 1.5rem;
                                font-weight: 700;
                                color: {color};
                            ">{sentiment.title()}</div>
                            <div style="
                                font-size: 1.2rem;
                                color: #6c757d;
                                margin: 0.5rem 0;
                            ">{count} predictions</div>
                            <div style="
                                font-size: 1rem;
                                color: {color};
                                font-weight: 600;
                            ">{percentage:.1f}% of total</div>
                            <div style="
                                font-size: 0.9rem;
                                color: #6c757d;
                                margin-top: 0.5rem;
                            ">Avg Confidence: {avg_confidence*100:.1f}%</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
    def _get_recent_count(self, prediction_history: List[Dict[str, Any]], days: int) -> int:
        """Get count of predictions from the last N days."""
        cutoff_time = datetime.now() - timedelta(days=days)
        return sum(1 for pred in prediction_history if pred['timestamp'] >= cutoff_time)
    
    def _get_confidence_trend(self, prediction_history: List[Dict[str, Any]]) -> float:
        """Get confidence trend (change in average confidence over time)."""
        if len(prediction_history) < 2:
            return 0.0
        
        # Compare recent vs older predictions
        mid_point = len(prediction_history) // 2
        recent = prediction_history[:mid_point]
        older = prediction_history[mid_point:]
        
        if not recent or not older:
            return 0.0
        
        recent_avg = sum(pred['confidence_score'] for pred in recent) / len(recent)
        older_avg = sum(pred['confidence_score'] for pred in older) / len(older)
        
        return (recent_avg - older_avg) * 100
    
    def _get_processing_time_trend(self, prediction_history: List[Dict[str, Any]]) -> float:
        """Get processing time trend (change in average processing time over time)."""
        if len(prediction_history) < 2:
            return 0.0
        
        # Compare recent vs older predictions
        mid_point = len(prediction_history) // 2
        recent = prediction_history[:mid_point]
        older = prediction_history[mid_point:]
        
        if not recent or not older:
            return 0.0
        
        recent_avg = sum(pred['processing_time_ms'] for pred in recent) / len(recent)
        older_avg = sum(pred['processing_time_ms'] for pred in older) / len(older)
        
        return recent_avg - older_avg
