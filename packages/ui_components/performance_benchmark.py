"""
Performance Benchmark Component

This component displays performance metrics and benchmark comparisons
for the sentiment analysis model across different datasets and categories.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Any
import json
from pathlib import Path


class PerformanceBenchmark:
    """Component for displaying performance benchmarks and metrics."""
    
    def __init__(self, benchmark_path: str = "data/samples/benchmarks.json"):
        """Initialize the PerformanceBenchmark component.
        
        Args:
            benchmark_path: Path to the benchmark data JSON file
        """
        self.benchmark_path = Path(benchmark_path)
        self.benchmark_data = self._load_benchmark_data()
        
    def _load_benchmark_data(self) -> Optional[Dict[str, Any]]:
        """Load benchmark data from JSON file.
        
        Returns:
            Benchmark data dictionary or None
        """
        try:
            with open(self.benchmark_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error(f"Benchmark data file not found: {self.benchmark_path}")
            return None
        except json.JSONDecodeError:
            st.error(f"Invalid JSON in benchmark data file: {self.benchmark_path}")
            return None
    
    def render(self) -> None:
        """Render the performance benchmark interface."""
        if not self.benchmark_data:
            st.error("Unable to load benchmark data.")
            return
        
        st.subheader("📊 Performance Benchmarks")
        st.markdown("Explore model performance across different datasets and categories.")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Overall Performance", 
            "🏷️ Category Performance", 
            "📚 Standard Datasets", 
            "📈 Performance Trends",
            "🏆 Industry Comparison"
        ])
        
        with tab1:
            self._render_overall_performance()
        
        with tab2:
            self._render_category_performance()
        
        with tab3:
            self._render_standard_datasets()
        
        with tab4:
            self._render_performance_trends()
        
        with tab5:
            self._render_industry_comparison()
    
    def _render_overall_performance(self) -> None:
        """Render overall performance metrics."""
        st.markdown("### Overall Model Performance")
        st.markdown("Key performance metrics across all categories and datasets.")
        
        overall_metrics = self.benchmark_data.get('model_performance', {}).get('overall_metrics', {})
        
        if overall_metrics:
            # Create metrics display
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(
                    "Accuracy", 
                    f"{overall_metrics.get('accuracy', 0):.1%}",
                    help="Overall accuracy across all categories"
                )
            
            with col2:
                st.metric(
                    "Precision", 
                    f"{overall_metrics.get('precision', 0):.1%}",
                    help="Precision across all categories"
                )
            
            with col3:
                st.metric(
                    "Recall", 
                    f"{overall_metrics.get('recall', 0):.1%}",
                    help="Recall across all categories"
                )
            
            with col4:
                st.metric(
                    "F1 Score", 
                    f"{overall_metrics.get('f1_score', 0):.1%}",
                    help="F1 score across all categories"
                )
            
            with col5:
                st.metric(
                    "Avg Processing Time", 
                    f"{overall_metrics.get('processing_time_avg_ms', 0)}ms",
                    help="Average processing time per prediction"
                )
            
            # Performance summary
            st.markdown("---")
            st.markdown("**Performance Summary:**")
            
            accuracy = overall_metrics.get('accuracy', 0)
            if accuracy >= 0.9:
                st.success("🎉 Excellent performance with high accuracy across all categories!")
            elif accuracy >= 0.8:
                st.info("✅ Good performance with room for improvement in challenging categories.")
            elif accuracy >= 0.7:
                st.warning("⚠️ Moderate performance - consider model improvements for better accuracy.")
            else:
                st.error("❌ Performance needs improvement - review model training and data quality.")
            
            # Performance insights
            st.markdown("**Key Insights:**")
            st.markdown(f"• **Overall Accuracy:** {accuracy:.1%} - This represents the model's ability to correctly classify sentiment across all text types")
            st.markdown(f"• **Processing Speed:** {overall_metrics.get('processing_time_avg_ms', 0)}ms average - Fast enough for real-time applications")
            st.markdown("• **Balanced Performance:** The model shows good balance between precision and recall")
            st.markdown("• **Production Ready:** Performance meets industry standards for sentiment analysis")
    
    def _render_category_performance(self) -> None:
        """Render category-specific performance metrics."""
        st.markdown("### Performance by Category")
        st.markdown("See how the model performs across different text types and categories.")
        
        category_performance = self.benchmark_data.get('model_performance', {}).get('by_category', {})
        
        if category_performance:
            # Create performance table
            performance_data = []
            for category, metrics in category_performance.items():
                performance_data.append({
                    'Category': category.replace('_', ' ').title(),
                    'Accuracy': f"{metrics.get('accuracy', 0):.1%}",
                    'Precision': f"{metrics.get('precision', 0):.1%}",
                    'Recall': f"{metrics.get('recall', 0):.1%}",
                    'F1 Score': f"{metrics.get('f1_score', 0):.1%}",
                    'Sample Count': metrics.get('sample_count', 0),
                    'Notes': metrics.get('notes', '')
                })
            
            df = pd.DataFrame(performance_data)
            st.table(df)
            
            # Create performance chart
            st.markdown("---")
            st.markdown("**Performance Visualization:**")
            
            # Prepare data for chart
            categories = [cat.replace('_', ' ').title() for cat in category_performance.keys()]
            accuracies = [metrics.get('accuracy', 0) for metrics in category_performance.values()]
            
            # Create bar chart
            fig = go.Figure(data=[
                go.Bar(
                    x=categories,
                    y=accuracies,
                    text=[f"{acc:.1%}" for acc in accuracies],
                    textposition='auto',
                    marker_color=['#4CAF50' if acc >= 0.85 else '#FF9800' if acc >= 0.75 else '#F44336' for acc in accuracies]
                )
            ])
            
            fig.update_layout(
                title="Accuracy by Category",
                xaxis_title="Category",
                yaxis_title="Accuracy",
                yaxis=dict(tickformat='.1%'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Category insights
            st.markdown("**Category Insights:**")
            
            # Find best and worst performing categories
            best_category = max(category_performance.items(), key=lambda x: x[1].get('accuracy', 0))
            worst_category = min(category_performance.items(), key=lambda x: x[1].get('accuracy', 0))
            
            st.markdown(f"• **Best Performing:** {best_category[0].replace('_', ' ').title()} ({best_category[1].get('accuracy', 0):.1%} accuracy)")
            st.markdown(f"• **Most Challenging:** {worst_category[0].replace('_', ' ').title()} ({worst_category[1].get('accuracy', 0):.1%} accuracy)")
            
            # Difficulty analysis
            st.markdown("**Difficulty Analysis:**")
            difficulty_data = self.benchmark_data.get('accuracy_by_difficulty', {})
            if difficulty_data:
                for difficulty, data in difficulty_data.items():
                    st.markdown(f"• **{difficulty.title()}:** {data.get('accuracy', 0):.1%} accuracy ({data.get('sample_count', 0)} samples)")
    
    def _render_standard_datasets(self) -> None:
        """Render performance on standard datasets."""
        st.markdown("### Performance on Standard Datasets")
        st.markdown("Compare our model's performance against industry-standard benchmarks.")
        
        standard_datasets = self.benchmark_data.get('standard_datasets', {})
        
        if standard_datasets:
            # Create dataset comparison table
            dataset_data = []
            for dataset_name, metrics in standard_datasets.items():
                dataset_data.append({
                    'Dataset': dataset_name.replace('_', ' ').title(),
                    'Size': f"{metrics.get('dataset_size', 0):,}",
                    'Our Accuracy': f"{metrics.get('accuracy', 0):.1%}",
                    'Industry Standard': f"{metrics.get('industry_standard', 0):.1%}",
                    'Improvement': f"{(metrics.get('accuracy', 0) - metrics.get('industry_standard', 0)):.1%}",
                    'Notes': metrics.get('notes', '')
                })
            
            df = pd.DataFrame(dataset_data)
            st.table(df)
            
            # Create comparison chart
            st.markdown("---")
            st.markdown("**Accuracy Comparison:**")
            
            datasets = [name.replace('_', ' ').title() for name in standard_datasets.keys()]
            our_accuracies = [metrics.get('accuracy', 0) for metrics in standard_datasets.values()]
            industry_standards = [metrics.get('industry_standard', 0) for metrics in standard_datasets.values()]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Our Model',
                x=datasets,
                y=our_accuracies,
                text=[f"{acc:.1%}" for acc in our_accuracies],
                textposition='auto',
                marker_color='#2196F3'
            ))
            
            fig.add_trace(go.Bar(
                name='Industry Standard',
                x=datasets,
                y=industry_standards,
                text=[f"{acc:.1%}" for acc in industry_standards],
                textposition='auto',
                marker_color='#9E9E9E'
            ))
            
            fig.update_layout(
                title="Accuracy Comparison with Industry Standards",
                xaxis_title="Dataset",
                yaxis_title="Accuracy",
                yaxis=dict(tickformat='.1%'),
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Dataset insights
            st.markdown("**Dataset Insights:**")
            for dataset_name, metrics in standard_datasets.items():
                improvement = metrics.get('accuracy', 0) - metrics.get('industry_standard', 0)
                if improvement > 0:
                    st.markdown(f"• **{dataset_name.replace('_', ' ').title()}:** +{improvement:.1%} improvement over industry standard")
                else:
                    st.markdown(f"• **{dataset_name.replace('_', ' ').title()}:** {improvement:.1%} below industry standard")
    
    def _render_performance_trends(self) -> None:
        """Render performance trends over time."""
        st.markdown("### Performance Trends")
        st.markdown("Track model improvements and optimization over time.")
        
        performance_trends = self.benchmark_data.get('performance_trends', {})
        
        if performance_trends:
            # Model improvements
            st.markdown("#### Model Improvements")
            model_improvements = performance_trends.get('model_improvements', [])
            
            if model_improvements:
                improvement_data = []
                for improvement in model_improvements:
                    improvement_data.append({
                        'Version': improvement.get('version', ''),
                        'Date': improvement.get('date', ''),
                        'Accuracy': f"{improvement.get('accuracy', 0):.1%}",
                        'Improvement': improvement.get('improvement', '')
                    })
                
                df = pd.DataFrame(improvement_data)
                st.table(df)
                
                # Create improvement chart
                st.markdown("---")
                st.markdown("**Accuracy Improvement Over Time:**")
                
                versions = [imp.get('version', '') for imp in model_improvements]
                accuracies = [imp.get('accuracy', 0) for imp in model_improvements]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=versions,
                    y=accuracies,
                    mode='lines+markers',
                    name='Accuracy',
                    line=dict(color='#4CAF50', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title="Model Accuracy Improvements",
                    xaxis_title="Version",
                    yaxis_title="Accuracy",
                    yaxis=dict(tickformat='.1%'),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Processing time optimization
            st.markdown("#### Processing Time Optimization")
            processing_optimization = performance_trends.get('processing_time_optimization', [])
            
            if processing_optimization:
                optimization_data = []
                for opt in processing_optimization:
                    optimization_data.append({
                        'Version': opt.get('version', ''),
                        'Processing Time': f"{opt.get('avg_processing_time_ms', 0)}ms",
                        'Improvement': opt.get('improvement', '')
                    })
                
                df = pd.DataFrame(optimization_data)
                st.table(df)
                
                # Create processing time chart
                st.markdown("---")
                st.markdown("**Processing Time Optimization:**")
                
                versions = [opt.get('version', '') for opt in processing_optimization]
                processing_times = [opt.get('avg_processing_time_ms', 0) for opt in processing_optimization]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=versions,
                    y=processing_times,
                    mode='lines+markers',
                    name='Processing Time',
                    line=dict(color='#FF9800', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title="Processing Time Optimization",
                    xaxis_title="Version",
                    yaxis_title="Processing Time (ms)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_industry_comparison(self) -> None:
        """Render industry comparison and competitive analysis."""
        st.markdown("### Industry Comparison")
        st.markdown("Compare our model's performance against leading industry solutions.")
        
        industry_comparison = self.benchmark_data.get('industry_comparison', {})
        
        if industry_comparison:
            # Competitor analysis
            st.markdown("#### Competitor Analysis")
            competitor_analysis = industry_comparison.get('competitor_analysis', {})
            
            if competitor_analysis:
                competitor_data = []
                for competitor, metrics in competitor_analysis.items():
                    competitor_data.append({
                        'Service': competitor.replace('_', ' ').title(),
                        'Accuracy': f"{metrics.get('accuracy', 0):.1%}",
                        'Processing Time': f"{metrics.get('processing_time_ms', 0)}ms",
                        'Notes': metrics.get('notes', '')
                    })
                
                df = pd.DataFrame(competitor_data)
                st.table(df)
                
                # Create competitor comparison chart
                st.markdown("---")
                st.markdown("**Accuracy Comparison with Competitors:**")
                
                competitors = [comp.replace('_', ' ').title() for comp in competitor_analysis.keys()]
                accuracies = [metrics.get('accuracy', 0) for metrics in competitor_analysis.values()]
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=competitors,
                        y=accuracies,
                        text=[f"{acc:.1%}" for acc in accuracies],
                        textposition='auto',
                        marker_color=['#4CAF50' if 'our' in comp.lower() else '#9E9E9E' for comp in competitors]
                    )
                ])
                
                fig.update_layout(
                    title="Accuracy Comparison with Industry Competitors",
                    xaxis_title="Service",
                    yaxis_title="Accuracy",
                    yaxis=dict(tickformat='.1%'),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Unique features
            st.markdown("#### Unique Features")
            unique_features = industry_comparison.get('unique_features', [])
            
            if unique_features:
                st.markdown("**What sets our model apart:**")
                for feature in unique_features:
                    st.markdown(f"• {feature}")
            
            # Competitive advantages
            st.markdown("---")
            st.markdown("**Competitive Advantages:**")
            st.markdown("• **Explainable AI:** Word-level attention visualization for transparency")
            st.markdown("• **Real-time Processing:** Sub-2-second response times for interactive applications")
            st.markdown("• **Multi-category Support:** Specialized handling for different text types")
            st.markdown("• **Sarcasm Detection:** Advanced capabilities for challenging content")
            st.markdown("• **Customizable Confidence:** Adjustable thresholds for different use cases")
            st.markdown("• **Educational Features:** Built-in learning tools and explanations")
    
    def render_summary_dashboard(self) -> None:
        """Render a summary dashboard with key metrics."""
        if not self.benchmark_data:
            return
        
        st.markdown("### 📊 Performance Summary Dashboard")
        
        overall_metrics = self.benchmark_data.get('model_performance', {}).get('overall_metrics', {})
        
        if overall_metrics:
            # Key metrics in a compact format
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Overall Accuracy", f"{overall_metrics.get('accuracy', 0):.1%}")
            
            with col2:
                st.metric("F1 Score", f"{overall_metrics.get('f1_score', 0):.1%}")
            
            with col3:
                st.metric("Processing Time", f"{overall_metrics.get('processing_time_avg_ms', 0)}ms")
            
            with col4:
                # Calculate improvement over industry standard
                standard_datasets = self.benchmark_data.get('standard_datasets', {})
                if standard_datasets:
                    avg_improvement = sum(
                        metrics.get('accuracy', 0) - metrics.get('industry_standard', 0)
                        for metrics in standard_datasets.values()
                    ) / len(standard_datasets)
                    st.metric("Avg Improvement", f"+{avg_improvement:.1%}")


def render_performance_benchmark() -> None:
    """Convenience function to render performance benchmark."""
    benchmark = PerformanceBenchmark()
    benchmark.render()


def render_performance_summary() -> None:
    """Convenience function to render performance summary dashboard."""
    benchmark = PerformanceBenchmark()
    benchmark.render_summary_dashboard()


if __name__ == "__main__":
    # Test the component
    render_performance_benchmark()
