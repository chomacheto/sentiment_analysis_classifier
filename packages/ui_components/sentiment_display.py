"""
Sentiment Display Component

This module provides a reusable component for displaying sentiment analysis results
with professional styling, color coding, and visual confidence meters.
"""

import streamlit as st
from typing import Dict, Any
import math
from .attention_visualization import AttentionVisualization

class SentimentDisplay:
    """
    Component for displaying sentiment analysis results.
    
    Features:
    - Sentiment label with color coding (green/red/yellow)
    - Confidence percentage display
    - Visual confidence meter/progress bar
    - Processing time display
    - Professional styling and responsive design
    """
    
    def __init__(self):
        """Initialize the sentiment display component."""
        # Initialize attention visualization component
        self.attention_viz = AttentionVisualization()
        
        # Color scheme for different sentiments
        self.sentiment_colors = {
            "positive": {
                "primary": "#28a745",
                "secondary": "#d4edda",
                "text": "#155724"
            },
            "negative": {
                "primary": "#dc3545",
                "secondary": "#f8d7da",
                "text": "#721c24"
            },
            "neutral": {
                "primary": "#ffc107",
                "secondary": "#fff3cd",
                "text": "#856404"
            }
        }
        
        # Emoji mapping for sentiments
        self.sentiment_emojis = {
            "positive": "😊",
            "negative": "😞",
            "neutral": "😐"
        }
    
    def render(self, result: Dict[str, Any]) -> None:
        """
        Render the sentiment display component.
        
        Args:
            result: Dictionary containing sentiment analysis results
        """
        if not result:
            st.error("No sentiment analysis results to display")
            return
        
        # Extract results
        sentiment_label = result.get("sentiment_label", "unknown")
        confidence_score = result.get("confidence_score", 0.0)
        processing_time_ms = result.get("processing_time_ms", 0.0)
        
        # Get color scheme for sentiment
        colors = self.sentiment_colors.get(sentiment_label.lower(), self.sentiment_colors["neutral"])
        emoji = self.sentiment_emojis.get(sentiment_label.lower(), "🤔")
        
        # Create main results container
        with st.container():
            # Sentiment label and emoji
            st.markdown(
                f"""
                <div style="
                    background: {colors['secondary']};
                    border: 2px solid {colors['primary']};
                    border-radius: 10px;
                    padding: 1.5rem;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{emoji}</div>
                    <h2 style="
                        color: {colors['text']};
                        margin: 0;
                        font-size: 2rem;
                        font-weight: 700;
                        text-transform: capitalize;
                    ">{sentiment_label}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Confidence score and meter
            self._render_confidence_section(confidence_score, colors)
            
            # Processing time
            self._render_processing_time(processing_time_ms)
            
            # Additional metadata if available
            if "model_confidence" in result and result["model_confidence"]:
                self._render_model_confidence(result["model_confidence"], result)
    
    def _render_confidence_section(self, confidence_score: float, colors: Dict[str, str]) -> None:
        """
        Render the confidence score section with visual meter.
        
        Args:
            confidence_score: Confidence score (0.0-1.0)
            colors: Color scheme for the sentiment
        """
        # Convert to percentage
        confidence_percentage = confidence_score * 100
        
        # Create confidence container
        st.markdown(
            f"""
            <div style="
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 1.5rem;
                margin-bottom: 1rem;
            ">
                <h3 style="margin-top: 0; color: {colors['text']};">
                    🎯 Confidence Score
                </h3>
                <div style="
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: {colors['primary']};
                    text-align: center;
                    margin: 1rem 0;
                ">{confidence_percentage:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Visual confidence meter
        st.markdown("**Confidence Meter:**")
        
        # Create custom progress bar with sentiment colors
        meter_container = st.container()
        with meter_container:
            # Progress bar
            st.progress(confidence_score)
            
            # Confidence level indicator
            if confidence_percentage >= 80:
                level = "Very High"
                level_color = "#28a745"
            elif confidence_percentage >= 60:
                level = "High"
                level_color = "#17a2b8"
            elif confidence_percentage >= 40:
                level = "Medium"
                level_color = "#ffc107"
            elif confidence_percentage >= 20:
                level = "Low"
                level_color = "#fd7e14"
            else:
                level = "Very Low"
                level_color = "#dc3545"
            
            st.markdown(
                f"<div style='text-align: center; color: {level_color}; font-weight: 600;'>"
                f"Confidence Level: {level}</div>",
                unsafe_allow_html=True
            )
    
    def _render_processing_time(self, processing_time_ms: float) -> None:
        """
        Render the processing time display.
        
        Args:
            processing_time_ms: Processing time in milliseconds
        """
        # Convert to appropriate unit
        if processing_time_ms < 1000:
            time_display = f"{processing_time_ms:.1f} ms"
            time_color = "#28a745"  # Green for fast
        elif processing_time_ms < 2000:
            time_display = f"{processing_time_ms/1000:.2f} s"
            time_color = "#ffc107"  # Yellow for medium
        else:
            time_display = f"{processing_time_ms/1000:.2f} s"
            time_color = "#dc3545"  # Red for slow
        
        st.markdown(
            f"""
            <div style="
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
                text-align: center;
            ">
                <div style="color: #6c757d; font-size: 0.9rem; margin-bottom: 0.5rem;">
                    ⏱️ Processing Time
                </div>
                <div style="
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: {time_color};
                ">{time_display}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def _render_model_confidence(self, model_confidence: list, result: dict = None) -> None:
        """
        Render detailed model confidence scores.
        
        Args:
            model_confidence: List of model confidence scores
            result: Full result dictionary for attention visualization
        """
        if not model_confidence:
            return
        
        st.markdown("**📊 Model Confidence Breakdown:**")
        
        # Flatten the model_confidence structure
        flattened_scores = []
        for score_data in model_confidence:
            if isinstance(score_data, list):
                flattened_scores.extend(score_data)
            else:
                flattened_scores.append(score_data)
        
        # Create columns for each confidence score
        cols = st.columns(len(flattened_scores))
        
        for i, score_data in enumerate(flattened_scores):
            with cols[i]:
                # Handle dictionary format from Hugging Face pipeline
                if isinstance(score_data, dict):
                    label = score_data.get("label", f"Class {i}")
                    score = score_data.get("score", 0.0)
                else:
                    # Fallback for direct score values
                    label = f"Class {i}"
                    score = float(score_data) if score_data is not None else 0.0
                percentage = score * 100
                
                # Color based on score
                if score >= 0.7:
                    color = "#28a745"
                elif score >= 0.4:
                    color = "#ffc107"
                else:
                    color = "#dc3545"
                
                st.markdown(
                    f"""
                    <div style="
                        background: white;
                        border: 1px solid #dee2e6;
                        border-radius: 5px;
                        padding: 1rem;
                        text-align: center;
                    ">
                        <div style="font-weight: 600; margin-bottom: 0.5rem;">{label}</div>
                        <div style="
                            font-size: 1.2rem;
                            color: {color};
                            font-weight: 700;
                        ">{percentage:.1f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Add enhanced confidence metrics link with unique key
        import uuid
        unique_key = f"enhanced_confidence_btn_{uuid.uuid4().hex[:8]}"
        if st.button("🔍 View Enhanced Confidence Metrics", help="Open detailed confidence visualization", key=unique_key):
            st.session_state.show_enhanced_confidence = True
        
        # Add attention visualization if available
        if result and "attention_weights" in result:
            st.markdown("---")
            st.subheader("🧠 Explainable AI - Word-Level Analysis")
            self.attention_viz.render(result)
