"""
Attention Visualization Component

This module provides components for visualizing word-level attention in sentiment analysis,
including heatmaps, clickable word interactions, and contribution score displays.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional
import numpy as np

class WordAttentionHeatmap:
    """
    Component for visualizing word-level attention with interactive heatmaps.
    
    Features:
    - Color-coded attention visualization (red for negative, green for positive influence)
    - Clickable word interactions with contribution score display
    - Interactive heatmap with hover information
    - Responsive design for different screen sizes
    """
    
    def __init__(self):
        """Initialize the attention heatmap component."""
        # Color scheme for attention visualization
        self.attention_colors = {
            "positive": {
                "low": "#e8f5e8",
                "medium": "#4caf50",
                "high": "#2e7d32"
            },
            "negative": {
                "low": "#ffebee",
                "medium": "#f44336",
                "high": "#c62828"
            },
            "neutral": {
                "low": "#f5f5f5",
                "medium": "#9e9e9e",
                "high": "#424242"
            }
        }
    
    def render(self, attention_data: Dict[str, Any], sentiment_label: str) -> None:
        """
        Render the attention heatmap visualization.
        
        Args:
            attention_data: Dictionary containing attention weights and word contributions
            sentiment_label: Predicted sentiment label
        """
        if not attention_data or "attention_weights" not in attention_data:
            st.warning("No attention data available for visualization")
            return
        
        attention_weights = attention_data.get("attention_weights", [])
        if not attention_weights:
            st.warning("No attention weights found in the data")
            return
        
        # Create the attention heatmap
        self._render_attention_heatmap(attention_weights, sentiment_label)
        
        # Create clickable word interactions
        self._render_clickable_words(attention_weights, sentiment_label)
    
    def _render_attention_heatmap(self, attention_weights: List[Dict], sentiment_label: str) -> None:
        """Render the main attention heatmap visualization."""
        st.subheader("🔍 Word-Level Attention Heatmap")
        
        # Prepare data for visualization
        tokens = [item["token"] for item in attention_weights]
        attention_scores = [item["attention_score"] for item in attention_weights]
        contribution_scores = [item["contribution_score"] for item in attention_weights]
        
        # Create color mapping based on contribution scores
        colors = []
        for score in contribution_scores:
            if abs(score) < 0.1:
                intensity = "low"
            elif abs(score) < 0.3:
                intensity = "medium"
            else:
                intensity = "high"
            
            if score > 0:
                colors.append(self.attention_colors["positive"][intensity])
            elif score < 0:
                colors.append(self.attention_colors["negative"][intensity])
            else:
                colors.append(self.attention_colors["neutral"][intensity])
        
        # Create the heatmap using plotly
        fig = go.Figure(data=go.Bar(
            x=tokens,
            y=attention_scores,
            marker_color=colors,
            text=[f"Score: {score:.3f}<br>Contribution: {contrib:.3f}" 
                  for score, contrib in zip(attention_scores, contribution_scores)],
            textposition='auto',
            hovertemplate="<b>%{x}</b><br>" +
                         "Attention Score: %{y:.3f}<br>" +
                         "Contribution: %{text}<br>" +
                         "<extra></extra>"
        ))
        
        # Update layout
        fig.update_layout(
            title=f"Word Attention Scores - {sentiment_label.capitalize()} Sentiment",
            xaxis_title="Words",
            yaxis_title="Attention Score",
            height=400,
            showlegend=False,
            xaxis=dict(
                tickangle=45,
                tickmode='array',
                ticktext=tokens,
                tickvals=list(range(len(tokens)))
            )
        )
        
        # Display the heatmap
        st.plotly_chart(fig, use_container_width=True)
        
        # Add explanation
        st.markdown("""
        **How to interpret this visualization:**
        - **Green bars**: Words that contribute positively to the sentiment
        - **Red bars**: Words that contribute negatively to the sentiment
        - **Bar height**: Attention score (how much the model focuses on each word)
        - **Color intensity**: Contribution strength (darker = stronger influence)
        """)
    
    def _render_clickable_words(self, attention_weights: List[Dict], sentiment_label: str) -> None:
        """Render clickable word interactions with contribution scores."""
        st.subheader("🎯 Clickable Word Analysis")
        
        # Create columns for better layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Click on any word to see its detailed contribution:**")
            
            # Create clickable word display
            word_html = ""
            for item in attention_weights:
                token = item["token"]
                attention_score = item["attention_score"]
                contribution_score = item["contribution_score"]
                
                # Determine color based on contribution
                if contribution_score > 0:
                    color = self.attention_colors["positive"]["medium"]
                    influence = "positive"
                elif contribution_score < 0:
                    color = self.attention_colors["negative"]["medium"]
                    influence = "negative"
                else:
                    color = self.attention_colors["neutral"]["medium"]
                    influence = "neutral"
                
                # Create clickable word with hover effect
                word_html += f"""
                <span style="
                    display: inline-block;
                    margin: 2px;
                    padding: 4px 8px;
                    background-color: {color};
                    color: white;
                    border-radius: 4px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: all 0.3s ease;
                " 
                onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.3)';"
                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none';"
                title="Attention: {attention_score:.3f}, Contribution: {contribution_score:.3f}, Influence: {influence}"
                >
                    {token}
                </span>
                """
            
            st.markdown(word_html, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Word Contribution Legend:**")
            st.markdown("""
            - 🟢 **Green**: Positive contribution
            - 🔴 **Red**: Negative contribution  
            - ⚪ **Gray**: Neutral contribution
            
            **Hover over words** to see detailed scores!
            """)

class TopContributingWords:
    """
    Component for displaying top contributing words with influence rankings.
    """
    
    def __init__(self):
        """Initialize the top contributing words component."""
        pass
    
    def render(self, attention_data: Dict[str, Any]) -> None:
        """
        Render the top contributing words component.
        
        Args:
            attention_data: Dictionary containing attention analysis data
        """
        if not attention_data or "top_contributing_words" not in attention_data:
            return
        
        top_words = attention_data.get("top_contributing_words", [])
        if not top_words:
            return
        
        st.subheader("🏆 Top Contributing Words")
        
        # Create columns for positive and negative contributions
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔴 Negative Contributors:**")
            negative_words = [word for word in top_words if word["score"] < 0]
            if negative_words:
                for i, word in enumerate(negative_words[:5], 1):
                    st.markdown(f"{i}. **{word['token']}** (Score: {word['score']:.3f})")
            else:
                st.markdown("*No significant negative contributors*")
        
        with col2:
            st.markdown("**🟢 Positive Contributors:**")
            positive_words = [word for word in top_words if word["score"] > 0]
            if positive_words:
                for i, word in enumerate(positive_words[:5], 1):
                    st.markdown(f"{i}. **{word['token']}** (Score: {word['score']:.3f})")
            else:
                st.markdown("*No significant positive contributors*")
        
        # Create a summary chart
        self._render_contribution_chart(top_words)
    
    def _render_contribution_chart(self, top_words: List[Dict]) -> None:
        """Render a chart showing the top contributing words."""
        if len(top_words) < 2:
            return
        
        # Prepare data for the chart
        tokens = [word["token"] for word in top_words[:10]]
        scores = [word["score"] for word in top_words[:10]]
        colors = ["red" if score < 0 else "green" for score in scores]
        
        # Create horizontal bar chart
        fig = go.Figure(data=go.Bar(
            y=tokens,
            x=scores,
            orientation='h',
            marker_color=colors,
            text=[f"{score:.3f}" for score in scores],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Top 10 Word Contributions",
            xaxis_title="Contribution Score",
            yaxis_title="Words",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

class AttentionVisualization:
    """
    Main attention visualization component that combines all attention features.
    """
    
    def __init__(self):
        """Initialize the attention visualization component."""
        self.heatmap = WordAttentionHeatmap()
        self.top_words = TopContributingWords()
    
    def render(self, result: Dict[str, Any]) -> None:
        """
        Render the complete attention visualization.
        
        Args:
            result: Dictionary containing sentiment analysis results with attention data
        """
        if not result:
            st.error("No results to visualize")
            return
        
        # Check if attention data is available
        if "attention_weights" not in result:
            st.info("Enable attention analysis in the sidebar to see word-level explanations")
            return
        
        sentiment_label = result.get("sentiment_label", "unknown")
        
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["🎨 Attention Heatmap", "🏆 Top Contributors", "📊 Summary"])
        
        with tab1:
            self.heatmap.render(result, sentiment_label)
        
        with tab2:
            self.top_words.render(result)
        
        with tab3:
            self._render_summary(result, sentiment_label)
    
    def _render_summary(self, result: Dict[str, Any], sentiment_label: str) -> None:
        """Render a summary of the attention analysis."""
        st.subheader("📊 Attention Analysis Summary")
        
        attention_weights = result.get("attention_weights", [])
        if not attention_weights:
            st.warning("No attention data available")
            return
        
        # Calculate summary statistics
        attention_scores = [item["attention_score"] for item in attention_weights]
        contribution_scores = [item["contribution_score"] for item in attention_weights]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Words Analyzed", len(attention_weights))
        
        with col2:
            avg_attention = np.mean(attention_scores)
            st.metric("Average Attention", f"{avg_attention:.3f}")
        
        with col3:
            max_attention = max(attention_scores)
            st.metric("Max Attention", f"{max_attention:.3f}")
        
        with col4:
            positive_words = len([s for s in contribution_scores if s > 0])
            st.metric("Positive Contributors", positive_words)
        
        # Show key insights
        st.markdown("**🔍 Key Insights:**")
        
        # Find the most influential words
        if contribution_scores:
            max_positive = max(contribution_scores)
            max_negative = min(contribution_scores)
            
            if max_positive > 0:
                positive_word = next(item["token"] for item in attention_weights 
                                   if item["contribution_score"] == max_positive)
                st.markdown(f"- **Most positive word**: '{positive_word}' (Score: {max_positive:.3f})")
            
            if max_negative < 0:
                negative_word = next(item["token"] for item in attention_weights 
                                   if item["contribution_score"] == max_negative)
                st.markdown(f"- **Most negative word**: '{negative_word}' (Score: {max_negative:.3f})")
        
        # Show confidence correlation
        confidence_score = result.get("confidence_score", 0.0)
        st.markdown(f"- **Model confidence**: {confidence_score:.1%}")
        st.markdown(f"- **Predicted sentiment**: {sentiment_label.capitalize()}")
