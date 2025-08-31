"""
Tests for Attention Comparison Component

This module contains unit tests for the attention comparison component
including AttentionComparison class and its functionality.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.ui_components.attention_comparison import AttentionComparison

class TestAttentionComparison:
    """Test cases for AttentionComparison component."""
    
    def test_initialization(self):
        """Test that the component initializes correctly."""
        comparison = AttentionComparison()
        assert comparison is not None
        assert hasattr(comparison, 'heatmap')
        assert hasattr(comparison, 'comparison_colors')
        assert 'positive' in comparison.comparison_colors
        assert 'negative' in comparison.comparison_colors
        assert 'neutral' in comparison.comparison_colors
        assert 'difference' in comparison.comparison_colors
    
    def test_render_with_valid_data(self):
        """Test rendering with valid attention data."""
        comparison = AttentionComparison()
        
        # Mock current result
        current_result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4},
                {"token": "amazing", "attention_score": 0.7, "contribution_score": 0.5}
            ],
            "word_contributions": [
                {"token": "great", "score": 0.6},
                {"token": "amazing", "score": 0.5},
                {"token": "movie", "score": 0.4}
            ]
        }
        
        # This should not raise any exceptions
        try:
            comparison.render(current_result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception: {e}")
    
    def test_render_with_comparison_data(self):
        """Test rendering with both current and comparison data."""
        comparison = AttentionComparison()
        
        # Mock current result
        current_result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4},
                {"token": "amazing", "attention_score": 0.7, "contribution_score": 0.5}
            ],
            "word_contributions": [
                {"token": "great", "score": 0.6},
                {"token": "amazing", "score": 0.5},
                {"token": "movie", "score": 0.4}
            ]
        }
        
        # Mock comparison result
        comparison_result = {
            "sentiment_label": "negative",
            "confidence_score": 0.75,
            "attention_weights": [
                {"token": "terrible", "attention_score": 0.9, "contribution_score": -0.7},
                {"token": "movie", "attention_score": 0.5, "contribution_score": -0.3},
                {"token": "awful", "attention_score": 0.8, "contribution_score": -0.6}
            ],
            "word_contributions": [
                {"token": "terrible", "score": -0.7},
                {"token": "awful", "score": -0.6},
                {"token": "movie", "score": -0.3}
            ]
        }
        
        # This should not raise any exceptions
        try:
            comparison.render(current_result, comparison_result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with comparison data: {e}")
    
    def test_render_without_attention_data(self):
        """Test rendering without attention data."""
        comparison = AttentionComparison()
        
        # Result without attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85
        }
        
        # This should not raise any exceptions
        try:
            comparison.render(result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception without attention data: {e}")
    
    def test_render_with_empty_result(self):
        """Test rendering with empty result."""
        comparison = AttentionComparison()
        
        # Empty result
        empty_result = {}
        
        # This should not raise any exceptions
        try:
            comparison.render(empty_result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with empty result: {e}")
    
    def test_render_with_none_result(self):
        """Test rendering with None result."""
        comparison = AttentionComparison()
        
        # None result
        none_result = None
        
        # This should not raise any exceptions
        try:
            comparison.render(none_result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with None result: {e}")
    
    def test_comparison_chart_creation(self):
        """Test that comparison chart creation works correctly."""
        comparison = AttentionComparison()
        
        # Mock attention weights with common tokens
        current_weights = [
            {"token": "great", "attention_score": 0.8},
            {"token": "movie", "attention_score": 0.6},
            {"token": "amazing", "attention_score": 0.7}
        ]
        
        comparison_weights = [
            {"token": "great", "attention_score": 0.7},
            {"token": "movie", "attention_score": 0.5},
            {"token": "terrible", "attention_score": 0.9}
        ]
        
        # This should not raise any exceptions
        try:
            comparison._create_comparison_chart(current_weights, comparison_weights)
            assert True
        except Exception as e:
            pytest.fail(f"Comparison chart creation raised an exception: {e}")
    
    def test_attention_difference_calculation(self):
        """Test attention difference calculation."""
        comparison = AttentionComparison()
        
        # Mock attention weights
        current_weights = [
            {"token": "great", "attention_score": 0.8},
            {"token": "movie", "attention_score": 0.6}
        ]
        
        comparison_weights = [
            {"token": "great", "attention_score": 0.7},
            {"token": "terrible", "attention_score": 0.9}
        ]
        
        # This should not raise any exceptions
        try:
            comparison._render_attention_difference(current_weights, comparison_weights)
            assert True
        except Exception as e:
            pytest.fail(f"Attention difference calculation raised an exception: {e}")
    
    def test_word_differences_rendering(self):
        """Test word differences rendering."""
        comparison = AttentionComparison()
        
        # Mock results with word contributions
        current_result = {
            "word_contributions": [
                {"token": "great", "score": 0.6},
                {"token": "amazing", "score": 0.5}
            ]
        }
        
        comparison_result = {
            "word_contributions": [
                {"token": "terrible", "score": -0.7},
                {"token": "awful", "score": -0.6}
            ]
        }
        
        # This should not raise any exceptions
        try:
            comparison._render_word_differences(current_result, comparison_result)
            assert True
        except Exception as e:
            pytest.fail(f"Word differences rendering raised an exception: {e}")
    
    def test_comparison_summary_rendering(self):
        """Test comparison summary rendering."""
        comparison = AttentionComparison()
        
        # Mock results
        current_result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8},
                {"token": "movie", "attention_score": 0.6}
            ]
        }
        
        comparison_result = {
            "sentiment_label": "negative",
            "confidence_score": 0.75,
            "attention_weights": [
                {"token": "terrible", "attention_score": 0.9},
                {"token": "movie", "attention_score": 0.5}
            ]
        }
        
        # This should not raise any exceptions
        try:
            comparison._render_comparison_summary(current_result, comparison_result)
            assert True
        except Exception as e:
            pytest.fail(f"Comparison summary rendering raised an exception: {e}")
    
    def test_difference_chart_creation(self):
        """Test difference chart creation."""
        comparison = AttentionComparison()
        
        # Mock differences data
        differences = [
            {"token": "great", "current_score": 0.8, "comparison_score": 0.7, "difference": 0.1},
            {"token": "movie", "current_score": 0.6, "comparison_score": 0.5, "difference": 0.1},
            {"token": "terrible", "current_score": 0.0, "comparison_score": 0.9, "difference": -0.9}
        ]
        
        # This should not raise any exceptions
        try:
            comparison._create_difference_chart(differences)
            assert True
        except Exception as e:
            pytest.fail(f"Difference chart creation raised an exception: {e}")
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        comparison = AttentionComparison()
        
        # Test with minimal data
        minimal_current = {
            "sentiment_label": "neutral",
            "confidence_score": 0.5,
            "attention_weights": [],
            "word_contributions": []
        }
        
        minimal_comparison = {
            "sentiment_label": "neutral",
            "confidence_score": 0.5,
            "attention_weights": [],
            "word_contributions": []
        }
        
        # Should handle empty attention data gracefully
        try:
            comparison.render(minimal_current, minimal_comparison)
            assert True
        except Exception as e:
            pytest.fail(f"Edge case test failed: {e}")
    
    def test_no_common_tokens(self):
        """Test behavior when there are no common tokens between analyses."""
        comparison = AttentionComparison()
        
        # Mock attention weights with no common tokens
        current_weights = [
            {"token": "great", "attention_score": 0.8},
            {"token": "amazing", "attention_score": 0.7}
        ]
        
        comparison_weights = [
            {"token": "terrible", "attention_score": 0.9},
            {"token": "awful", "attention_score": 0.8}
        ]
        
        # This should not raise any exceptions
        try:
            comparison._create_comparison_chart(current_weights, comparison_weights)
            assert True
        except Exception as e:
            pytest.fail(f"No common tokens test failed: {e}")

class TestIntegration:
    """Integration tests for attention comparison component."""
    
    def test_full_comparison_workflow(self):
        """Test the complete comparison workflow."""
        comparison = AttentionComparison()
        
        # Mock complete data
        current_result = {
            "sentiment_label": "positive",
            "confidence_score": 0.9,
            "attention_weights": [
                {"token": "fantastic", "attention_score": 0.95, "contribution_score": 0.9},
                {"token": "performance", "attention_score": 0.7, "contribution_score": 0.5},
                {"token": "brilliant", "attention_score": 0.8, "contribution_score": 0.7}
            ],
            "word_contributions": [
                {"token": "fantastic", "score": 0.9},
                {"token": "brilliant", "score": 0.7},
                {"token": "performance", "score": 0.5}
            ]
        }
        
        comparison_result = {
            "sentiment_label": "negative",
            "confidence_score": 0.8,
            "attention_weights": [
                {"token": "terrible", "attention_score": 0.9, "contribution_score": -0.8},
                {"token": "performance", "attention_score": 0.6, "contribution_score": -0.4},
                {"token": "awful", "attention_score": 0.85, "contribution_score": -0.7}
            ],
            "word_contributions": [
                {"token": "terrible", "score": -0.8},
                {"token": "awful", "score": -0.7},
                {"token": "performance", "score": -0.4}
            ]
        }
        
        # Test all comparison methods
        try:
            comparison.render(current_result, comparison_result)
            comparison._create_comparison_chart(
                current_result["attention_weights"], 
                comparison_result["attention_weights"]
            )
            comparison._render_attention_difference(
                current_result["attention_weights"], 
                comparison_result["attention_weights"]
            )
            comparison._render_word_differences(current_result, comparison_result)
            comparison._render_comparison_summary(current_result, comparison_result)
            assert True
        except Exception as e:
            pytest.fail(f"Full comparison workflow test failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
