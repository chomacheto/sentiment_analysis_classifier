"""
Use Case Documentation Component

This component provides detailed documentation about different text types,
their characteristics, and real-world use cases for sentiment analysis.
"""

import streamlit as st
import json
from typing import Dict, List, Optional, Any
from pathlib import Path


class UseCaseDocumentation:
    """Component for displaying use case documentation and examples."""
    
    def __init__(self, use_cases_path: str = "data/samples/use_cases.json"):
        """Initialize the UseCaseDocumentation component.
        
        Args:
            use_cases_path: Path to the use cases JSON file
        """
        self.use_cases_path = Path(use_cases_path)
        self.use_cases = self._load_use_cases()
        
    def _load_use_cases(self) -> List[Dict[str, Any]]:
        """Load use cases from JSON file.
        
        Returns:
            List of use case dictionaries
        """
        try:
            with open(self.use_cases_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('use_cases', [])
        except FileNotFoundError:
            st.error(f"Use cases file not found: {self.use_cases_path}")
            return []
        except json.JSONDecodeError:
            st.error(f"Invalid JSON in use cases file: {self.use_cases_path}")
            return []
    
    def render(self) -> None:
        """Render the use case documentation interface."""
        st.subheader("📖 Use Case Documentation")
        st.markdown("Learn about different text types and their real-world applications in sentiment analysis.")
        
        # Category selection
        selected_category = st.selectbox(
            "Select a text category to explore:",
            [uc['category'] for uc in self.use_cases],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="use_case_category_selector"
        )
        
        # Display selected use case
        use_case = self._get_use_case_by_category(selected_category)
        if use_case:
            self._render_use_case_details(use_case)
    
    def _get_use_case_by_category(self, category: str) -> Optional[Dict[str, Any]]:
        """Get use case by category.
        
        Args:
            category: Category to retrieve
            
        Returns:
            Use case dictionary or None if not found
        """
        for use_case in self.use_cases:
            if use_case['category'] == category:
                return use_case
        return None
    
    def _render_use_case_details(self, use_case: Dict[str, Any]) -> None:
        """Render detailed information about a use case.
        
        Args:
            use_case: Use case dictionary
        """
        # Header
        st.markdown(f"## {use_case['name']}")
        st.markdown(f"*{use_case['description']}*")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Characteristics", 
            "🌍 Real-World Scenarios", 
            "💡 Best Practices", 
            "🏢 Industry Examples",
            "📊 Performance Insights"
        ])
        
        with tab1:
            self._render_characteristics(use_case)
        
        with tab2:
            self._render_real_world_scenarios(use_case)
        
        with tab3:
            self._render_best_practices(use_case)
        
        with tab4:
            self._render_industry_examples(use_case)
        
        with tab5:
            self._render_performance_insights(use_case)
    
    def _render_characteristics(self, use_case: Dict[str, Any]) -> None:
        """Render text characteristics section.
        
        Args:
            use_case: Use case dictionary
        """
        st.markdown("### Text Characteristics")
        st.markdown("Understanding the key characteristics of this text type helps improve sentiment analysis accuracy.")
        
        characteristics = use_case.get('characteristics', [])
        if characteristics:
            for i, char in enumerate(characteristics, 1):
                st.markdown(f"**{i}.** {char}")
        else:
            st.info("No specific characteristics documented for this text type.")
        
        # Add visual indicators
        st.markdown("---")
        st.markdown("**Key Indicators:**")
        
        # Category-specific indicators
        indicators = self._get_category_indicators(use_case['category'])
        for indicator in indicators:
            st.markdown(f"• {indicator}")
    
    def _render_real_world_scenarios(self, use_case: Dict[str, Any]) -> None:
        """Render real-world scenarios section.
        
        Args:
            use_case: Use case dictionary
        """
        st.markdown("### Real-World Scenarios")
        st.markdown("These are common situations where you might encounter this type of text.")
        
        scenarios = use_case.get('real_world_scenarios', [])
        if scenarios:
            for i, scenario in enumerate(scenarios, 1):
                st.markdown(f"**{i}.** {scenario}")
        else:
            st.info("No real-world scenarios documented for this text type.")
        
        # Add practical examples
        st.markdown("---")
        st.markdown("**Practical Applications:**")
        
        # Category-specific applications
        applications = self._get_category_applications(use_case['category'])
        for app in applications:
            st.markdown(f"• {app}")
    
    def _render_best_practices(self, use_case: Dict[str, Any]) -> None:
        """Render best practices section.
        
        Args:
            use_case: Use case dictionary
        """
        st.markdown("### Best Practices")
        st.markdown("Follow these guidelines to improve sentiment analysis accuracy for this text type.")
        
        practices = use_case.get('best_practices', [])
        if practices:
            for i, practice in enumerate(practices, 1):
                st.markdown(f"**{i}.** {practice}")
        else:
            st.info("No best practices documented for this text type.")
        
        # Add tips and warnings
        st.markdown("---")
        st.markdown("**Pro Tips:**")
        
        # Category-specific tips
        tips = self._get_category_tips(use_case['category'])
        for tip in tips:
            st.markdown(f"💡 {tip}")
    
    def _render_industry_examples(self, use_case: Dict[str, Any]) -> None:
        """Render industry examples section.
        
        Args:
            use_case: Use case dictionary
        """
        st.markdown("### Industry Examples")
        st.markdown("See how companies and organizations use sentiment analysis for this text type.")
        
        examples = use_case.get('industry_examples', [])
        if examples:
            for i, example in enumerate(examples, 1):
                st.markdown(f"**{i}.** {example}")
        else:
            st.info("No industry examples documented for this text type.")
        
        # Add case studies
        st.markdown("---")
        st.markdown("**Case Studies:**")
        
        # Category-specific case studies
        case_studies = self._get_category_case_studies(use_case['category'])
        for case in case_studies:
            st.markdown(f"📊 {case}")
    
    def _render_performance_insights(self, use_case: Dict[str, Any]) -> None:
        """Render performance insights section.
        
        Args:
            use_case: Use case dictionary
        """
        st.markdown("### Performance Insights")
        st.markdown("Understanding typical performance characteristics for this text type.")
        
        # Load benchmark data
        benchmark_data = self._load_benchmark_data()
        if benchmark_data:
            category = use_case['category']
            category_performance = benchmark_data.get('model_performance', {}).get('by_category', {}).get(category, {})
            
            if category_performance:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Accuracy", f"{category_performance.get('accuracy', 0):.1%}")
                
                with col2:
                    st.metric("Precision", f"{category_performance.get('precision', 0):.1%}")
                
                with col3:
                    st.metric("Recall", f"{category_performance.get('recall', 0):.1%}")
                
                with col4:
                    st.metric("F1 Score", f"{category_performance.get('f1_score', 0):.1%}")
                
                # Performance notes
                if category_performance.get('notes'):
                    st.info(category_performance['notes'])
            else:
                st.info("No performance data available for this category.")
        else:
            st.info("Performance data not available.")
        
        # Add difficulty insights
        st.markdown("---")
        st.markdown("**Difficulty Insights:**")
        
        difficulty_insights = self._get_difficulty_insights(use_case['category'])
        for insight in difficulty_insights:
            st.markdown(f"• {insight}")
    
    def _load_benchmark_data(self) -> Optional[Dict[str, Any]]:
        """Load benchmark data for performance insights.
        
        Returns:
            Benchmark data dictionary or None
        """
        try:
            benchmark_path = Path("data/samples/benchmarks.json")
            with open(benchmark_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def _get_category_indicators(self, category: str) -> List[str]:
        """Get category-specific indicators.
        
        Args:
            category: Text category
            
        Returns:
            List of indicators
        """
        indicators_map = {
            'movie_review': [
                "Emotional language and personal opinions",
                "Technical film terminology",
                "Comparative language and recommendations",
                "Star ratings or numerical scores"
            ],
            'social_media': [
                "Informal language and abbreviations",
                "Emojis, hashtags, and mentions",
                "Short, concise messages",
                "Real-time, trending content"
            ],
            'formal': [
                "Professional, objective language",
                "Technical terminology and jargon",
                "Structured format with headings",
                "Factual information and data"
            ],
            'sarcasm': [
                "Positive words with negative intent",
                "Exaggeration and hyperbole",
                "Quotation marks for emphasis",
                "Context-dependent meaning"
            ],
            'feedback': [
                "Specific product/service details",
                "Personal experiences and recommendations",
                "Actionable suggestions",
                "Credibility indicators"
            ],
            'news': [
                "Factual reporting language",
                "Editorial bias indicators",
                "Current events and breaking news",
                "Multiple viewpoints and quotes"
            ],
            'technical': [
                "Technical terminology and specifications",
                "Functionality and performance focus",
                "Code examples and technical details",
                "Objective, analytical language"
            ],
            'emotional': [
                "Strong emotional language",
                "Personal experiences and feelings",
                "Mental health indicators",
                "Highly subjective content"
            ]
        }
        
        return indicators_map.get(category, ["This text type has unique characteristics."])
    
    def _get_category_applications(self, category: str) -> List[str]:
        """Get category-specific applications.
        
        Args:
            category: Text category
            
        Returns:
            List of applications
        """
        applications_map = {
            'movie_review': [
                "Content recommendation systems",
                "Marketing campaign analysis",
                "Audience sentiment tracking",
                "Film industry market research"
            ],
            'social_media': [
                "Brand monitoring and reputation management",
                "Trend analysis and viral content detection",
                "Crisis communication and public relations",
                "Political campaign sentiment tracking"
            ],
            'formal': [
                "Compliance monitoring and risk assessment",
                "Business intelligence and market analysis",
                "Legal document review and analysis",
                "Academic research sentiment analysis"
            ],
            'sarcasm': [
                "Customer service complaint detection",
                "Social media sentiment analysis",
                "Political commentary analysis",
                "Entertainment and humor content analysis"
            ],
            'feedback': [
                "Product improvement and development",
                "Customer satisfaction monitoring",
                "Service quality assessment",
                "Market research and competitive analysis"
            ],
            'news': [
                "Media monitoring and brand mentions",
                "Public opinion tracking",
                "Market sentiment analysis",
                "Crisis management and public relations"
            ],
            'technical': [
                "Developer experience improvement",
                "API and framework feedback analysis",
                "Technical documentation review",
                "Software product development"
            ],
            'emotional': [
                "Mental health monitoring and support",
                "Personal development and wellness tracking",
                "Social media safety and content moderation",
                "Research on emotional expression"
            ]
        }
        
        return applications_map.get(category, ["This text type has various applications."])
    
    def _get_category_tips(self, category: str) -> List[str]:
        """Get category-specific tips.
        
        Args:
            category: Text category
            
        Returns:
            List of tips
        """
        tips_map = {
            'movie_review': [
                "Consider the reviewer's expertise level and background",
                "Look for genre-specific language patterns",
                "Account for cultural differences in film appreciation",
                "Consider the timing of reviews relative to release"
            ],
            'social_media': [
                "Monitor for trending hashtags and topics",
                "Account for platform-specific language patterns",
                "Consider user demographics and audience",
                "Look for sarcasm and internet slang"
            ],
            'formal': [
                "Focus on factual content over emotional language",
                "Consider document type and industry context",
                "Account for technical terminology and jargon",
                "Look for subtle sentiment indicators"
            ],
            'sarcasm': [
                "Consider context and background information",
                "Look for linguistic markers of sarcasm",
                "Account for cultural and regional differences",
                "Use additional context clues beyond text"
            ],
            'feedback': [
                "Focus on specific feedback points and suggestions",
                "Consider review authenticity and credibility",
                "Account for review length and detail level",
                "Look for actionable insights"
            ],
            'news': [
                "Distinguish between factual reporting and opinion",
                "Consider source credibility and bias",
                "Account for breaking news vs. analysis pieces",
                "Look for editorial slant and perspective"
            ],
            'technical': [
                "Focus on technical accuracy and usability",
                "Consider technical expertise level of audience",
                "Account for industry-specific terminology",
                "Look for specific technical issues"
            ],
            'emotional': [
                "Handle with sensitivity and privacy considerations",
                "Consider mental health implications",
                "Account for personal context and background",
                "Look for patterns over time"
            ]
        }
        
        return tips_map.get(category, ["Consider the unique characteristics of this text type."])
    
    def _get_category_case_studies(self, category: str) -> List[str]:
        """Get category-specific case studies.
        
        Args:
            category: Text category
            
        Returns:
            List of case studies
        """
        case_studies_map = {
            'movie_review': [
                "Netflix using sentiment analysis for content acquisition decisions",
                "IMDb aggregating user reviews for movie ratings and recommendations",
                "Movie marketing teams analyzing trailer reactions and audience feedback",
                "Film festivals using sentiment for award considerations and programming"
            ],
            'social_media': [
                "Social media agencies monitoring client brands for reputation management",
                "Political campaigns tracking public opinion and sentiment shifts",
                "E-commerce companies monitoring product mentions and customer feedback",
                "News organizations tracking public reaction to major events"
            ],
            'formal': [
                "Banks analyzing financial reports for risk assessment and compliance",
                "Law firms reviewing legal documents for sentiment and bias detection",
                "Universities analyzing research paper sentiment for academic insights",
                "Consulting firms analyzing business reports for market intelligence"
            ],
            'sarcasm': [
                "Customer service teams identifying sarcastic complaints for priority handling",
                "Social media managers handling ironic brand mentions and responses",
                "Political analysts tracking satirical commentary and public sentiment",
                "Entertainment companies analyzing humor content and audience reception"
            ],
            'feedback': [
                "Amazon analyzing product reviews for improvement and recommendation systems",
                "Restaurant chains monitoring customer feedback for service improvement",
                "Software companies analyzing app store reviews for product development",
                "Hotels tracking guest satisfaction surveys for service optimization"
            ],
            'news': [
                "PR firms monitoring media coverage for clients and crisis management",
                "Financial institutions analyzing market news sentiment for trading decisions",
                "Political campaigns tracking media coverage and public opinion",
                "News organizations analyzing reader engagement and content optimization"
            ],
            'technical': [
                "Software companies analyzing developer feedback for API improvements",
                "API providers monitoring developer sentiment for platform optimization",
                "Technical documentation teams improving content based on user feedback",
                "Open source projects analyzing community feedback for feature development"
            ],
            'emotional': [
                "Mental health apps monitoring user sentiment for wellness tracking",
                "Social media platforms detecting concerning content for safety measures",
                "Personal development apps tracking mood and emotional patterns",
                "Research institutions studying emotional expression and mental health"
            ]
        }
        
        return case_studies_map.get(category, ["Various organizations use this text type for analysis."])
    
    def _get_difficulty_insights(self, category: str) -> List[str]:
        """Get difficulty insights for a category.
        
        Args:
            category: Text category
            
        Returns:
            List of difficulty insights
        """
        difficulty_map = {
            'movie_review': [
                "Generally easier due to clear sentiment indicators",
                "Longer text provides more context for analysis",
                "Specific film terminology can be learned patterns",
                "Mixed reviews can be challenging due to conflicting elements"
            ],
            'social_media': [
                "Moderate difficulty due to informal language",
                "Short text limits context availability",
                "Emojis and hashtags provide additional sentiment cues",
                "Sarcasm and internet slang increase complexity"
            ],
            'formal': [
                "Moderate difficulty with subtle sentiment indicators",
                "Objective language can mask underlying sentiment",
                "Technical terminology requires domain knowledge",
                "Structured format can help with analysis"
            ],
            'sarcasm': [
                "High difficulty due to context-dependent meaning",
                "Requires understanding of irony and cultural context",
                "Positive words with negative intent are challenging",
                "Background knowledge is often necessary"
            ],
            'feedback': [
                "Moderate difficulty with specific domain language",
                "Mixed sentiment in reviews can be complex",
                "Authenticity detection adds complexity",
                "Actionable insights require careful analysis"
            ],
            'news': [
                "Moderate difficulty balancing objectivity and bias",
                "Breaking news vs. analysis requires different approaches",
                "Source credibility affects sentiment interpretation",
                "Editorial content can have subtle sentiment indicators"
            ],
            'technical': [
                "Moderate difficulty with technical terminology",
                "Objective language can mask sentiment",
                "Technical accuracy vs. sentiment can conflict",
                "Expertise level affects interpretation"
            ],
            'emotional': [
                "Moderate difficulty with personal context",
                "Strong emotional language provides clear indicators",
                "Privacy and sensitivity considerations important",
                "Cultural differences affect emotional expression"
            ]
        }
        
        return difficulty_map.get(category, ["This text type has varying levels of analysis difficulty."])
    
    def render_overview(self) -> None:
        """Render an overview of all use cases."""
        st.subheader("📚 Use Cases Overview")
        st.markdown("Explore different text types and their applications in sentiment analysis.")
        
        # Create a summary table
        summary_data = []
        for use_case in self.use_cases:
            summary_data.append({
                'Category': use_case['category'].replace('_', ' ').title(),
                'Name': use_case['name'],
                'Description': use_case['description'][:100] + "...",
                'Difficulty': self._get_category_difficulty(use_case['category'])
            })
        
        if summary_data:
            import pandas as pd
            df = pd.DataFrame(summary_data)
            st.table(df)
    
    def _get_category_difficulty(self, category: str) -> str:
        """Get difficulty level for a category.
        
        Args:
            category: Text category
            
        Returns:
            Difficulty level string
        """
        difficulty_map = {
            'movie_review': 'Easy',
            'social_media': 'Medium',
            'formal': 'Medium',
            'sarcasm': 'Hard',
            'feedback': 'Medium',
            'news': 'Medium',
            'technical': 'Medium',
            'emotional': 'Medium'
        }
        
        return difficulty_map.get(category, 'Medium')


def render_use_case_documentation() -> None:
    """Convenience function to render use case documentation."""
    doc = UseCaseDocumentation()
    doc.render()


def render_use_case_overview() -> None:
    """Convenience function to render use case overview."""
    doc = UseCaseDocumentation()
    doc.render_overview()


if __name__ == "__main__":
    # Test the component
    render_use_case_documentation()
