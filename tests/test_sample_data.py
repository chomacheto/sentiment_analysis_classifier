"""
Unit tests for sample data components.

This module tests the functionality of sample data components including
ExampleGallery, ResultsComparison, UseCaseDocumentation, PerformanceBenchmark,
and InteractiveTutorial.
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.ui_components.example_gallery import ExampleGallery
from packages.ui_components.results_comparison import ResultsComparison
from packages.ui_components.use_case_documentation import UseCaseDocumentation
from packages.ui_components.performance_benchmark import PerformanceBenchmark
from packages.ui_components.interactive_tutorial import InteractiveTutorial


class TestExampleGallery:
    """Test cases for ExampleGallery component."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_data = {
            "samples": [
                {
                    "id": "test_sample_1",
                    "text": "This is a positive test sample.",
                    "category": "test",
                    "expected_sentiment": "positive",
                    "difficulty_level": "easy",
                    "source": "Test source",
                    "use_case": "Test use case",
                    "notes": "Test notes"
                },
                {
                    "id": "test_sample_2",
                    "text": "This is a negative test sample.",
                    "category": "test",
                    "expected_sentiment": "negative",
                    "difficulty_level": "medium",
                    "source": "Test source",
                    "use_case": "Test use case",
                    "notes": "Test notes"
                }
            ]
        }
        
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(self.sample_data, self.temp_file)
        self.temp_file.close()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_init_with_valid_file(self):
        """Test initialization with valid sample data file."""
        gallery = ExampleGallery(self.temp_file.name)
        assert len(gallery.samples) == 2
        assert gallery.categories == ['test']
    
    def test_init_with_invalid_file(self):
        """Test initialization with invalid file path."""
        gallery = ExampleGallery("nonexistent_file.json")
        assert len(gallery.samples) == 0
        assert gallery.categories == []
    
    def test_get_sample_by_id(self):
        """Test getting sample by ID."""
        gallery = ExampleGallery(self.temp_file.name)
        sample = gallery.get_sample_by_id("test_sample_1")
        assert sample is not None
        assert sample['text'] == "This is a positive test sample."
        assert sample['expected_sentiment'] == "positive"
    
    def test_get_sample_by_nonexistent_id(self):
        """Test getting sample by nonexistent ID."""
        gallery = ExampleGallery(self.temp_file.name)
        sample = gallery.get_sample_by_id("nonexistent_id")
        assert sample is None
    
    def test_get_samples_by_category(self):
        """Test getting samples by category."""
        gallery = ExampleGallery(self.temp_file.name)
        samples = gallery.get_samples_by_category("test")
        assert len(samples) == 2
        assert all(sample['category'] == 'test' for sample in samples)
    
    def test_get_samples_by_nonexistent_category(self):
        """Test getting samples by nonexistent category."""
        gallery = ExampleGallery(self.temp_file.name)
        samples = gallery.get_samples_by_category("nonexistent")
        assert len(samples) == 0
    
    def test_filter_samples(self):
        """Test filtering samples by category and difficulty."""
        gallery = ExampleGallery(self.temp_file.name)
        
        # Filter by category
        filtered = gallery._filter_samples("test", "All Difficulties")
        assert len(filtered) == 2
        
        # Filter by difficulty
        filtered = gallery._filter_samples("All Categories", "easy")
        assert len(filtered) == 1
        assert filtered[0]['difficulty_level'] == "easy"
        
        # Filter by both
        filtered = gallery._filter_samples("test", "medium")
        assert len(filtered) == 1
        assert filtered[0]['difficulty_level'] == "medium"


