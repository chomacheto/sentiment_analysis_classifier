"""
Tests for Attention Visualization Components

This module contains unit tests for the attention visualization components
including WordAttentionHeatmap, TopContributingWords, and AttentionVisualization.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.ui_components.attention_visualization import (
    WordAttentionHeatmap,
    TopContributingWords,
    AttentionVisualization
)

class TestWordAttentionHeatmap:
    """Test cases for WordAttentionHeatmap component."""
    
    def test_initialization(self):
        """Test that the component initializes correctly."""
        heatmap = WordAttentionHeatmap()
        assert heatmap is not None
        assert hasattr(heatmap, 'attention_colors')
        assert 'positive' in heatmap.attention_colors
        assert 'negative' in heatmap.attention_colors
        assert 'neutral' in heatmap.attention_colors
    
    def test_render_with_valid_data(self):
        """Test rendering with valid attention data."""
        heatmap = WordAttentionHeatmap()
        
        # Mock attention data
        attention_data = {
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4},
                {"token": "terrible", "attention_score": 0.9, "contribution_score": -0.7}
            ]
        }
        
        # This should not raise any exceptions
        try:
            heatmap.render(attention_data, "positive")
            assert True  # If we get here, no exception was raised
        except Exception as e:
            pytest.fail(f"Render method raised an exception: {e}")
    
    def test_render_with_empty_data(self):
        """Test rendering with empty attention data."""
        heatmap = WordAttentionHeatmap()
        
        # Empty data
        empty_data = {}
        
        # This should not raise any exceptions
        try:
            heatmap.render(empty_data, "positive")
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with empty data: {e}")
    
    def test_render_with_no_attention_weights(self):
        """Test rendering when attention_weights is missing."""
        heatmap = WordAttentionHeatmap()
        
        # Data without attention_weights
        data_without_weights = {"other_data": "value"}
        
        # This should not raise any exceptions
        try:
            heatmap.render(data_without_weights, "positive")
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception without attention_weights: {e}")
    
    def test_color_mapping(self):
        """Test that color mapping works correctly for different contribution scores."""
        heatmap = WordAttentionHeatmap()
        
        # Test positive contributions
        positive_colors = []
        for score in [0.05, 0.2, 0.4]:  # low, medium, high
            if score < 0.1:
                intensity = "low"
            elif score < 0.3:
                intensity = "medium"
            else:
                intensity = "high"
            positive_colors.append(heatmap.attention_colors["positive"][intensity])
        
        assert len(positive_colors) == 3
        assert all(color.startswith('#') for color in positive_colors)
        
        # Test negative contributions
        negative_colors = []
        for score in [-0.05, -0.2, -0.4]:  # low, medium, high
            if abs(score) < 0.1:
                intensity = "low"
            elif abs(score) < 0.3:
                intensity = "medium"
            else:
                intensity = "high"
            negative_colors.append(heatmap.attention_colors["negative"][intensity])
        
        assert len(negative_colors) == 3
        assert all(color.startswith('#') for color in negative_colors)

class TestTopContributingWords:
    """Test cases for TopContributingWords component."""
    
    def test_initialization(self):
        """Test that the component initializes correctly."""
        top_words = TopContributingWords()
        assert top_words is not None
    
    def test_render_with_valid_data(self):
        """Test rendering with valid top contributing words data."""
        top_words = TopContributingWords()
        
        # Mock attention data with top contributing words
        attention_data = {
            "top_contributing_words": [
                {"token": "amazing", "score": 0.8},
                {"token": "fantastic", "score": 0.7},
                {"token": "terrible", "score": -0.6},
                {"token": "awful", "score": -0.5}
            ]
        }
        
        # This should not raise any exceptions
        try:
            top_words.render(attention_data)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception: {e}")
    
    def test_render_with_empty_data(self):
        """Test rendering with empty data."""
        top_words = TopContributingWords()
        
        # Empty data
        empty_data = {}
        
        # This should not raise any exceptions
        try:
            top_words.render(empty_data)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with empty data: {e}")
    
    def test_render_with_no_top_words(self):
        """Test rendering when top_contributing_words is missing."""
        top_words = TopContributingWords()
        
        # Data without top_contributing_words
        data_without_top_words = {"other_data": "value"}
        
        # This should not raise any exceptions
        try:
            top_words.render(data_without_top_words)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception without top_contributing_words: {e}")
    
    def test_contribution_chart_with_sufficient_data(self):
        """Test that contribution chart renders with sufficient data."""
        top_words = TopContributingWords()
        
        # Data with enough words for chart
        attention_data = {
            "top_contributing_words": [
                {"token": "word1", "score": 0.8},
                {"token": "word2", "score": 0.7},
                {"token": "word3", "score": -0.6}
            ]
        }
        
        # This should not raise any exceptions
        try:
            top_words.render(attention_data)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with sufficient data: {e}")

class TestAttentionVisualization:
    """Test cases for AttentionVisualization component."""
    
    def test_initialization(self):
        """Test that the component initializes correctly."""
        viz = AttentionVisualization()
        assert viz is not None
        assert hasattr(viz, 'heatmap')
        assert hasattr(viz, 'top_words')
        assert isinstance(viz.heatmap, WordAttentionHeatmap)
        assert isinstance(viz.top_words, TopContributingWords)
    
    def test_render_with_valid_data(self):
        """Test rendering with valid attention data."""
        viz = AttentionVisualization()
        
        # Mock complete attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "excellent", "attention_score": 0.9, "contribution_score": 0.8},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4},
                {"token": "amazing", "attention_score": 0.8, "contribution_score": 0.7}
            ],
            "top_contributing_words": [
                {"token": "excellent", "score": 0.8},
                {"token": "amazing", "score": 0.7},
                {"token": "movie", "score": 0.4}
            ]
        }
        
        # This should not raise any exceptions
        try:
            viz.render(result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception: {e}")
    
    def test_render_without_attention_data(self):
        """Test rendering without attention data."""
        viz = AttentionVisualization()
        
        # Result without attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85
        }
        
        # This should not raise any exceptions
        try:
            viz.render(result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception without attention data: {e}")
    
    def test_render_with_empty_result(self):
        """Test rendering with empty result."""
        viz = AttentionVisualization()
        
        # Empty result
        empty_result = {}
        
        # This should not raise any exceptions
        try:
            viz.render(empty_result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with empty result: {e}")
    
    def test_render_with_none_result(self):
        """Test rendering with None result."""
        viz = AttentionVisualization()
        
        # None result
        none_result = None
        
        # This should not raise any exceptions
        try:
            viz.render(none_result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with None result: {e}")
    
    def test_summary_calculation(self):
        """Test that summary statistics are calculated correctly."""
        viz = AttentionVisualization()
        
        # Mock data for summary calculation
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "word1", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "word2", "attention_score": 0.6, "contribution_score": 0.4},
                {"token": "word3", "attention_score": 0.4, "contribution_score": -0.2}
            ]
        }
        
        # This should not raise any exceptions
        try:
            viz.render(result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception during summary calculation: {e}")

class TestIntegration:
    """Integration tests for attention visualization components."""
    
    def test_component_integration(self):
        """Test that all components work together correctly."""
        # Test data
        test_data = {
            "sentiment_label": "positive",
            "confidence_score": 0.9,
            "attention_weights": [
                {"token": "fantastic", "attention_score": 0.95, "contribution_score": 0.9},
                {"token": "performance", "attention_score": 0.7, "contribution_score": 0.5},
                {"token": "brilliant", "attention_score": 0.8, "contribution_score": 0.7}
            ],
            "top_contributing_words": [
                {"token": "fantastic", "score": 0.9},
                {"token": "brilliant", "score": 0.7},
                {"token": "performance", "score": 0.5}
            ]
        }
        
        # Test each component individually
        heatmap = WordAttentionHeatmap()
        top_words = TopContributingWords()
        viz = AttentionVisualization()
        
        # All should work without exceptions
        try:
            heatmap.render(test_data, "positive")
            top_words.render(test_data)
            viz.render(test_data)
            assert True
        except Exception as e:
            pytest.fail(f"Integration test failed: {e}")
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        # Test with minimal data
        minimal_data = {
            "sentiment_label": "neutral",
            "confidence_score": 0.5,
            "attention_weights": [],
            "top_contributing_words": []
        }
        
        viz = AttentionVisualization()
        
        # Should handle empty attention data gracefully
        try:
            viz.render(minimal_data)
            assert True
        except Exception as e:
            pytest.fail(f"Edge case test failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
