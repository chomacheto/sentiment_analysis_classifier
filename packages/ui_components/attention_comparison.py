"""
Attention Comparison Component

This module provides components for comparing attention visualizations between
different sentiment predictions, allowing side-by-side analysis of word-level attention.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from .attention_visualization import WordAttentionHeatmap

class AttentionComparison:
    """
    Component for comparing attention visualizations between different predictions.
    
    Features:
    - Side-by-side attention comparison
    - Attention difference visualization
    - Toggle between single and comparison views
    - Integration with existing confidence metrics
    """
    
    def __init__(self):
        """Initialize the attention comparison component."""
        self.heatmap = WordAttentionHeatmap()
        
        # Color scheme for comparison visualization
        self.comparison_colors = {
            "positive": "#4caf50",
            "negative": "#f44336",
            "neutral": "#9e9e9e",
            "difference": "#ff9800"
        }
    
    def render(self, current_result: Dict[str, Any], comparison_result: Optional[Dict[str, Any]] = None) -> None:
        """
        Render the attention comparison component.
        
        Args:
            current_result: Current sentiment analysis result with attention data
            comparison_result: Optional comparison result for side-by-side analysis
        """
        if not current_result:
            st.error("No current result to compare")
            return
        
        # Check if attention data is available
        if "attention_weights" not in current_result:
            st.info("Enable attention analysis to use comparison features")
            return
        
        # Create tabs for different comparison views
        tab1, tab2 = st.tabs(["📊 Current Analysis", "🔄 Comparison Mode"])
        
        with tab1:
            self._render_single_analysis(current_result)
        
        with tab2:
            if comparison_result and "attention_weights" in comparison_result:
                self._render_comparison_analysis(current_result, comparison_result)
            else:
                self._render_comparison_setup(current_result)
    
    def _render_single_analysis(self, result: Dict[str, Any]) -> None:
        """Render single analysis view."""
        st.subheader("📊 Current Attention Analysis")
        
        sentiment_label = result.get("sentiment_label", "unknown")
        confidence_score = result.get("confidence_score", 0.0)
        
        # Display current sentiment info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Sentiment", sentiment_label.capitalize())
        
        with col2:
            st.metric("Confidence", f"{confidence_score:.1%}")
        
        with col3:
            attention_weights = result.get("attention_weights", [])
            st.metric("Words Analyzed", len(attention_weights))
        
        # Show attention heatmap
        self.heatmap.render(result, sentiment_label)
    
    def _render_comparison_setup(self, current_result: Dict[str, Any]) -> None:
        """Render comparison setup when no comparison data is available."""
        st.subheader("🔄 Comparison Mode")
        
        st.info("""
        **Comparison Mode Setup:**
        
        To compare attention visualizations, you can:
        1. **Analyze a different text** - Enter new text and compare with current analysis
        2. **Compare with previous analysis** - Select from your analysis history
        3. **Load comparison data** - Import attention data from external sources
        """)
        
        # Option 1: Analyze different text
        st.markdown("**Option 1: Analyze Different Text**")
        comparison_text = st.text_area(
            "Enter text to compare:",
            placeholder="Enter text for comparison analysis...",
            height=100
        )
        
        if st.button("🔍 Analyze for Comparison", disabled=not comparison_text.strip()):
            # Store comparison text in session state for processing
            st.session_state.comparison_text = comparison_text.strip()
            st.session_state.show_comparison_analysis = True
            st.rerun()
        
        # Option 2: Compare with history
        st.markdown("**Option 2: Compare with History**")
        if st.session_state.get('analysis_history'):
            history_options = []
            for i, analysis in enumerate(st.session_state.analysis_history[-5:], 1):
                text_preview = analysis['input_text'][:50] + "..." if len(analysis['input_text']) > 50 else analysis['input_text']
                history_options.append(f"{i}. {text_preview}")
            
            selected_history = st.selectbox(
                "Select from recent analyses:",
                ["None"] + history_options
            )
            
            if selected_history != "None" and st.button("🔄 Compare with Selected"):
                # Get the selected analysis
                selected_index = int(selected_history.split('.')[0]) - 1
                selected_analysis = st.session_state.analysis_history[-(5-selected_index)]
                st.session_state.comparison_result = selected_analysis['result']
                st.rerun()
    
    def _render_comparison_analysis(self, current_result: Dict[str, Any], comparison_result: Dict[str, Any]) -> None:
        """Render side-by-side comparison analysis."""
        st.subheader("🔄 Side-by-Side Comparison")
        
        # Display comparison overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Current Analysis**")
            current_sentiment = current_result.get("sentiment_label", "unknown")
            current_confidence = current_result.get("confidence_score", 0.0)
            st.metric("Sentiment", current_sentiment.capitalize())
            st.metric("Confidence", f"{current_confidence:.1%}")
        
        with col2:
            st.markdown("**📊 Comparison Analysis**")
            comp_sentiment = comparison_result.get("sentiment_label", "unknown")
            comp_confidence = comparison_result.get("confidence_score", 0.0)
            st.metric("Sentiment", comp_sentiment.capitalize())
            st.metric("Confidence", f"{comp_confidence:.1%}")
        
        # Create comparison tabs
        tab1, tab2, tab3 = st.tabs(["📈 Attention Comparison", "🔍 Word Differences", "📊 Summary"])
        
        with tab1:
            self._render_attention_comparison(current_result, comparison_result)
        
        with tab2:
            self._render_word_differences(current_result, comparison_result)
        
        with tab3:
            self._render_comparison_summary(current_result, comparison_result)
    
    def _render_attention_comparison(self, current_result: Dict[str, Any], comparison_result: Dict[str, Any]) -> None:
        """Render attention comparison visualization."""
        st.subheader("📈 Attention Score Comparison")
        
        current_weights = current_result.get("attention_weights", [])
        comparison_weights = comparison_result.get("attention_weights", [])
        
        if not current_weights or not comparison_weights:
            st.warning("Insufficient attention data for comparison")
            return
        
        # Create comparison chart
        self._create_comparison_chart(current_weights, comparison_weights)
        
        # Show attention difference heatmap
        self._render_attention_difference(current_weights, comparison_weights)
    
    def _create_comparison_chart(self, current_weights: List[Dict], comparison_weights: List[Dict]) -> None:
        """Create a comparison chart showing attention scores side by side."""
        # Get common words for comparison
        current_tokens = {item["token"]: item["attention_score"] for item in current_weights}
        comparison_tokens = {item["token"]: item["attention_score"] for item in comparison_weights}
        
        # Find common tokens
        common_tokens = list(set(current_tokens.keys()) & set(comparison_tokens.keys()))
        
        if len(common_tokens) < 2:
            st.info("Not enough common words for meaningful comparison")
            return
        
        # Prepare data for chart
        tokens = common_tokens[:10]  # Limit to top 10 for readability
        current_scores = [current_tokens[token] for token in tokens]
        comparison_scores = [comparison_tokens[token] for token in tokens]
        
        # Create grouped bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name="Current Analysis",
            x=tokens,
            y=current_scores,
            marker_color=self.comparison_colors["positive"]
        ))
        
        fig.add_trace(go.Bar(
            name="Comparison Analysis",
            x=tokens,
            y=comparison_scores,
            marker_color=self.comparison_colors["negative"]
        ))
        
        fig.update_layout(
            title="Attention Score Comparison",
            xaxis_title="Words",
            yaxis_title="Attention Score",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_attention_difference(self, current_weights: List[Dict], comparison_weights: List[Dict]) -> None:
        """Render attention difference visualization."""
        st.subheader("🔍 Attention Differences")
        
        # Calculate attention differences
        current_dict = {item["token"]: item["attention_score"] for item in current_weights}
        comparison_dict = {item["token"]: item["attention_score"] for item in comparison_weights}
        
        # Find all unique tokens
        all_tokens = list(set(current_dict.keys()) | set(comparison_dict.keys()))
        
        differences = []
        for token in all_tokens:
            current_score = current_dict.get(token, 0.0)
            comparison_score = comparison_dict.get(token, 0.0)
            difference = current_score - comparison_score
            
            differences.append({
                "token": token,
                "current_score": current_score,
                "comparison_score": comparison_score,
                "difference": difference
            })
        
        # Sort by absolute difference
        differences.sort(key=lambda x: abs(x["difference"]), reverse=True)
        
        # Display top differences
        st.markdown("**Top Attention Differences:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔴 Higher in Current Analysis:**")
            positive_diffs = [d for d in differences[:5] if d["difference"] > 0]
            for diff in positive_diffs:
                st.markdown(f"- **{diff['token']}**: +{diff['difference']:.3f}")
        
        with col2:
            st.markdown("**🟢 Higher in Comparison Analysis:**")
            negative_diffs = [d for d in differences[:5] if d["difference"] < 0]
            for diff in negative_diffs:
                st.markdown(f"- **{diff['token']}**: {diff['difference']:.3f}")
        
        # Create difference chart
        if differences:
            self._create_difference_chart(differences[:10])
    
    def _create_difference_chart(self, differences: List[Dict]) -> None:
        """Create a chart showing attention differences."""
        tokens = [d["token"] for d in differences]
        diff_values = [d["difference"] for d in differences]
        
        # Color based on difference direction
        colors = []
        for diff in diff_values:
            if diff > 0:
                colors.append(self.comparison_colors["positive"])
            elif diff < 0:
                colors.append(self.comparison_colors["negative"])
            else:
                colors.append(self.comparison_colors["neutral"])
        
        fig = go.Figure(data=go.Bar(
            x=tokens,
            y=diff_values,
            marker_color=colors,
            text=[f"{diff:.3f}" for diff in diff_values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Attention Score Differences (Current - Comparison)",
            xaxis_title="Words",
            yaxis_title="Difference",
            height=400,
            showlegend=False
        )
        
        # Add horizontal line at zero
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_word_differences(self, current_result: Dict[str, Any], comparison_result: Dict[str, Any]) -> None:
        """Render detailed word-level differences."""
        st.subheader("🔍 Word-Level Differences")
        
        current_contributions = current_result.get("word_contributions", [])
        comparison_contributions = comparison_result.get("word_contributions", [])
        
        if not current_contributions or not comparison_contributions:
            st.warning("No word contribution data available for comparison")
            return
        
        # Create word contribution comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Current Analysis - Top Contributors:**")
            for i, word in enumerate(current_contributions[:5], 1):
                score = word["score"]
                color = "🟢" if score > 0 else "🔴"
                st.markdown(f"{i}. {color} **{word['token']}** ({score:.3f})")
        
        with col2:
            st.markdown("**📊 Comparison Analysis - Top Contributors:**")
            for i, word in enumerate(comparison_contributions[:5], 1):
                score = word["score"]
                color = "🟢" if score > 0 else "🔴"
                st.markdown(f"{i}. {color} **{word['token']}** ({score:.3f})")
    
    def _render_comparison_summary(self, current_result: Dict[str, Any], comparison_result: Dict[str, Any]) -> None:
        """Render comparison summary statistics."""
        st.subheader("📊 Comparison Summary")
        
        # Calculate summary statistics
        current_weights = current_result.get("attention_weights", [])
        comparison_weights = comparison_result.get("attention_weights", [])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_avg = np.mean([w["attention_score"] for w in current_weights]) if current_weights else 0
            st.metric("Current Avg Attention", f"{current_avg:.3f}")
        
        with col2:
            comp_avg = np.mean([w["attention_score"] for w in comparison_weights]) if comparison_weights else 0
            st.metric("Comparison Avg Attention", f"{comp_avg:.3f}")
        
        with col3:
            current_max = max([w["attention_score"] for w in current_weights]) if current_weights else 0
            st.metric("Current Max Attention", f"{current_max:.3f}")
        
        with col4:
            comp_max = max([w["attention_score"] for w in comparison_weights]) if comparison_weights else 0
            st.metric("Comparison Max Attention", f"{comp_max:.3f}")
        
        # Key insights
        st.markdown("**🔍 Key Insights:**")
        
        current_sentiment = current_result.get("sentiment_label", "unknown")
        comp_sentiment = comparison_result.get("sentiment_label", "unknown")
        
        if current_sentiment != comp_sentiment:
            st.markdown(f"- **Sentiment Change**: {current_sentiment.capitalize()} → {comp_sentiment.capitalize()}")
        
        current_conf = current_result.get("confidence_score", 0.0)
        comp_conf = comparison_result.get("confidence_score", 0.0)
        conf_diff = current_conf - comp_conf
        
        if abs(conf_diff) > 0.1:
            direction = "higher" if conf_diff > 0 else "lower"
            st.markdown(f"- **Confidence**: Current analysis is {direction} by {abs(conf_diff):.1%}")
        
        # Word overlap analysis
        current_tokens = set(w["token"] for w in current_weights)
        comp_tokens = set(w["token"] for w in comparison_weights)
        overlap = len(current_tokens & comp_tokens)
        total_unique = len(current_tokens | comp_tokens)
        
        if total_unique > 0:
            overlap_percentage = (overlap / total_unique) * 100
            st.markdown(f"- **Word Overlap**: {overlap_percentage:.1f}% of words are common")
        
        # Close comparison button
        if st.button("❌ Close Comparison", help="Return to single analysis view"):
            st.session_state.comparison_result = None
            st.session_state.show_comparison_analysis = False
            st.rerun()
