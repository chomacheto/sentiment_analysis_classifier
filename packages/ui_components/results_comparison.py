"""
Results Comparison Component for Educational Analysis

This component displays expected vs. actual sentiment analysis results
for educational purposes, showing confidence scores and attention visualizations.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
import json
from pathlib import Path


class ResultsComparison:
    """Component for comparing expected vs. actual sentiment analysis results."""
    
    def __init__(self, sample_data_path: str = "data/samples/sample_data.json"):
        """Initialize the ResultsComparison component.
        
        Args:
            sample_data_path: Path to the sample data JSON file
        """
        self.sample_data_path = Path(sample_data_path)
        self.samples = self._load_sample_data()
        
    def _load_sample_data(self) -> List[Dict[str, Any]]:
        """Load sample data from JSON file.
        
        Returns:
            List of sample data dictionaries
        """
        try:
            with open(self.sample_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('samples', [])
        except FileNotFoundError:
            st.error(f"Sample data file not found: {self.sample_data_path}")
            return []
        except json.JSONDecodeError:
            st.error(f"Invalid JSON in sample data file: {self.sample_data_path}")
            return []
    
    def render_comparison(self, 
                         sample_id: str, 
                         actual_result: Dict[str, Any],
                         attention_data: Optional[Dict[str, Any]] = None) -> None:
        """Render the comparison between expected and actual results.
        
        Args:
            sample_id: ID of the sample being analyzed
            actual_result: Actual sentiment analysis result
            attention_data: Optional attention visualization data
        """
        # Find the sample
        sample = self._get_sample_by_id(sample_id)
        if not sample:
            st.error(f"Sample with ID '{sample_id}' not found.")
            return
        
        st.subheader("🔍 Expected vs. Actual Results Comparison")
        st.markdown("Compare the expected sentiment with the model's prediction and understand the differences.")
        
        # Create comparison layout
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_expected_result(sample)
        
        with col2:
            self._render_actual_result(actual_result)
        
        # Comparison analysis
        self._render_comparison_analysis(sample, actual_result)
        
        # Attention visualization if available
        if attention_data:
            self._render_attention_analysis(attention_data, sample)
        
        # Learning insights
        self._render_learning_insights(sample, actual_result)
    
    def _get_sample_by_id(self, sample_id: str) -> Optional[Dict[str, Any]]:
        """Get a sample by its ID.
        
        Args:
            sample_id: ID of the sample to retrieve
            
        Returns:
            Sample data dictionary or None if not found
        """
        for sample in self.samples:
            if sample['id'] == sample_id:
                return sample
        return None
    
    def _render_expected_result(self, sample: Dict[str, Any]) -> None:
        """Render the expected result section.
        
        Args:
            sample: Sample data dictionary
        """
        st.markdown("### 📋 Expected Result")
        
        # Expected sentiment
        expected_sentiment = sample['expected_sentiment']
        sentiment_color = self._get_sentiment_color(expected_sentiment)
        
        st.markdown(f"""
        <div style="padding: 16px; border: 2px solid {sentiment_color}; border-radius: 8px; background-color: {sentiment_color}20;">
            <h4 style="margin: 0; color: {sentiment_color};">Expected Sentiment: {expected_sentiment.title()}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample metadata
        st.markdown("**Sample Information:**")
        st.markdown(f"- **Category:** {sample['category']}")
        st.markdown(f"- **Difficulty:** {sample['difficulty_level']}")
        st.markdown(f"- **Source:** {sample['source']}")
        
        # Sample text
        st.markdown("**Sample Text:**")
        st.text_area(
            "Text:",
            value=sample['text'],
            height=120,
            key="expected_text",
            disabled=True
        )
    
    def _render_actual_result(self, actual_result: Dict[str, Any]) -> None:
        """Render the actual result section.
        
        Args:
            actual_result: Actual sentiment analysis result
        """
        st.markdown("### 🤖 Model Prediction")
        
        # Actual sentiment
        actual_sentiment = actual_result.get('sentiment_label', 'unknown')
        confidence = actual_result.get('confidence_score', 0.0)
        sentiment_color = self._get_sentiment_color(actual_sentiment)
        
        st.markdown(f"""
        <div style="padding: 16px; border: 2px solid {sentiment_color}; border-radius: 8px; background-color: {sentiment_color}20;">
            <h4 style="margin: 0; color: {sentiment_color};">Predicted Sentiment: {actual_sentiment.title()}</h4>
            <p style="margin: 8px 0 0 0; font-size: 14px;">Confidence: {confidence:.2%}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Processing time
        processing_time = actual_result.get('processing_time_ms', 0)
        st.markdown(f"**Processing Time:** {processing_time}ms")
        
        # Confidence gauge
        self._render_confidence_gauge(confidence)
    
    def _render_confidence_gauge(self, confidence: float) -> None:
        """Render a confidence gauge visualization.
        
        Args:
            confidence: Confidence score (0.0 to 1.0)
        """
        st.markdown("**Confidence Level:**")
        
        # Color based on confidence level
        if confidence >= 0.8:
            color = "#4CAF50"  # Green
        elif confidence >= 0.6:
            color = "#FF9800"  # Orange
        else:
            color = "#F44336"  # Red
        
        # Progress bar
        st.progress(confidence)
        st.markdown(f"<span style='color: {color}; font-weight: bold;'>{confidence:.1%}</span>", 
                   unsafe_allow_html=True)
    
    def _render_comparison_analysis(self, sample: Dict[str, Any], actual_result: Dict[str, Any]) -> None:
        """Render the comparison analysis section.
        
        Args:
            sample: Sample data dictionary
            actual_result: Actual sentiment analysis result
        """
        st.markdown("### 📊 Comparison Analysis")
        
        expected = sample['expected_sentiment']
        actual = actual_result.get('sentiment_label', 'unknown')
        confidence = actual_result.get('confidence_score', 0.0)
        
        # Match status
        is_match = expected.lower() == actual.lower()
        status_color = "#4CAF50" if is_match else "#F44336"
        status_text = "✅ Match" if is_match else "❌ Mismatch"
        
        st.markdown(f"""
        <div style="padding: 16px; border: 2px solid {status_color}; border-radius: 8px; background-color: {status_color}20;">
            <h4 style="margin: 0; color: {status_color};">{status_text}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Comparison table
        comparison_data = {
            'Metric': ['Expected Sentiment', 'Predicted Sentiment', 'Confidence', 'Match Status'],
            'Value': [expected.title(), actual.title(), f"{confidence:.1%}", status_text]
        }
        
        df = pd.DataFrame(comparison_data)
        st.table(df)
        
        # Analysis explanation
        if not is_match:
            self._render_mismatch_analysis(sample, actual_result)
    
    def _render_mismatch_analysis(self, sample: Dict[str, Any], actual_result: Dict[str, Any]) -> None:
        """Render analysis for mismatched predictions.
        
        Args:
            sample: Sample data dictionary
            actual_result: Actual sentiment analysis result
        """
        st.markdown("#### 🔍 Why the Mismatch?")
        
        expected = sample['expected_sentiment']
        actual = actual_result.get('sentiment_label', 'unknown')
        difficulty = sample['difficulty_level']
        
        # Common reasons for mismatches
        reasons = []
        
        if difficulty == 'hard':
            reasons.append("**High difficulty level** - This sample contains complex language patterns")
        
        if sample['category'] == 'sarcasm':
            reasons.append("**Sarcasm detection** - The model may struggle with ironic language")
        
        if sample['category'] == 'social_media':
            reasons.append("**Informal language** - Social media posts often use slang and abbreviations")
        
        if 'mixed' in sample['id']:
            reasons.append("**Mixed sentiment** - The text contains both positive and negative elements")
        
        if confidence < 0.7:
            reasons.append("**Low confidence** - The model is uncertain about this prediction")
        
        if reasons:
            st.markdown("Possible reasons for the mismatch:")
            for reason in reasons:
                st.markdown(f"- {reason}")
        else:
            st.markdown("The model's prediction differs from the expected result. This could be due to:")
            st.markdown("- Subtle language nuances")
            st.markdown("- Context-dependent meaning")
            st.markdown("- Model training data differences")
    
    def _render_attention_analysis(self, attention_data: Dict[str, Any], sample: Dict[str, Any]) -> None:
        """Render attention analysis section.
        
        Args:
            attention_data: Attention visualization data
            sample: Sample data dictionary
        """
        st.markdown("### 🎯 Attention Analysis")
        st.markdown("See which words the model focused on when making its prediction.")
        
        # This would integrate with the existing attention visualization component
        # For now, show a placeholder
        st.info("Attention visualization would be displayed here, showing word-level attention scores.")
        
        # You can integrate with the existing attention visualization component:
        # from packages.ui_components.attention_visualization import AttentionVisualization
        # attention_viz = AttentionVisualization()
        # attention_viz.render(attention_data)
    
    def _render_learning_insights(self, sample: Dict[str, Any], actual_result: Dict[str, Any]) -> None:
        """Render learning insights and tips.
        
        Args:
            sample: Sample data dictionary
            actual_result: Actual sentiment analysis result
        """
        st.markdown("### 💡 Learning Insights")
        
        expected = sample['expected_sentiment']
        actual = actual_result.get('sentiment_label', 'unknown')
        category = sample['category']
        
        # Category-specific insights
        insights = self._get_category_insights(category)
        
        st.markdown("**Understanding this text type:**")
        for insight in insights:
            st.markdown(f"- {insight}")
        
        # General tips
        st.markdown("**General tips for sentiment analysis:**")
        st.markdown("- Consider the context and source of the text")
        st.markdown("- Look for emotional words and phrases")
        st.markdown("- Be aware of sarcasm and irony")
        st.markdown("- Consider cultural and regional differences")
        st.markdown("- Pay attention to the overall tone and structure")
    
    def _get_category_insights(self, category: str) -> List[str]:
        """Get insights specific to a text category.
        
        Args:
            category: Text category
            
        Returns:
            List of insights for the category
        """
        insights_map = {
            'movie_review': [
                "Movie reviews often contain specific technical terms (acting, cinematography, plot)",
                "Look for comparative language and recommendations",
                "Consider the reviewer's expertise level"
            ],
            'social_media': [
                "Social media posts use informal language and abbreviations",
                "Emojis and hashtags can indicate sentiment",
                "Context is often limited due to character constraints"
            ],
            'formal': [
                "Formal documents use objective, professional language",
                "Sentiment may be subtle and context-dependent",
                "Focus on factual content rather than emotional expression"
            ],
            'sarcasm': [
                "Sarcasm often uses positive words to express negative sentiment",
                "Look for exaggeration and irony markers",
                "Context and background knowledge are crucial"
            ],
            'feedback': [
                "Customer feedback often includes specific details and experiences",
                "Look for actionable suggestions and recommendations",
                "Consider the credibility and authenticity of the review"
            ],
            'news': [
                "News articles may mix factual reporting with editorial bias",
                "Consider the source and potential bias",
                "Distinguish between breaking news and analysis pieces"
            ],
            'technical': [
                "Technical content focuses on functionality and performance",
                "Objective language is common, but sentiment can be subtle",
                "Consider the technical expertise level of the audience"
            ],
            'emotional': [
                "Personal expressions often contain strong emotional language",
                "Consider the personal context and background",
                "Handle with sensitivity, especially for mental health content"
            ]
        }
        
        return insights_map.get(category, ["This text type has unique characteristics that affect sentiment analysis."])
    
    def _get_sentiment_color(self, sentiment: str) -> str:
        """Get color for sentiment display.
        
        Args:
            sentiment: Sentiment label
            
        Returns:
            Hex color code
        """
        color_map = {
            'positive': '#4CAF50',  # Green
            'negative': '#F44336',  # Red
            'neutral': '#2196F3',   # Blue
            'unknown': '#9E9E9E'    # Gray
        }
        
        return color_map.get(sentiment.lower(), '#9E9E9E')
    
    def render_batch_comparison(self, results: List[Tuple[str, Dict[str, Any]]]) -> None:
        """Render comparison for multiple samples.
        
        Args:
            results: List of (sample_id, actual_result) tuples
        """
        st.subheader("📊 Batch Results Comparison")
        
        # Create comparison table
        comparison_data = []
        
        for sample_id, actual_result in results:
            sample = self._get_sample_by_id(sample_id)
            if sample:
                expected = sample['expected_sentiment']
                actual = actual_result.get('sentiment_label', 'unknown')
                confidence = actual_result.get('confidence_score', 0.0)
                is_match = expected.lower() == actual.lower()
                
                comparison_data.append({
                    'Sample ID': sample_id,
                    'Category': sample['category'],
                    'Expected': expected.title(),
                    'Predicted': actual.title(),
                    'Confidence': f"{confidence:.1%}",
                    'Match': '✅' if is_match else '❌'
                })
        
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            st.table(df)
            
            # Summary statistics
            total = len(comparison_data)
            matches = sum(1 for row in comparison_data if row['Match'] == '✅')
            accuracy = matches / total if total > 0 else 0
            
            st.markdown(f"**Summary:** {matches}/{total} correct predictions ({accuracy:.1%} accuracy)")


def render_results_comparison(sample_id: str, 
                            actual_result: Dict[str, Any], 
                            attention_data: Optional[Dict[str, Any]] = None) -> None:
    """Convenience function to render results comparison.
    
    Args:
        sample_id: ID of the sample being analyzed
        actual_result: Actual sentiment analysis result
        attention_data: Optional attention visualization data
    """
    comparison = ResultsComparison()
    comparison.render_comparison(sample_id, actual_result, attention_data)


if __name__ == "__main__":
    # Test the component
    test_result = {
        'sentiment_label': 'positive',
        'confidence_score': 0.85,
        'processing_time_ms': 1200
    }
    
    render_results_comparison('movie_review_1', test_result)
