"""
Example Gallery Component for Sample Data Display and Selection

This component provides a gallery of curated sample texts for sentiment analysis,
allowing users to quickly load examples into the analysis interface.
"""

import json
import streamlit as st
from typing import Dict, List, Optional, Any
from pathlib import Path


class ExampleGallery:
    """Gallery component for displaying and selecting sample data."""
    
    def __init__(self, sample_data_path: str = "data/samples/sample_data.json"):
        """Initialize the ExampleGallery with sample data.
        
        Args:
            sample_data_path: Path to the sample data JSON file
        """
        self.sample_data_path = Path(sample_data_path)
        self.samples = self._load_sample_data()
        self.categories = self._get_categories()
        
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
    
    def _get_categories(self) -> List[str]:
        """Get unique categories from sample data.
        
        Returns:
            List of unique category names
        """
        categories = list(set(sample['category'] for sample in self.samples))
        return sorted(categories)
    
    def render(self, on_sample_select: callable) -> None:
        """Render the example gallery interface.
        
        Args:
            on_sample_select: Callback function when a sample is selected
        """
        st.subheader("📚 Sample Data Gallery")
        st.markdown("Explore curated examples of different text types for sentiment analysis.")
        
        # Category filter
        selected_category = st.selectbox(
            "Filter by category:",
            ["All Categories"] + self.categories,
            key="gallery_category_filter"
        )
        
        # Difficulty filter
        difficulty_options = ["All Difficulties", "easy", "medium", "hard"]
        selected_difficulty = st.selectbox(
            "Filter by difficulty:",
            difficulty_options,
            key="gallery_difficulty_filter"
        )
        
        # Filter samples
        filtered_samples = self._filter_samples(selected_category, selected_difficulty)
        
        if not filtered_samples:
            st.info("No samples match the selected filters.")
            return
        
        # Display samples in a grid
        self._render_sample_grid(filtered_samples, on_sample_select)
    
    def _filter_samples(self, category: str, difficulty: str) -> List[Dict[str, Any]]:
        """Filter samples by category and difficulty.
        
        Args:
            category: Selected category filter
            difficulty: Selected difficulty filter
            
        Returns:
            Filtered list of samples
        """
        filtered = self.samples
        
        if category != "All Categories":
            filtered = [s for s in filtered if s['category'] == category]
        
        if difficulty != "All Difficulties":
            filtered = [s for s in filtered if s['difficulty_level'] == difficulty]
        
        return filtered
    
    def _render_sample_grid(self, samples: List[Dict[str, Any]], on_sample_select: callable) -> None:
        """Render samples in a responsive grid layout.
        
        Args:
            samples: List of samples to display
            on_sample_select: Callback function when a sample is selected
        """
        # Create columns for responsive grid
        cols = st.columns(2)
        
        for i, sample in enumerate(samples):
            col_idx = i % 2
            with cols[col_idx]:
                self._render_sample_card(sample, on_sample_select)
    
    def _render_sample_card(self, sample: Dict[str, Any], on_sample_select: callable) -> None:
        """Render a single sample card.
        
        Args:
            sample: Sample data dictionary
            on_sample_select: Callback function when sample is selected
        """
        with st.container():
            # Card styling
            st.markdown("""
                <style>
                .sample-card {
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 16px;
                    margin: 8px 0;
                    background-color: #fafafa;
                }
                .sample-card:hover {
                    border-color: #2196F3;
                    background-color: #f5f5f5;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Card content
            with st.container():
                st.markdown(f"""
                    <div class="sample-card">
                        <h4>{sample['id'].replace('_', ' ').title()}</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                # Sample text preview (truncated)
                preview_text = sample['text'][:100] + "..." if len(sample['text']) > 100 else sample['text']
                st.text_area(
                    "Sample Text:",
                    value=preview_text,
                    height=80,
                    key=f"preview_{sample['id']}",
                    disabled=True
                )
                
                # Sample metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Category:** {sample['category']}")
                with col2:
                    st.markdown(f"**Expected:** {sample['expected_sentiment']}")
                with col3:
                    st.markdown(f"**Difficulty:** {sample['difficulty_level']}")
                
                # Load button
                if st.button(f"Load Sample", key=f"load_{sample['id']}"):
                    on_sample_select(sample['text'])
                    st.success(f"Loaded sample: {sample['id']}")
                
                # Show full text on expander
                with st.expander("View Full Text"):
                    st.text_area(
                        "Full Sample Text:",
                        value=sample['text'],
                        height=120,
                        key=f"full_{sample['id']}",
                        disabled=True
                    )
                    
                    # Additional metadata
                    st.markdown(f"**Source:** {sample['source']}")
                    st.markdown(f"**Use Case:** {sample['use_case']}")
                    if sample.get('notes'):
                        st.markdown(f"**Notes:** {sample['notes']}")
    
    def get_sample_by_id(self, sample_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific sample by ID.
        
        Args:
            sample_id: ID of the sample to retrieve
            
        Returns:
            Sample data dictionary or None if not found
        """
        for sample in self.samples:
            if sample['id'] == sample_id:
                return sample
        return None
    
    def get_samples_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all samples for a specific category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of samples in the specified category
        """
        return [s for s in self.samples if s['category'] == category]
    
    def get_random_sample(self, category: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a random sample, optionally filtered by category.
        
        Args:
            category: Optional category filter
            
        Returns:
            Random sample or None if no samples available
        """
        import random
        
        samples = self.samples
        if category:
            samples = self.get_samples_by_category(category)
        
        if samples:
            return random.choice(samples)
        return None


def render_example_gallery(on_sample_select: callable) -> None:
    """Convenience function to render the example gallery.
    
    Args:
        on_sample_select: Callback function when a sample is selected
    """
    gallery = ExampleGallery()
    gallery.render(on_sample_select)


if __name__ == "__main__":
    # Test the component
    def test_callback(text: str):
        st.write(f"Selected text: {text[:50]}...")
    
    render_example_gallery(test_callback)
