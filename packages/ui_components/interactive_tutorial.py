"""
Interactive Tutorial Component

This component provides guided learning experiences for first-time users
and advanced tutorials for power users and data scientists.
"""

import streamlit as st
import json
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path


class InteractiveTutorial:
    """Component for interactive tutorials and guided learning."""
    
    def __init__(self):
        """Initialize the InteractiveTutorial component."""
        self.tutorials = self._load_tutorials()
        self.current_tutorial = None
        self.current_step = 0
        
    def _load_tutorials(self) -> Dict[str, Any]:
        """Load tutorial definitions.
        
        Returns:
            Dictionary of tutorial definitions
        """
        return {
            "beginner": {
                "title": "Beginner Tutorial",
                "description": "Learn the basics of sentiment analysis and how to use this tool",
                "steps": [
                    {
                        "title": "Welcome to Sentiment Analysis",
                        "content": "Welcome! This tutorial will guide you through the basics of sentiment analysis and how to use this tool effectively.",
                        "action": "info",
                        "highlight_element": None
                    },
                    {
                        "title": "Understanding Sentiment Analysis",
                        "content": "Sentiment analysis is the process of determining whether a piece of text expresses positive, negative, or neutral sentiment. This tool uses advanced AI to analyze text and provide insights.",
                        "action": "info",
                        "highlight_element": None
                    },
                    {
                        "title": "Text Input",
                        "content": "Start by entering your text in the text area. You can analyze any type of text - from social media posts to business documents.",
                        "action": "highlight",
                        "highlight_element": "text_input",
                        "sample_text": "I love this product! It's amazing and works perfectly."
                    },
                    {
                        "title": "Running Analysis",
                        "content": "Click the 'Analyze Sentiment' button to process your text. The model will analyze the sentiment and provide results.",
                        "action": "highlight",
                        "highlight_element": "analyze_button"
                    },
                    {
                        "title": "Understanding Results",
                        "content": "The results show the predicted sentiment (positive, negative, or neutral), confidence score, and processing time. Higher confidence means the model is more certain about its prediction.",
                        "action": "highlight",
                        "highlight_element": "results_section"
                    },
                    {
                        "title": "Sample Data Gallery",
                        "content": "Explore the Sample Data Gallery to see examples of different text types and how they're analyzed. This helps you understand what to expect.",
                        "action": "highlight",
                        "highlight_element": "sample_gallery"
                    },
                    {
                        "title": "Congratulations!",
                        "content": "You've completed the beginner tutorial! You now know how to use the basic features of this sentiment analysis tool. Try analyzing some text of your own!",
                        "action": "success",
                        "highlight_element": None
                    }
                ]
            },
            "intermediate": {
                "title": "Intermediate Tutorial",
                "description": "Learn about advanced features and interpretation techniques",
                "steps": [
                    {
                        "title": "Advanced Features Overview",
                        "content": "Welcome to the intermediate tutorial! You'll learn about attention visualizations, confidence scores, and advanced interpretation techniques.",
                        "action": "info",
                        "highlight_element": None
                    },
                    {
                        "title": "Attention Visualization",
                        "content": "The attention visualization shows which words the model focused on when making its prediction. This helps you understand how the model 'thinks' about your text.",
                        "action": "highlight",
                        "highlight_element": "attention_viz",
                        "sample_text": "The movie was absolutely fantastic! The acting was superb, but the plot was confusing."
                    },
                    {
                        "title": "Interpreting Attention",
                        "content": "Brighter colors indicate words that had more influence on the sentiment prediction. Click on words to see their individual contribution scores.",
                        "action": "info",
                        "highlight_element": None
                    },
                    {
                        "title": "Confidence Scores",
                        "content": "Confidence scores range from 0 to 1. Higher scores (0.8+) indicate high confidence, while lower scores suggest the model is uncertain. Use this to gauge reliability.",
                        "action": "highlight",
                        "highlight_element": "confidence_score"
                    },
                    {
                        "title": "Sample Data Analysis",
                        "content": "Try analyzing samples from different categories to see how the model handles various text types. Compare expected vs. actual results.",
                        "action": "highlight",
                        "highlight_element": "sample_analysis"
                    },
                    {
                        "title": "Use Case Documentation",
                        "content": "Explore the Use Case Documentation to understand different text types and their characteristics. This helps you interpret results more effectively.",
                        "action": "highlight",
                        "highlight_element": "use_case_docs"
                    },
                    {
                        "title": "Performance Benchmarks",
                        "content": "Check the Performance Benchmarks to see how the model performs on different types of text and compare with industry standards.",
                        "action": "highlight",
                        "highlight_element": "performance_benchmarks"
                    },
                    {
                        "title": "Intermediate Complete!",
                        "content": "Great job! You now understand advanced features and can interpret results more effectively. You're ready for the advanced tutorial!",
                        "action": "success",
                        "highlight_element": None
                    }
                ]
            },
            "advanced": {
                "title": "Advanced Tutorial",
                "description": "Master advanced techniques for data scientists and power users",
                "steps": [
                    {
                        "title": "Advanced Techniques",
                        "content": "Welcome to the advanced tutorial! You'll learn about model architecture, performance optimization, and advanced analysis techniques.",
                        "action": "info",
                        "highlight_element": None
                    },
                    {
                        "title": "Model Architecture",
                        "content": "This model uses transformer-based architecture with attention mechanisms. It's trained on diverse text types and optimized for real-time processing.",
                        "action": "info",
                        "highlight_element": None
                    },
                    {
                        "title": "Attention Analysis",
                        "content": "Deep dive into attention patterns. Compare attention between different predictions and understand how context affects word importance.",
                        "action": "highlight",
                        "highlight_element": "attention_comparison"
                    },
                    {
                        "title": "Performance Optimization",
                        "content": "Learn about processing time optimization, caching strategies, and how to achieve sub-2-second response times for production use.",
                        "action": "highlight",
                        "highlight_element": "performance_metrics"
                    },
                    {
                        "title": "Batch Analysis",
                        "content": "For large-scale analysis, use batch processing capabilities. Upload CSV files or process multiple texts efficiently.",
                        "action": "highlight",
                        "highlight_element": "batch_processing"
                    },
                    {
                        "title": "Custom Thresholds",
                        "content": "Adjust confidence thresholds based on your use case. Lower thresholds catch more sentiment but may reduce accuracy.",
                        "action": "highlight",
                        "highlight_element": "custom_thresholds"
                    },
                    {
                        "title": "Export and Integration",
                        "content": "Export results in various formats (CSV, JSON) and learn about API integration for automated workflows.",
                        "action": "highlight",
                        "highlight_element": "export_features"
                    },
                    {
                        "title": "Advanced Complete!",
                        "content": "Excellent! You've mastered advanced features and are ready to use this tool for professional sentiment analysis projects.",
                        "action": "success",
                        "highlight_element": None
                    }
                ]
            }
        }
    
    def render_tutorial_selector(self) -> None:
        """Render the tutorial selection interface."""
        st.subheader("🎓 Interactive Tutorials")
        st.markdown("Choose a tutorial to learn about sentiment analysis and how to use this tool effectively.")
        
        # Tutorial selection
        tutorial_options = {
            "beginner": "Beginner - Learn the basics",
            "intermediate": "Intermediate - Advanced features",
            "advanced": "Advanced - For data scientists"
        }
        
        selected_tutorial = st.selectbox(
            "Select a tutorial:",
            list(tutorial_options.keys()),
            format_func=lambda x: tutorial_options[x],
            key="tutorial_selector"
        )
        
        if selected_tutorial:
            tutorial = self.tutorials[selected_tutorial]
            st.markdown(f"### {tutorial['title']}")
            st.markdown(f"*{tutorial['description']}*")
            
            # Start tutorial button
            if st.button("Start Tutorial", key="start_tutorial"):
                st.session_state.current_tutorial = selected_tutorial
                st.session_state.tutorial_step = 0
                st.rerun()
    
    def render_current_tutorial(self, on_sample_load: Callable[[str], None]) -> None:
        """Render the current tutorial step.
        
        Args:
            on_sample_load: Callback function to load sample text
        """
        if 'current_tutorial' not in st.session_state or 'tutorial_step' not in st.session_state:
            return
        
        tutorial_id = st.session_state.current_tutorial
        current_step = st.session_state.tutorial_step
        
        if tutorial_id not in self.tutorials:
            return
        
        tutorial = self.tutorials[tutorial_id]
        steps = tutorial['steps']
        
        if current_step >= len(steps):
            # Tutorial completed
            self._render_tutorial_completion(tutorial_id)
            return
        
        step = steps[current_step]
        
        # Tutorial progress
        progress = (current_step + 1) / len(steps)
        st.progress(progress)
        st.markdown(f"**Step {current_step + 1} of {len(steps)}**")
        
        # Step content
        st.markdown(f"### {step['title']}")
        st.markdown(step['content'])
        
        # Handle step actions
        if step['action'] == 'info':
            st.info("💡 This is an informational step. Read the content and click 'Next' when ready.")
        elif step['action'] == 'highlight':
            st.warning(f"🎯 **Focus on:** {step['highlight_element']}")
            if step.get('sample_text'):
                st.markdown("**Sample text to try:**")
                st.code(step['sample_text'])
                if st.button("Load Sample Text", key=f"load_sample_{current_step}"):
                    on_sample_load(step['sample_text'])
        elif step['action'] == 'success':
            st.success("🎉 Great job! You've completed this step.")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if current_step > 0:
                if st.button("← Previous", key=f"prev_{current_step}"):
                    st.session_state.tutorial_step -= 1
                    st.rerun()
        
        with col2:
            if st.button("⏸️ Pause Tutorial", key=f"pause_{current_step}"):
                del st.session_state.current_tutorial
                del st.session_state.tutorial_step
                st.rerun()
        
        with col3:
            if current_step < len(steps) - 1:
                if st.button("Next →", key=f"next_{current_step}"):
                    st.session_state.tutorial_step += 1
                    st.rerun()
            else:
                if st.button("Complete Tutorial", key=f"complete_{current_step}"):
                    st.session_state.tutorial_step += 1
                    st.rerun()
    
    def _render_tutorial_completion(self, tutorial_id: str) -> None:
        """Render tutorial completion screen.
        
        Args:
            tutorial_id: ID of the completed tutorial
        """
        tutorial = self.tutorials[tutorial_id]
        
        st.success("🎉 Tutorial Completed!")
        st.markdown(f"### Congratulations!")
        st.markdown(f"You've successfully completed the **{tutorial['title']}**!")
        
        # Completion certificate
        st.markdown("""
        <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; text-align: center; background-color: #f0f8f0;">
            <h2>🏆 Certificate of Completion</h2>
            <p><strong>{tutorial['title']}</strong></p>
            <p>This certifies that you have successfully completed the tutorial and understand the concepts covered.</p>
            <p><em>Date: {st.session_state.get('tutorial_completion_date', 'Today')}</em></p>
        </div>
        """.format(tutorial['title']), unsafe_allow_html=True)
        
        # Next steps
        st.markdown("### What's Next?")
        
        if tutorial_id == "beginner":
            st.markdown("• Try the **Intermediate Tutorial** to learn about advanced features")
            st.markdown("• Practice with different types of text in the Sample Gallery")
            st.markdown("• Explore the Use Case Documentation")
        elif tutorial_id == "intermediate":
            st.markdown("• Try the **Advanced Tutorial** for data scientists")
            st.markdown("• Experiment with attention visualizations")
            st.markdown("• Check the Performance Benchmarks")
        elif tutorial_id == "advanced":
            st.markdown("• You're now ready for professional use!")
            st.markdown("• Explore API integration options")
            st.markdown("• Consider batch processing for large datasets")
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Start Another Tutorial"):
                del st.session_state.current_tutorial
                del st.session_state.tutorial_step
                st.rerun()
        
        with col2:
            if st.button("Return to Main Interface"):
                del st.session_state.current_tutorial
                del st.session_state.tutorial_step
                st.rerun()
    
    def render_quick_tips(self) -> None:
        """Render quick tips for users."""
        st.subheader("💡 Quick Tips")
        
        tips = [
            "**Start with sample data** - Use the Sample Gallery to see how different text types are analyzed",
            "**Check confidence scores** - Higher confidence means more reliable predictions",
            "**Use attention visualization** - See which words influenced the sentiment prediction",
            "**Try different text types** - Test with reviews, social media, formal documents, etc.",
            "**Compare expected vs. actual** - Use the Results Comparison feature for learning",
            "**Explore use cases** - Read the documentation to understand different applications",
            "**Check performance** - Review benchmarks to understand model capabilities"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")
    
    def render_help_section(self) -> None:
        """Render help section with common questions."""
        st.subheader("❓ Help & FAQ")
        
        faq = [
            {
                "question": "What is sentiment analysis?",
                "answer": "Sentiment analysis is the process of determining whether a piece of text expresses positive, negative, or neutral sentiment using AI and natural language processing."
            },
            {
                "question": "How accurate is the model?",
                "answer": "The model achieves 89% overall accuracy across different text types. Performance varies by category - movie reviews (92%), social media (85%), sarcasm (78%)."
            },
            {
                "question": "What types of text can I analyze?",
                "answer": "You can analyze any type of text: social media posts, reviews, news articles, formal documents, technical content, and more. The model is trained on diverse text types."
            },
            {
                "question": "How do I interpret confidence scores?",
                "answer": "Confidence scores range from 0 to 1. Higher scores (0.8+) indicate high confidence, while lower scores suggest uncertainty. Use this to gauge prediction reliability."
            },
            {
                "question": "What is attention visualization?",
                "answer": "Attention visualization shows which words the model focused on when making predictions. Brighter colors indicate more influential words. Click words to see contribution scores."
            },
            {
                "question": "Can I analyze multiple texts at once?",
                "answer": "Yes! Use the batch processing feature to analyze multiple texts efficiently. Upload CSV files or process multiple texts in sequence."
            },
            {
                "question": "How fast is the analysis?",
                "answer": "Average processing time is 1.45 seconds per text, making it suitable for real-time applications and interactive use."
            }
        ]
        
        for i, item in enumerate(faq):
            with st.expander(f"Q: {item['question']}"):
                st.markdown(f"**A:** {item['answer']}")
    
    def render_tutorial_progress(self) -> None:
        """Render tutorial progress tracking."""
        if 'tutorial_progress' not in st.session_state:
            st.session_state.tutorial_progress = {
                'beginner': False,
                'intermediate': False,
                'advanced': False
            }
        
        st.subheader("📊 Tutorial Progress")
        
        progress = st.session_state.tutorial_progress
        total_tutorials = len(self.tutorials)
        completed_tutorials = sum(progress.values())
        
        # Overall progress
        overall_progress = completed_tutorials / total_tutorials
        st.progress(overall_progress)
        st.markdown(f"**Overall Progress:** {completed_tutorials}/{total_tutorials} tutorials completed")
        
        # Individual tutorial progress
        for tutorial_id, tutorial in self.tutorials.items():
            status = "✅ Completed" if progress.get(tutorial_id, False) else "⏳ Not Started"
            st.markdown(f"• **{tutorial['title']}:** {status}")
        
        # Achievement badges
        if completed_tutorials >= 1:
            st.markdown("🏆 **Achievement Unlocked:** Tutorial Explorer")
        if completed_tutorials >= 2:
            st.markdown("🎓 **Achievement Unlocked:** Knowledge Seeker")
        if completed_tutorials >= 3:
            st.markdown("👑 **Achievement Unlocked:** Master Learner")


def render_interactive_tutorial(on_sample_load: Callable[[str], None] = None) -> None:
    """Convenience function to render interactive tutorial.
    
    Args:
        on_sample_load: Callback function to load sample text
    """
    tutorial = InteractiveTutorial()
    
    # Check if tutorial is in progress
    if 'current_tutorial' in st.session_state:
        tutorial.render_current_tutorial(on_sample_load or (lambda x: None))
    else:
        tutorial.render_tutorial_selector()


def render_quick_tips() -> None:
    """Convenience function to render quick tips."""
    tutorial = InteractiveTutorial()
    tutorial.render_quick_tips()


def render_help_section() -> None:
    """Convenience function to render help section."""
    tutorial = InteractiveTutorial()
    tutorial.render_help_section()


def render_tutorial_progress() -> None:
    """Convenience function to render tutorial progress."""
    tutorial = InteractiveTutorial()
    tutorial.render_tutorial_progress()


if __name__ == "__main__":
    # Test the component
    render_interactive_tutorial()