class TestResultsComparison:
    """Test cases for ResultsComparison component."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_data = {
            "samples": [
                {
                    "id": "test_sample_1",
                    "text": "This is a positive test sample.",
                    "category": "test",
                    "expected_sentiment": "positive",
                    "difficulty_level": "easy",
                    "source": "Test source",
                    "use_case": "Test use case",
                    "notes": "Test notes"
                }
            ]
        }
        
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(self.sample_data, self.temp_file)
        self.temp_file.close()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_init_with_valid_file(self):
        """Test initialization with valid sample data file."""
        comparison = ResultsComparison(self.temp_file.name)
        assert len(comparison.samples) == 1
    
    def test_get_sample_by_id(self):
        """Test getting sample by ID."""
        comparison = ResultsComparison(self.temp_file.name)
        sample = comparison._get_sample_by_id("test_sample_1")
        assert sample is not None
        assert sample['expected_sentiment'] == "positive"
    
    def test_get_sentiment_color(self):
        """Test getting sentiment color."""
        comparison = ResultsComparison(self.temp_file.name)
        
        assert comparison._get_sentiment_color("positive") == "#4CAF50"
        assert comparison._get_sentiment_color("negative") == "#F44336"
        assert comparison._get_sentiment_color("neutral") == "#2196F3"
        assert comparison._get_sentiment_color("unknown") == "#9E9E9E"
    
    def test_get_category_insights(self):
        """Test getting category insights."""
        comparison = ResultsComparison(self.temp_file.name)
        
        insights = comparison._get_category_insights("movie_review")
        assert len(insights) > 0
        assert all(isinstance(insight, str) for insight in insights)
        
        # Test unknown category
        insights = comparison._get_category_insights("unknown_category")
        assert len(insights) == 1
        assert "unique characteristics" in insights[0]


class TestUseCaseDocumentation:
    """Test cases for UseCaseDocumentation component."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.use_cases_data = {
            "use_cases": [
                {
                    "category": "test",
                    "name": "Test Use Case",
                    "description": "Test description",
                    "characteristics": ["Test characteristic"],
                    "real_world_scenarios": ["Test scenario"],
                    "best_practices": ["Test practice"],
                    "industry_examples": ["Test example"]
                }
            ]
        }
        
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(self.use_cases_data, self.temp_file)
        self.temp_file.close()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_init_with_valid_file(self):
        """Test initialization with valid use cases file."""
        docs = UseCaseDocumentation(self.temp_file.name)
        assert len(docs.use_cases) == 1
    
    def test_get_use_case_by_category(self):
        """Test getting use case by category."""
        docs = UseCaseDocumentation(self.temp_file.name)
        use_case = docs._get_use_case_by_category("test")
        assert use_case is not None
        assert use_case['name'] == "Test Use Case"
    
    def test_get_use_case_by_nonexistent_category(self):
        """Test getting use case by nonexistent category."""
        docs = UseCaseDocumentation(self.temp_file.name)
        use_case = docs._get_use_case_by_category("nonexistent")
        assert use_case is None
    
    def test_get_category_indicators(self):
        """Test getting category indicators."""
        docs = UseCaseDocumentation(self.temp_file.name)
        
        indicators = docs._get_category_indicators("movie_review")
        assert len(indicators) > 0
        assert all(isinstance(indicator, str) for indicator in indicators)
    
    def test_get_category_applications(self):
        """Test getting category applications."""
        docs = UseCaseDocumentation(self.temp_file.name)
        
        applications = docs._get_category_applications("social_media")
        assert len(applications) > 0
        assert all(isinstance(app, str) for app in applications)
    
    def test_get_category_tips(self):
        """Test getting category tips."""
        docs = UseCaseDocumentation(self.temp_file.name)
        
        tips = docs._get_category_tips("formal")
        assert len(tips) > 0
        assert all(isinstance(tip, str) for tip in tips)
    
    def test_get_category_difficulty(self):
        """Test getting category difficulty."""
        docs = UseCaseDocumentation(self.temp_file.name)
        
        assert docs._get_category_difficulty("movie_review") == "Easy"
        assert docs._get_category_difficulty("sarcasm") == "Hard"
        assert docs._get_category_difficulty("unknown") == "Medium"


