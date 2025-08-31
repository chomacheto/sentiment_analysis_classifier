"""
Tests for Technical Explanation Component

This module contains unit tests for the technical explanation component
including TechnicalExplanation class and its functionality.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.ui_components.technical_explanation import TechnicalExplanation

class TestTechnicalExplanation:
    """Test cases for TechnicalExplanation component."""
    
    def test_initialization(self):
        """Test that the component initializes correctly."""
        explanation = TechnicalExplanation()
        assert explanation is not None
        assert hasattr(explanation, 'sections')
        assert 'attention_basics' in explanation.sections
        assert 'transformer_attention' in explanation.sections
        assert 'interpretation_guide' in explanation.sections
        assert 'best_practices' in explanation.sections
        assert 'visual_examples' in explanation.sections
    
    def test_render_with_valid_data(self):
        """Test rendering with valid result data."""
        explanation = TechnicalExplanation()
        
        # Mock result with attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4},
                {"token": "amazing", "attention_score": 0.7, "contribution_score": 0.5}
            ]
        }
        
        # This should not raise any exceptions
        try:
            explanation.render(result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception: {e}")
    
    def test_render_without_data(self):
        """Test rendering without result data."""
        explanation = TechnicalExplanation()
        
        # This should not raise any exceptions
        try:
            explanation.render()
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception without data: {e}")
    
    def test_render_with_empty_result(self):
        """Test rendering with empty result."""
        explanation = TechnicalExplanation()
        
        # Empty result
        empty_result = {}
        
        # This should not raise any exceptions
        try:
            explanation.render(empty_result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with empty result: {e}")
    
    def test_render_with_none_result(self):
        """Test rendering with None result."""
        explanation = TechnicalExplanation()
        
        # None result
        none_result = None
        
        # This should not raise any exceptions
        try:
            explanation.render(none_result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception with None result: {e}")
    
    def test_attention_basics_rendering(self):
        """Test attention basics section rendering."""
        explanation = TechnicalExplanation()
        
        # This should not raise any exceptions
        try:
            explanation._render_attention_basics()
            assert True
        except Exception as e:
            pytest.fail(f"Attention basics rendering raised an exception: {e}")
    
    def test_transformer_attention_rendering(self):
        """Test transformer attention section rendering."""
        explanation = TechnicalExplanation()
        
        # This should not raise any exceptions
        try:
            explanation._render_transformer_attention()
            assert True
        except Exception as e:
            pytest.fail(f"Transformer attention rendering raised an exception: {e}")
    
    def test_interpretation_guide_rendering(self):
        """Test interpretation guide section rendering."""
        explanation = TechnicalExplanation()
        
        # Test without result data
        try:
            explanation._render_interpretation_guide()
            assert True
        except Exception as e:
            pytest.fail(f"Interpretation guide rendering raised an exception: {e}")
        
        # Test with result data
        result = {
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4}
            ]
        }
        
        try:
            explanation._render_interpretation_guide(result)
            assert True
        except Exception as e:
            pytest.fail(f"Interpretation guide rendering with data raised an exception: {e}")
    
    def test_best_practices_rendering(self):
        """Test best practices section rendering."""
        explanation = TechnicalExplanation()
        
        # This should not raise any exceptions
        try:
            explanation._render_best_practices()
            assert True
        except Exception as e:
            pytest.fail(f"Best practices rendering raised an exception: {e}")
    
    def test_visual_examples_rendering(self):
        """Test visual examples section rendering."""
        explanation = TechnicalExplanation()
        
        # Test without result data
        try:
            explanation._render_visual_examples()
            assert True
        except Exception as e:
            pytest.fail(f"Visual examples rendering raised an exception: {e}")
        
        # Test with result data
        result = {
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4}
            ]
        }
        
        try:
            explanation._render_visual_examples(result)
            assert True
        except Exception as e:
            pytest.fail(f"Visual examples rendering with data raised an exception: {e}")
    
    def test_attention_example_rendering(self):
        """Test attention example rendering."""
        explanation = TechnicalExplanation()
        
        # Test with different sentences
        test_sentences = [
            "The movie was great!",
            "This film is terrible.",
            "The acting was amazing but the plot was awful."
        ]
        
        for sentence in test_sentences:
            try:
                explanation._show_attention_example(sentence)
                assert True
            except Exception as e:
                pytest.fail(f"Attention example rendering raised an exception for '{sentence}': {e}")
    
    def test_section_rendering(self):
        """Test section rendering method."""
        explanation = TechnicalExplanation()
        
        # Test all sections
        sections = ["attention_basics", "transformer_attention", "interpretation_guide", "best_practices", "visual_examples"]
        
        for section in sections:
            try:
                explanation._render_section(section)
                assert True
            except Exception as e:
                pytest.fail(f"Section rendering raised an exception for '{section}': {e}")
        
        # Test with result data
        result = {
            "attention_weights": [
                {"token": "test", "attention_score": 0.5, "contribution_score": 0.3}
            ]
        }
        
        for section in sections:
            try:
                explanation._render_section(section, result)
                assert True
            except Exception as e:
                pytest.fail(f"Section rendering with data raised an exception for '{section}': {e}")
    
    def test_content_methods(self):
        """Test content retrieval methods."""
        explanation = TechnicalExplanation()
        
        # Test all content methods
        content_methods = [
            explanation._get_attention_basics_content,
            explanation._get_transformer_attention_content,
            explanation._get_interpretation_guide_content,
            explanation._get_best_practices_content,
            explanation._get_visual_examples_content
        ]
        
        for method in content_methods:
            try:
                content = method()
                assert isinstance(content, str)
                assert len(content) > 0
            except Exception as e:
                pytest.fail(f"Content method raised an exception: {e}")
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        explanation = TechnicalExplanation()
        
        # Test with minimal data
        minimal_result = {
            "sentiment_label": "neutral",
            "confidence_score": 0.5,
            "attention_weights": []
        }
        
        # Should handle empty attention data gracefully
        try:
            explanation.render(minimal_result)
            assert True
        except Exception as e:
            pytest.fail(f"Edge case test failed: {e}")
        
        # Test with invalid section name
        try:
            explanation._render_section("invalid_section")
            assert True
        except Exception as e:
            pytest.fail(f"Invalid section test failed: {e}")
    
    def test_empty_sentence_handling(self):
        """Test handling of empty sentences in attention examples."""
        explanation = TechnicalExplanation()
        
        # Test with empty string
        try:
            explanation._show_attention_example("")
            assert True
        except Exception as e:
            pytest.fail(f"Empty sentence test failed: {e}")
        
        # Test with single word
        try:
            explanation._show_attention_example("test")
            assert True
        except Exception as e:
            pytest.fail(f"Single word test failed: {e}")
        
        # Test with very long sentence
        long_sentence = "This is a very long sentence with many words to test how the component handles longer inputs and whether it can process them correctly without any issues or errors occurring during the rendering process."
        try:
            explanation._show_attention_example(long_sentence)
            assert True
        except Exception as e:
            pytest.fail(f"Long sentence test failed: {e}")

class TestIntegration:
    """Integration tests for technical explanation component."""
    
    def test_full_explanation_workflow(self):
        """Test the complete explanation workflow."""
        explanation = TechnicalExplanation()
        
        # Mock complete data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.9,
            "attention_weights": [
                {"token": "fantastic", "attention_score": 0.95, "contribution_score": 0.9},
                {"token": "performance", "attention_score": 0.7, "contribution_score": 0.5},
                {"token": "brilliant", "attention_score": 0.8, "contribution_score": 0.7}
            ]
        }
        
        # Test all explanation methods
        try:
            explanation.render(result)
            explanation._render_attention_basics()
            explanation._render_transformer_attention()
            explanation._render_interpretation_guide(result)
            explanation._render_best_practices()
            explanation._render_visual_examples(result)
            explanation._show_attention_example("The movie was fantastic!")
            assert True
        except Exception as e:
            pytest.fail(f"Full explanation workflow test failed: {e}")
    
    def test_section_content_consistency(self):
        """Test that section content is consistent and accessible."""
        explanation = TechnicalExplanation()
        
        # Verify all sections have required attributes
        for section_name, section_data in explanation.sections.items():
            assert "title" in section_data
            assert "content" in section_data
            assert isinstance(section_data["title"], str)
            assert isinstance(section_data["content"], str)
            assert len(section_data["title"]) > 0
            assert len(section_data["content"]) > 0
    
    def test_interactive_features(self):
        """Test interactive features of the explanation component."""
        explanation = TechnicalExplanation()
        
        # Test attention example with various inputs
        test_inputs = [
            "Great movie!",
            "Terrible film.",
            "The acting was good but the plot was bad.",
            "Absolutely amazing performance!",
            "Not worth watching at all."
        ]
        
        for test_input in test_inputs:
            try:
                explanation._show_attention_example(test_input)
                assert True
            except Exception as e:
                pytest.fail(f"Interactive feature test failed for '{test_input}': {e}")

if __name__ == "__main__":
    pytest.main([__file__])
