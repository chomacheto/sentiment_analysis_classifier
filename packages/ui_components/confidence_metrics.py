"""
Confidence Metrics Component

This module provides enhanced confidence visualization including probability distribution charts,
enhanced confidence meters, and detailed confidence level indicators.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
import math

class ConfidenceMetrics:
    """
    Component for displaying enhanced confidence metrics and visualizations.
    
    Features:
    - Probability distribution chart showing all sentiment class scores
    - Enhanced confidence meter with granular visual indicators
    - Color-coded sentiment indicators with improved visual hierarchy
    - Confidence level indicators (Very High, High, Medium, Low, Very Low)
    - Interactive charts and detailed breakdowns
    """
    
    def __init__(self):
        """Initialize the confidence metrics component."""
        # Enhanced color scheme for confidence levels
        self.confidence_colors = {
            "Very High": {"color": "#28a745", "bg": "#d4edda", "text": "#155724"},
            "High": {"color": "#17a2b8", "bg": "#d1ecf1", "text": "#0c5460"},
            "Medium": {"color": "#ffc107", "bg": "#fff3cd", "text": "#856404"},
            "Low": {"color": "#fd7e14", "bg": "#ffeaa7", "text": "#a04000"},
            "Very Low": {"color": "#dc3545", "bg": "#f8d7da", "text": "#721c24"}
        }
        
        # Sentiment color mapping
        self.sentiment_colors = {
            "positive": "#28a745",
            "negative": "#dc3545",
            "neutral": "#ffc107"
        }
    
    def render(self, result: Dict[str, Any]) -> None:
        """
        Render the enhanced confidence metrics component.
        
        Args:
            result: Dictionary containing sentiment analysis results
        """
        if not result:
            st.error("No sentiment analysis results to display")
            return
        
        # Extract results
        sentiment_label = result.get("sentiment_label", "unknown")
        confidence_score = result.get("confidence_score", 0.0)
        model_confidence = result.get("model_confidence", [])
        
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["📊 Confidence Overview", "📈 Probability Distribution", "🎯 Detailed Metrics"])
        
        with tab1:
            self._render_confidence_overview(confidence_score, sentiment_label)
        
        with tab2:
            self._render_probability_distribution(model_confidence, sentiment_label)
        
        with tab3:
            self._render_detailed_metrics(confidence_score, model_confidence, sentiment_label)
    
    def _render_confidence_overview(self, confidence_score: float, sentiment_label: str) -> None:
        """
        Render the main confidence overview with enhanced visual indicators.
        
        Args:
            confidence_score: Confidence score (0.0-1.0)
            sentiment_label: Predicted sentiment label
        """
        confidence_percentage = confidence_score * 100
        confidence_level = self._get_confidence_level(confidence_percentage)
        level_colors = self.confidence_colors[confidence_level]
        
        # Main confidence display
        st.markdown(
            f"""
            <div style="
                background: {level_colors['bg']};
                border: 3px solid {level_colors['color']};
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                margin-bottom: 2rem;
            ">
                <h2 style="
                    color: {level_colors['text']};
                    margin: 0 0 1rem 0;
                    font-size: 1.5rem;
                    font-weight: 600;
                ">🎯 Confidence Level: {confidence_level}</h2>
                
                <div style="
                    font-size: 4rem;
                    font-weight: 700;
                    color: {level_colors['color']};
                    margin: 1rem 0;
                ">{confidence_percentage:.1f}%</div>
                
                <div style="
                    color: {level_colors['text']};
                    font-size: 1.1rem;
                    opacity: 0.8;
                ">Predicted Sentiment: {sentiment_label.title()}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Enhanced confidence meter
        self._render_enhanced_confidence_meter(confidence_score, level_colors)
    
    def _render_enhanced_confidence_meter(self, confidence_score: float, level_colors: Dict[str, str]) -> None:
        """
        Render an enhanced confidence meter with granular visual indicators.
        
        Args:
            confidence_score: Confidence score (0.0-1.0)
            level_colors: Color scheme for the confidence level
        """
        st.markdown("**Enhanced Confidence Meter:**")
        
        # Create custom progress bar with multiple segments
        meter_container = st.container()
        with meter_container:
            # Main progress bar
            st.progress(confidence_score)
            
            # Confidence level indicators with color coding
            col1, col2, col3, col4, col5 = st.columns(5)
            
            levels = ["Very Low", "Low", "Medium", "High", "Very High"]
            thresholds = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
            
            for i, (level, threshold) in enumerate(zip(levels, thresholds[:-1])):
                with [col1, col2, col3, col4, col5][i]:
                    level_colors = self.confidence_colors[level]
                    is_active = confidence_score >= threshold
                    
                    # Determine border style based on whether this level is active
                    border_style = f"3px solid {level_colors['color']}" if is_active else "1px solid #dee2e6"
                    bg_color = level_colors['bg'] if is_active else "#f8f9fa"
                    text_color = level_colors['text'] if is_active else "#6c757d"
                    
                    st.markdown(
                        f"""
                        <div style="
                            background: {bg_color};
                            border: {border_style};
                            border-radius: 8px;
                            padding: 0.5rem;
                            text-align: center;
                            margin: 0.25rem 0;
                        ">
                            <div style="
                                font-size: 0.8rem;
                                font-weight: 600;
                                color: {text_color};
                            ">{level}</div>
                            <div style="
                                font-size: 0.7rem;
                                color: {text_color};
                                opacity: 0.8;
                            ">{threshold*100:.0f}%+</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
    def _render_probability_distribution(self, model_confidence: List[Dict], sentiment_label: str) -> None:
        """
        Render probability distribution chart showing scores for all sentiment classes.
        
        Args:
            model_confidence: List of model confidence scores
            sentiment_label: Predicted sentiment label
        """
        if not model_confidence:
            st.warning("No model confidence data available for probability distribution")
            return
        
        st.markdown("**📈 Probability Distribution Across All Sentiment Classes**")
        
        # Extract data for plotting
        labels = []
        scores = []
        colors = []
        
        for score_data in model_confidence:
            label = score_data.get("label", "Unknown")
            score = score_data.get("score", 0.0)
            
            labels.append(label.title())
            scores.append(score)
            
            # Color based on whether this is the predicted label
            if label.lower() == sentiment_label.lower():
                colors.append(self.sentiment_colors.get(sentiment_label.lower(), "#6c757d"))
            else:
                colors.append("#6c757d")
        
        # Create horizontal bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=scores,
                y=labels,
                orientation='h',
                marker_color=colors,
                text=[f"{score*100:.1f}%" for score in scores],
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Confidence: %{x:.3f}<br>Percentage: %{text}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="Sentiment Class Confidence Distribution",
            xaxis_title="Confidence Score",
            yaxis_title="Sentiment Class",
            xaxis=dict(range=[0, 1]),
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insights below the chart
        max_score = max(scores)
        max_label = labels[scores.index(max_score)]
        
        st.info(f"💡 **Insight**: The model is most confident in '{max_label}' with {max_score*100:.1f}% confidence.")
    
    def _render_detailed_metrics(self, confidence_score: float, model_confidence: List[Dict], sentiment_label: str) -> None:
        """
        Render detailed confidence metrics and breakdowns.
        
        Args:
            confidence_score: Confidence score (0.0-1.0)
            model_confidence: List of model confidence scores
            sentiment_label: Predicted sentiment label
        """
        confidence_percentage = confidence_score * 100
        confidence_level = self._get_confidence_level(confidence_percentage)
        
        # Create metrics grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Overall Confidence",
                value=f"{confidence_percentage:.1f}%",
                delta=f"{confidence_level} Level"
            )
            
            st.metric(
                label="Confidence Level",
                value=confidence_level,
                delta=f"Threshold: {self._get_confidence_threshold(confidence_level)*100:.0f}%"
            )
        
        with col2:
            # Calculate additional metrics
            if model_confidence:
                second_highest = sorted([s.get("score", 0) for s in model_confidence], reverse=True)[1] if len(model_confidence) > 1 else 0
                margin = confidence_score - second_highest
                
                st.metric(
                    label="Margin of Victory",
                    value=f"{margin*100:.1f}%",
                    delta="vs Second Best"
                )
                
                # Confidence stability (how close scores are)
                score_variance = sum((s.get("score", 0) - confidence_score) ** 2 for s in model_confidence) / len(model_confidence)
                stability = 1 - min(score_variance * 10, 1)  # Normalize to 0-1
                
                st.metric(
                    label="Prediction Stability",
                    value=f"{stability*100:.1f}%",
                    delta="High = More Certain"
                )
        
        # Detailed breakdown
        st.markdown("**🔍 Detailed Confidence Breakdown:**")
        
        if model_confidence:
            # Create a detailed table
            breakdown_data = []
            for score_data in model_confidence:
                label = score_data.get("label", "Unknown")
                score = score_data.get("score", 0.0)
                percentage = score * 100
                
                # Determine status
                if label.lower() == sentiment_label.lower():
                    status = "🏆 **PREDICTED**"
                    status_color = "#28a745"
                else:
                    status = "❌ Not Selected"
                    status_color = "#6c757d"
                
                breakdown_data.append({
                    "Sentiment": label.title(),
                    "Confidence": f"{percentage:.1f}%",
                    "Score": f"{score:.4f}",
                    "Status": status,
                    "Color": status_color
                })
            
            # Sort by confidence score (highest first)
            breakdown_data.sort(key=lambda x: float(x["Score"]), reverse=True)
            
            # Display as styled table
            for item in breakdown_data:
                st.markdown(
                    f"""
                    <div style="
                        background: white;
                        border: 1px solid #dee2e6;
                        border-radius: 5px;
                        padding: 1rem;
                        margin: 0.5rem 0;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <div style="flex: 1;">
                            <strong>{item['Sentiment']}</strong>
                        </div>
                        <div style="flex: 1; text-align: center;">
                            <span style="font-size: 1.2rem; font-weight: 600; color: {item['Color']};">
                                {item['Confidence']}
                            </span>
                        </div>
                        <div style="flex: 1; text-align: center;">
                            <span style="color: #6c757d;">{item['Score']}</span>
                        </div>
                        <div style="flex: 1; text-align: right;">
                            <span style="color: {item['Color']}; font-weight: 600;">
                                {item['Status']}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    def _get_confidence_level(self, confidence_percentage: float) -> str:
        """
        Get the confidence level based on percentage.
        
        Args:
            confidence_percentage: Confidence percentage (0-100)
            
        Returns:
            Confidence level string
        """
        if confidence_percentage >= 90:
            return "Very High"
        elif confidence_percentage >= 75:
            return "High"
        elif confidence_percentage >= 60:
            return "Medium"
        elif confidence_percentage >= 40:
            return "Low"
        else:
            return "Very Low"
    
    def _get_confidence_threshold(self, confidence_level: str) -> float:
        """
        Get the threshold for a confidence level.
        
        Args:
            confidence_level: Confidence level string
            
        Returns:
            Threshold value (0.0-1.0)
        """
        thresholds = {
            "Very High": 0.9,
            "High": 0.75,
            "Medium": 0.6,
            "Low": 0.4,
            "Very Low": 0.0
        }
        return thresholds.get(confidence_level, 0.0)
