"""
Tests for Visualization Export Component

This module contains unit tests for the visualization export component
including VisualizationExport class and its functionality.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.ui_components.visualization_export import VisualizationExport

class TestVisualizationExport:
    """Test cases for VisualizationExport component."""
    
    def test_initialization(self):
        """Test that the component initializes correctly."""
        export = VisualizationExport()
        assert export is not None
    
    def test_render_with_valid_data(self):
        """Test rendering with valid result data."""
        export = VisualizationExport()
        
        # Mock result with attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4},
                {"token": "amazing", "attention_score": 0.7, "contribution_score": 0.5}
            ],
            "top_contributing_words": [
                {"token": "great", "score": 0.6},
                {"token": "amazing", "score": 0.5},
                {"token": "movie", "score": 0.4}
            ]
        }
        
        # This should not raise any exceptions
        try:
            export.render(result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception: {e}")
    
    def test_render_without_data(self):
        """Test rendering without result data."""
        export = VisualizationExport()
        
        # This should not raise any exceptions
        try:
            export.render()
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception without data: {e}")
    
    def test_render_without_attention_data(self):
        """Test rendering without attention data."""
        export = VisualizationExport()
        
        # Result without attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85
        }
        
        # This should not raise any exceptions
        try:
            export.render(result)
            assert True
        except Exception as e:
            pytest.fail(f"Render method raised an exception without attention data: {e}")
    
    def test_export_attention_csv(self):
        """Test CSV export functionality."""
        export = VisualizationExport()
        
        # Mock result with attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4}
            ]
        }
        
        # This should not raise any exceptions
        try:
            export._export_attention_csv(result)
            assert True
        except Exception as e:
            pytest.fail(f"CSV export raised an exception: {e}")
    
    def test_export_attention_excel(self):
        """Test Excel export functionality."""
        export = VisualizationExport()
        
        # Mock result with attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4}
            ],
            "top_contributing_words": [
                {"token": "great", "score": 0.6},
                {"token": "movie", "score": 0.4}
            ]
        }
        
        # This should not raise any exceptions
        try:
            export._export_attention_excel(result)
            assert True
        except Exception as e:
            pytest.fail(f"Excel export raised an exception: {e}")
    
    def test_export_heatmap_png(self):
        """Test PNG export functionality."""
        export = VisualizationExport()
        
        # Mock result with attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4}
            ]
        }
        
        # This should not raise any exceptions
        try:
            export._export_heatmap_png(result)
            assert True
        except Exception as e:
            pytest.fail(f"PNG export raised an exception: {e}")
    
    def test_export_heatmap_pdf(self):
        """Test PDF export functionality."""
        export = VisualizationExport()
        
        # Mock result with attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4}
            ]
        }
        
        # This should not raise any exceptions
        try:
            export._export_heatmap_pdf(result)
            assert True
        except Exception as e:
            pytest.fail(f"PDF export raised an exception: {e}")
    
    def test_advanced_export_options(self):
        """Test advanced export options rendering."""
        export = VisualizationExport()
        
        # Mock result with attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4}
            ]
        }
        
        # This should not raise any exceptions
        try:
            export._render_advanced_export_options(result)
            assert True
        except Exception as e:
            pytest.fail(f"Advanced export options raised an exception: {e}")
    
    def test_custom_export_settings(self):
        """Test custom export settings functionality."""
        export = VisualizationExport()
        
        # Mock result with attention data
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6},
                {"token": "movie", "attention_score": 0.6, "contribution_score": 0.4}
            ]
        }
        
        # Test different formats
        formats = ["PNG", "PDF", "SVG", "HTML"]
        
        for format_type in formats:
            try:
                export._export_with_custom_settings(
                    result, format_type, True, "test_export"
                )
                assert True
            except Exception as e:
                pytest.fail(f"Custom export with {format_type} raised an exception: {e}")
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        export = VisualizationExport()
        
        # Test with minimal data
        minimal_result = {
            "sentiment_label": "neutral",
            "confidence_score": 0.5,
            "attention_weights": []
        }
        
        # Should handle empty attention data gracefully
        try:
            export.render(minimal_result)
            assert True
        except Exception as e:
            pytest.fail(f"Edge case test failed: {e}")
        
        # Test with None result
        try:
            export.render(None)
            assert True
        except Exception as e:
            pytest.fail(f"None result test failed: {e}")
    
    def test_empty_attention_weights(self):
        """Test handling of empty attention weights."""
        export = VisualizationExport()
        
        # Result with empty attention weights
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": []
        }
        
        # Test all export methods with empty data
        try:
            export._export_attention_csv(result)
            export._export_attention_excel(result)
            export._export_heatmap_png(result)
            export._export_heatmap_pdf(result)
            assert True
        except Exception as e:
            pytest.fail(f"Empty attention weights test failed: {e}")
    
    def test_missing_top_contributing_words(self):
        """Test handling of missing top contributing words."""
        export = VisualizationExport()
        
        # Result without top contributing words
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6}
            ]
        }
        
        # This should not raise any exceptions
        try:
            export._export_attention_excel(result)
            assert True
        except Exception as e:
            pytest.fail(f"Missing top contributing words test failed: {e}")

class TestIntegration:
    """Integration tests for visualization export component."""
    
    def test_full_export_workflow(self):
        """Test the complete export workflow."""
        export = VisualizationExport()
        
        # Mock complete data
        result = {
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
        
        # Test all export methods
        try:
            export.render(result)
            export._export_attention_csv(result)
            export._export_attention_excel(result)
            export._export_heatmap_png(result)
            export._export_heatmap_pdf(result)
            export._render_advanced_export_options(result)
            export._export_with_custom_settings(result, "PNG", True, "test")
            assert True
        except Exception as e:
            pytest.fail(f"Full export workflow test failed: {e}")
    
    def test_export_format_handling(self):
        """Test handling of different export formats."""
        export = VisualizationExport()
        
        # Mock result
        result = {
            "sentiment_label": "negative",
            "confidence_score": 0.8,
            "attention_weights": [
                {"token": "terrible", "attention_score": 0.9, "contribution_score": -0.8},
                {"token": "awful", "attention_score": 0.8, "contribution_score": -0.7}
            ]
        }
        
        # Test all supported formats
        formats = ["PNG", "PDF", "SVG", "HTML"]
        
        for format_type in formats:
            try:
                export._export_with_custom_settings(
                    result, format_type, True, f"test_{format_type.lower()}"
                )
                assert True
            except Exception as e:
                pytest.fail(f"Export format {format_type} test failed: {e}")
    
    def test_metadata_inclusion(self):
        """Test metadata inclusion in exports."""
        export = VisualizationExport()
        
        # Mock result
        result = {
            "sentiment_label": "positive",
            "confidence_score": 0.85,
            "attention_weights": [
                {"token": "great", "attention_score": 0.8, "contribution_score": 0.6}
            ]
        }
        
        # Test with and without metadata
        try:
            export._export_with_custom_settings(result, "PNG", True, "test_with_metadata")
            export._export_with_custom_settings(result, "PNG", False, "test_without_metadata")
            assert True
        except Exception as e:
            pytest.fail(f"Metadata inclusion test failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
