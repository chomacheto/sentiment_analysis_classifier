"""
Streamlit Web Interface for Sentiment Analysis

This module provides a clean, professional web interface for sentiment analysis
with real-time prediction, professional styling, and responsive design.
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from packages.ml_core.sentiment_pipeline import SentimentClassificationPipeline
from packages.ml_core.validators import TextValidator
from packages.ui_components.sentiment_display import SentimentDisplay
from packages.ui_components.text_input import TextInputComponent
from packages.ui_components.sidebar import SidebarComponent
from packages.ui_components.confidence_metrics import ConfidenceMetrics
from packages.ui_components.prediction_history import PredictionHistory
from packages.ui_components.statistics_panel import StatisticsPanel
from packages.ui_components.csv_export import CSVExport
from packages.ui_components.attention_comparison import AttentionComparison
from packages.ui_components.technical_explanation import TechnicalExplanation
from packages.ui_components.visualization_export import VisualizationExport
from packages.ui_components.example_gallery import ExampleGallery
from packages.ui_components.results_comparison import ResultsComparison
from packages.ui_components.use_case_documentation import UseCaseDocumentation
from packages.ui_components.performance_benchmark import PerformanceBenchmark
from packages.ui_components.interactive_tutorial import InteractiveTutorial

# Page configuration
st.set_page_config(
    page_title="Sentiment Analysis Classifier",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
def load_custom_css():
    """Load custom CSS for professional styling."""
    st.markdown("""
    <style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Content area styling */
    .content-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Input area styling */
    .input-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #e9ecef;
        margin-bottom: 2rem;
    }
    
    .input-container:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Results area styling */
    .results-container {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-top: 2rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .content-container {
            padding: 1rem;
        }
        
        .input-container {
            padding: 1rem;
        }
    }
    
    /* Loading spinner styling */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Success/error message styling */
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state for user interaction persistence."""
    if 'sentiment_pipeline' not in st.session_state:
        st.session_state.sentiment_pipeline = None
    
    if 'text_validator' not in st.session_state:
        st.session_state.text_validator = None
    
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    
    if 'current_input' not in st.session_state:
        st.session_state.current_input = ""
    
    if 'last_analysis' not in st.session_state:
        st.session_state.last_analysis = None
    
    # New components session state
    if 'show_enhanced_confidence' not in st.session_state:
        st.session_state.show_enhanced_confidence = False
    
    if 'show_statistics' not in st.session_state:
        st.session_state.show_statistics = False
    
    if 'show_prediction_history' not in st.session_state:
        st.session_state.show_prediction_history = False
    
    if 'show_export' not in st.session_state:
        st.session_state.show_export = False
    
    # Sample data components session state
    if 'show_sample_gallery' not in st.session_state:
        st.session_state.show_sample_gallery = False
    
    if 'show_results_comparison' not in st.session_state:
        st.session_state.show_results_comparison = False
    
    if 'show_use_case_docs' not in st.session_state:
        st.session_state.show_use_case_docs = False
    
    if 'show_performance_benchmarks' not in st.session_state:
        st.session_state.show_performance_benchmarks = False
    
    if 'show_tutorial' not in st.session_state:
        st.session_state.show_tutorial = False
    
    if 'current_sample_id' not in st.session_state:
        st.session_state.current_sample_id = None

def initialize_components():
    """Initialize ML components."""
    try:
        if st.session_state.sentiment_pipeline is None:
            with st.spinner("Initializing sentiment analysis pipeline..."):
                st.session_state.sentiment_pipeline = SentimentClassificationPipeline()
                st.session_state.text_validator = TextValidator()
        return True
    except Exception as e:
        st.error(f"Failed to initialize components: {str(e)}")
        return False

def main():
    """Main application function."""
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize components
    if not initialize_components():
        st.error("Application failed to initialize. Please refresh the page.")
        return
    
    # Sidebar
    sidebar = SidebarComponent()
    sidebar.render()
    
    # Main content area
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Sentiment Analysis Classifier</h1>
        <p>Analyze the sentiment of your text with AI-powered classification</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content container
    with st.container():
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # Text input section
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        st.subheader("📝 Enter Your Text")
        st.markdown("Input text to analyze (maximum 1000 characters)")
        
        text_input = TextInputComponent()
        user_input = text_input.render()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis button
        analyze_button = st.button(
            "🔍 Analyze Sentiment",
            type="primary",
            use_container_width=True,
            disabled=not user_input.strip()
        )
        
        # Perform analysis when button is clicked
        if analyze_button and user_input.strip():
            perform_sentiment_analysis(user_input.strip())
        
        # Display results if available
        if st.session_state.last_analysis:
            display_analysis_results()
            
            # Navigation buttons for enhanced features
            st.markdown("**🔗 Enhanced Features:**")
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            
            with col1:
                if st.button("🔍 Enhanced Confidence", help="View detailed confidence metrics and visualizations"):
                    st.session_state.show_enhanced_confidence = True
                    st.rerun()
            
            with col2:
                if st.button("📊 Statistics Dashboard", help="View comprehensive statistics and metrics"):
                    st.session_state.show_statistics = True
                    st.rerun()
            
            with col3:
                if st.button("📚 Prediction History", help="View detailed prediction history and tracking"):
                    st.session_state.show_prediction_history = True
                    st.rerun()
            
            with col4:
                if st.button("🔄 Attention Comparison", help="Compare attention analysis with other texts"):
                    st.session_state.show_attention_comparison = True
                    st.rerun()
            
            with col5:
                if st.button("📚 Technical Guide", help="Learn about attention mechanisms and interpretation"):
                    st.session_state.show_technical_explanation = True
                    st.rerun()
            
            with col6:
                if st.button("🖼️ Export Visualizations", help="Export attention heatmaps and visualizations"):
                    st.session_state.show_visualization_export = True
                    st.rerun()
            
            with col7:
                if st.button("💾 Export Results", help="Export results to CSV, JSON, or Excel"):
                    st.session_state.show_export = True
                    st.rerun()
        
        # Sample Data and Learning Features
        st.markdown("**📚 Sample Data & Learning:**")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("📚 Sample Gallery", help="Explore curated sample texts for analysis"):
                st.session_state.show_sample_gallery = True
                st.rerun()
        
        with col2:
            if st.button("🔍 Results Comparison", help="Compare expected vs. actual results"):
                st.session_state.show_results_comparison = True
                st.rerun()
        
        with col3:
            if st.button("📖 Use Case Docs", help="Learn about different text types and applications"):
                st.session_state.show_use_case_docs = True
                st.rerun()
        
        with col4:
            if st.button("📊 Performance Benchmarks", help="View model performance metrics"):
                st.session_state.show_performance_benchmarks = True
                st.rerun()
        
        with col5:
            if st.button("🎓 Interactive Tutorial", help="Learn with guided tutorials"):
                st.session_state.show_tutorial = True
                st.rerun()
        
        # Display enhanced confidence metrics if requested
        if st.session_state.show_enhanced_confidence and st.session_state.last_analysis:
            display_enhanced_confidence()
        
        # Display statistics panel if requested
        if st.session_state.show_statistics:
            display_statistics_panel()
        
        # Display prediction history if requested
        if st.session_state.show_prediction_history:
            display_prediction_history()
        
        # Display export functionality if requested
        if st.session_state.get('show_export', False):
            display_export_section()
        
        # Display attention comparison if requested
        if st.session_state.get('show_attention_comparison', False):
            display_attention_comparison()
        
        # Display technical explanation if requested
        if st.session_state.get('show_technical_explanation', False):
            display_technical_explanation()
        
        # Display visualization export if requested
        if st.session_state.get('show_visualization_export', False):
            display_visualization_export()
        
        # Display sample data components if requested
        if st.session_state.get('show_sample_gallery', False):
            display_sample_gallery()
        
        if st.session_state.get('show_results_comparison', False):
            display_results_comparison()
        
        if st.session_state.get('show_use_case_docs', False):
            display_use_case_documentation()
        
        if st.session_state.get('show_performance_benchmarks', False):
            display_performance_benchmarks()
        
        if st.session_state.get('show_tutorial', False):
            display_interactive_tutorial()
        
        # Display analysis history
        if st.session_state.analysis_history:
            display_analysis_history()
        
        # Handle comparison text analysis if requested
        if st.session_state.get('show_comparison_analysis', False) and st.session_state.get('comparison_text'):
            perform_comparison_analysis(st.session_state.comparison_text)
            st.session_state.show_comparison_analysis = False
            st.session_state.comparison_text = None
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_visualization_export():
    """Display visualization export component."""
    if not st.session_state.last_analysis:
        return
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("🖼️ Export Visualizations")
    
    # Create visualization export component
    visualization_export = VisualizationExport()
    
    # Render the visualization export component
    visualization_export.render(st.session_state.last_analysis['result'])
    
    # Close button
    if st.button("❌ Close Export", help="Close the visualization export view"):
        st.session_state.show_visualization_export = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_technical_explanation():
    """Display technical explanation component."""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("📚 Technical Explanation: Attention Mechanisms")
    
    # Create technical explanation component
    technical_explanation = TechnicalExplanation()
    
    # Get current result if available for contextual examples
    current_result = st.session_state.get('last_analysis', {}).get('result') if st.session_state.get('last_analysis') else None
    
    # Render the technical explanation component
    technical_explanation.render(current_result)
    
    # Close button
    if st.button("❌ Close Technical Guide", help="Close the technical explanation view"):
        st.session_state.show_technical_explanation = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_attention_comparison():
    """Display attention comparison component."""
    if not st.session_state.last_analysis:
        return
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("🔄 Attention Comparison Analysis")
    
    # Create attention comparison component
    attention_comparison = AttentionComparison()
    
    # Get comparison result if available
    comparison_result = st.session_state.get('comparison_result')
    
    # Render the comparison component
    attention_comparison.render(st.session_state.last_analysis['result'], comparison_result)
    
    # Close button
    if st.button("❌ Close Comparison", help="Close the attention comparison view"):
        st.session_state.show_attention_comparison = False
        st.session_state.comparison_result = None
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def perform_comparison_analysis(text: str):
    """Perform sentiment analysis for comparison."""
    try:
        # Validate input
        is_valid, error_message, metadata = st.session_state.text_validator.validate_text(text)
        
        if not is_valid:
            st.error(f"Input validation failed: {error_message}")
            return
        
        # Check character limit for web interface (1000 chars as per AC)
        if len(text) > 1000:
            st.error("Text too long. Maximum 1000 characters allowed for web interface.")
            return
        
        # Get user preferences for attention analysis
        include_attention = st.session_state.get('user_preferences', {}).get('attention_analysis', False)
        
        # Perform analysis
        with st.spinner("Analyzing comparison text..." + (" (with attention analysis)" if include_attention else "")):
            result = st.session_state.sentiment_pipeline.predict(text, include_attention=include_attention)
            
            # Store as comparison result
            st.session_state.comparison_result = result
            
            st.success("Comparison analysis completed!")
            
    except Exception as e:
        st.error(f"Comparison analysis failed: {str(e)}")

def perform_sentiment_analysis(text: str):
    """Perform sentiment analysis on the input text."""
    try:
        # Validate input
        is_valid, error_message, metadata = st.session_state.text_validator.validate_text(text)
        
        if not is_valid:
            st.error(f"Input validation failed: {error_message}")
            return
        
        # Check character limit for web interface (1000 chars as per AC)
        if len(text) > 1000:
            st.error("Text too long. Maximum 1000 characters allowed for web interface.")
            return
        
        # Get user preferences for attention analysis
        include_attention = st.session_state.get('user_preferences', {}).get('attention_analysis', False)
        
        # Perform analysis
        with st.spinner("Analyzing sentiment..." + (" (with attention analysis)" if include_attention else "")):
            result = st.session_state.sentiment_pipeline.predict(text, include_attention=include_attention)
            
            # Store in session state
            st.session_state.last_analysis = {
                'input_text': text,
                'result': result,
                'metadata': metadata
            }
            
            # Add to history with proper timestamp
            analysis_entry = {
                'id': len(st.session_state.analysis_history) + 1,
                'timestamp': datetime.now(),
                'input_text': text,
                'result': result,
                'metadata': metadata
            }
            st.session_state.analysis_history.append(analysis_entry)
            
            # Keep only last 10 analyses
            if len(st.session_state.analysis_history) > 10:
                st.session_state.analysis_history.pop(0)
            
            st.success("Analysis completed successfully!")
            
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")

def display_analysis_results():
    """Display the current analysis results."""
    if not st.session_state.last_analysis:
        return
    
    analysis = st.session_state.last_analysis
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("📊 Analysis Results")
    
    # Create sentiment display component
    sentiment_display = SentimentDisplay()
    sentiment_display.render(analysis['result'])
    
    # Display input metadata
    with st.expander("📋 Input Details"):
        st.write(f"**Text Length:** {analysis['metadata'].get('length', len(analysis['input_text']))} characters")
        st.write(f"**Word Count:** {analysis['metadata'].get('word_count', len(analysis['input_text'].split()))}")
        st.write(f"**Processing Time:** {analysis['result']['processing_time_ms']:.2f} ms")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_analysis_history():
    """Display analysis history."""
    if not st.session_state.analysis_history:
        return
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("📚 Analysis History")
    
    for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:]), 1):
        with st.expander(f"Analysis {i}: {analysis['input_text'][:50]}{'...' if len(analysis['input_text']) > 50 else ''}"):
            sentiment_display = SentimentDisplay()
            sentiment_display.render(analysis['result'])
            st.write(f"**Input:** {analysis['input_text']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_enhanced_confidence():
    """Display enhanced confidence metrics."""
    if not st.session_state.last_analysis:
        return
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("🔍 Enhanced Confidence Metrics")
    
    # Create confidence metrics component
    confidence_metrics = ConfidenceMetrics()
    confidence_metrics.render(st.session_state.last_analysis['result'])
    
    # Close button
    if st.button("❌ Close Enhanced Metrics", help="Close the enhanced confidence metrics view"):
        st.session_state.show_enhanced_confidence = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_statistics_panel():
    """Display statistics panel."""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("📊 Statistics Dashboard")
    
    # Create statistics panel component
    statistics_panel = StatisticsPanel()
    
    # Convert analysis history to prediction history format
    prediction_history = []
    for analysis in st.session_state.analysis_history:
        if 'result' in analysis:
            prediction_entry = {
                'id': analysis.get('id', len(prediction_history) + 1),
                'timestamp': analysis.get('timestamp', datetime.now()),
                'input_text': analysis['input_text'],
                'sentiment_label': analysis['result'].get('sentiment_label', 'unknown'),
                'confidence_score': analysis['result'].get('confidence_score', 0.0),
                'processing_time_ms': analysis['result'].get('processing_time_ms', 0.0),
                'model_confidence': analysis['result'].get('model_confidence', [])
            }
            prediction_history.append(prediction_entry)
    
    statistics_panel.render(prediction_history)
    
    # Close button
    if st.button("❌ Close Statistics", help="Close the statistics dashboard"):
        st.session_state.show_statistics = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_prediction_history():
    """Display prediction history."""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("📚 Prediction History")
    
    # Create prediction history component
    prediction_history = PredictionHistory()
    
    # Convert analysis history to prediction history format
    history_data = []
    for analysis in st.session_state.analysis_history:
        if 'result' in analysis:
            prediction_entry = {
                'id': analysis.get('id', len(history_data) + 1),
                'timestamp': analysis.get('timestamp', datetime.now()),
                'input_text': analysis['input_text'],
                'sentiment_label': analysis['result'].get('sentiment_label', 'unknown'),
                'confidence_score': analysis['result'].get('confidence_score', 0.0),
                'processing_time_ms': analysis['result'].get('processing_time_ms', 0.0),
                'model_confidence': analysis['result'].get('model_confidence', [])
            }
            history_data.append(prediction_entry)
    
    prediction_history.render()
    
    # Close button
    if st.button("❌ Close History", help="Close the prediction history view"):
        st.session_state.show_prediction_history = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_export_section():
    """Display export functionality."""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("💾 Export Results")
    
    # Create CSV export component
    csv_export = CSVExport()
    
    # Convert analysis history to prediction history format for export
    prediction_history = []
    for analysis in st.session_state.analysis_history:
        if 'result' in analysis:
            prediction_entry = {
                'id': analysis.get('id', len(prediction_history) + 1),
                'timestamp': analysis.get('timestamp', datetime.now()),
                'input_text': analysis['input_text'],
                'sentiment_label': analysis['result'].get('sentiment_label', 'unknown'),
                'confidence_score': analysis['result'].get('confidence_score', 0.0),
                'processing_time_ms': analysis['result'].get('processing_time_ms', 0.0),
                'model_confidence': analysis['result'].get('model_confidence', [])
            }
            prediction_history.append(prediction_entry)
    
    # Prepare single result for export if available
    single_result = None
    if st.session_state.last_analysis:
        single_result = {
            'id': st.session_state.last_analysis.get('id', 1),
            'timestamp': st.session_state.last_analysis.get('timestamp', datetime.now()),
            'input_text': st.session_state.last_analysis['input_text'],
            'sentiment_label': st.session_state.last_analysis['result'].get('sentiment_label', 'unknown'),
            'confidence_score': st.session_state.last_analysis['result'].get('confidence_score', 0.0),
            'processing_time_ms': st.session_state.last_analysis['result'].get('processing_time_ms', 0.0),
            'model_confidence': st.session_state.last_analysis['result'].get('model_confidence', [])
        }
    
    csv_export.render(
        prediction_history=prediction_history,
        single_result=single_result
    )
    
    # Close button
    if st.button("❌ Close Export", help="Close the export section"):
        st.session_state.show_export = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_sample_gallery():
    """Display sample data gallery."""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("📚 Sample Data Gallery")
    
    # Create sample gallery component
    sample_gallery = ExampleGallery()
    
    # Callback function to load sample text into the main input
    def on_sample_select(text: str):
        st.session_state.current_input = text
        # Find the sample ID for this text
        sample_gallery = ExampleGallery()
        for sample in sample_gallery.samples:
            if sample['text'] == text:
                st.session_state.current_sample_id = sample['id']
                break
        st.success(f"Sample text loaded! Click 'Analyze Sentiment' to analyze it.")
    
    # Render the sample gallery component
    sample_gallery.render(on_sample_select)
    
    # Close button
    if st.button("❌ Close Sample Gallery", help="Close the sample gallery view"):
        st.session_state.show_sample_gallery = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_results_comparison():
    """Display results comparison component."""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("🔍 Results Comparison")
    
    # Check if we have a current analysis and sample ID
    if not st.session_state.last_analysis or not st.session_state.current_sample_id:
        st.info("Please analyze a sample from the Sample Gallery first to see the comparison.")
        
        # Close button
        if st.button("❌ Close Results Comparison", help="Close the results comparison view"):
            st.session_state.show_results_comparison = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Create results comparison component
    results_comparison = ResultsComparison()
    
    # Get attention data if available
    attention_data = st.session_state.last_analysis['result'].get('attention_data')
    
    # Render the results comparison component
    results_comparison.render_comparison(
        st.session_state.current_sample_id,
        st.session_state.last_analysis['result'],
        attention_data
    )
    
    # Close button
    if st.button("❌ Close Results Comparison", help="Close the results comparison view"):
        st.session_state.show_results_comparison = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_use_case_documentation():
    """Display use case documentation component."""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("📖 Use Case Documentation")
    
    # Create use case documentation component
    use_case_docs = UseCaseDocumentation()
    
    # Render the use case documentation component
    use_case_docs.render()
    
    # Close button
    if st.button("❌ Close Use Case Docs", help="Close the use case documentation view"):
        st.session_state.show_use_case_docs = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_performance_benchmarks():
    """Display performance benchmarks component."""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("📊 Performance Benchmarks")
    
    # Create performance benchmark component
    performance_benchmark = PerformanceBenchmark()
    
    # Render the performance benchmark component
    performance_benchmark.render()
    
    # Close button
    if st.button("❌ Close Performance Benchmarks", help="Close the performance benchmarks view"):
        st.session_state.show_performance_benchmarks = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_interactive_tutorial():
    """Display interactive tutorial component."""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.subheader("🎓 Interactive Tutorial")
    
    # Create interactive tutorial component
    tutorial = InteractiveTutorial()
    
    # Callback function to load sample text into the main input
    def on_sample_load(text: str):
        st.session_state.current_input = text
        st.success(f"Sample text loaded! Click 'Analyze Sentiment' to analyze it.")
    
    # Render the interactive tutorial component
    tutorial.render_current_tutorial(on_sample_load)
    
    # Close button
    if st.button("❌ Close Tutorial", help="Close the tutorial view"):
        st.session_state.show_tutorial = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