class TestPerformanceBenchmark:
    """Test cases for PerformanceBenchmark component."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.benchmark_data = {
            "benchmarks": {
                "model_performance": {
                    "overall_metrics": {
                        "accuracy": 0.89,
                        "precision": 0.87,
                        "recall": 0.91,
                        "f1_score": 0.89,
                        "processing_time_avg_ms": 1450
                    },
                    "by_category": {
                        "test": {
                            "accuracy": 0.90,
                            "precision": 0.88,
                            "recall": 0.92,
                            "f1_score": 0.90,
                            "sample_count": 1000,
                            "notes": "Test category performance"
                        }
                    }
                },
                "standard_datasets": {
                    "test_dataset": {
                        "dataset_size": 5000,
                        "accuracy": 0.88,
                        "precision": 0.86,
                        "recall": 0.90,
                        "f1_score": 0.88,
                        "industry_standard": 0.85,
                        "notes": "Test dataset performance"
                    }
                }
            }
        }
        
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(self.benchmark_data, self.temp_file)
        self.temp_file.close()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_init_with_valid_file(self):
        """Test initialization with valid benchmark file."""
        benchmark = PerformanceBenchmark(self.temp_file.name)
        assert benchmark.benchmark_data is not None
        assert "model_performance" in benchmark.benchmark_data["benchmarks"]
    
    def test_init_with_invalid_file(self):
        """Test initialization with invalid file path."""
        benchmark = PerformanceBenchmark("nonexistent_file.json")
        assert benchmark.benchmark_data is None


class TestInteractiveTutorial:
    """Test cases for InteractiveTutorial component."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tutorial = InteractiveTutorial()
    
    def test_init(self):
        """Test initialization."""
        assert self.tutorial.tutorials is not None
        assert "beginner" in self.tutorial.tutorials
        assert "intermediate" in self.tutorial.tutorials
        assert "advanced" in self.tutorial.tutorials
    
    def test_load_tutorials(self):
        """Test loading tutorial definitions."""
        tutorials = self.tutorial._load_tutorials()
        assert isinstance(tutorials, dict)
        assert len(tutorials) == 3
        
        # Check beginner tutorial
        beginner = tutorials["beginner"]
        assert beginner["title"] == "Beginner Tutorial"
        assert len(beginner["steps"]) > 0
        
        # Check intermediate tutorial
        intermediate = tutorials["intermediate"]
        assert intermediate["title"] == "Intermediate Tutorial"
        assert len(intermediate["steps"]) > 0
        
        # Check advanced tutorial
        advanced = tutorials["advanced"]
        assert advanced["title"] == "Advanced Tutorial"
        assert len(advanced["steps"]) > 0
    
    def test_tutorial_structure(self):
        """Test tutorial structure and content."""
        for tutorial_id, tutorial in self.tutorial.tutorials.items():
            # Check required fields
            assert "title" in tutorial
            assert "description" in tutorial
            assert "steps" in tutorial
            
            # Check steps structure
            for step in tutorial["steps"]:
                assert "title" in step
                assert "content" in step
                assert "action" in step
                assert step["action"] in ["info", "highlight", "success"]


class TestSampleDataIntegration:
    """Integration tests for sample data components."""
    
    def test_sample_data_structure(self):
        """Test that sample data files have correct structure."""
        sample_data_path = Path("data/samples/sample_data.json")
        use_cases_path = Path("data/samples/use_cases.json")
        benchmarks_path = Path("data/samples/benchmarks.json")
        
        # Test sample data file
        if sample_data_path.exists():
            with open(sample_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                assert "samples" in data
                assert len(data["samples"]) > 0
                
                for sample in data["samples"]:
                    required_fields = ["id", "text", "category", "expected_sentiment", 
                                     "difficulty_level", "source", "use_case"]
                    for field in required_fields:
                        assert field in sample
        
        # Test use cases file
        if use_cases_path.exists():
            with open(use_cases_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                assert "use_cases" in data
                assert len(data["use_cases"]) > 0
                
                for use_case in data["use_cases"]:
                    required_fields = ["category", "name", "description", "characteristics",
                                     "real_world_scenarios", "best_practices", "industry_examples"]
                    for field in required_fields:
                        assert field in use_case
        
        # Test benchmarks file
        if benchmarks_path.exists():
            with open(benchmarks_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                assert "benchmarks" in data
                assert "model_performance" in data["benchmarks"]


if __name__ == "__main__":
    pytest.main([__file__])
