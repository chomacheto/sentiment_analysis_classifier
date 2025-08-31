"""
Technical Explanation Component

This module provides educational content about transformer attention mechanisms
and best practices for interpreting attention visualizations in sentiment analysis.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
import plotly.express as px

class TechnicalExplanation:
    """
    Component for providing technical explanations about attention mechanisms.
    
    Features:
    - Educational content about transformer attention mechanisms
    - Interactive explanations with visual examples
    - Best practices for interpreting attention visualizations
    - Step-by-step guide to understanding attention weights
    """
    
    def __init__(self):
        """Initialize the technical explanation component."""
        # Educational content sections
        self.sections = {
            "attention_basics": {
                "title": "🧠 Attention Mechanism Basics",
                "content": self._get_attention_basics_content()
            },
            "transformer_attention": {
                "title": "⚡ Transformer Attention",
                "content": self._get_transformer_attention_content()
            },
            "interpretation_guide": {
                "title": "📊 How to Interpret Attention",
                "content": self._get_interpretation_guide_content()
            },
            "best_practices": {
                "title": "✅ Best Practices",
                "content": self._get_best_practices_content()
            },
            "visual_examples": {
                "title": "🎨 Visual Examples",
                "content": self._get_visual_examples_content()
            }
        }
    
    def render(self, result: Optional[Dict[str, Any]] = None) -> None:
        """
        Render the technical explanation component.
        
        Args:
            result: Optional sentiment analysis result for contextual examples
        """
        st.subheader("📚 Technical Explanation: Attention Mechanisms")
        
        # Create tabs for different explanation sections
        tab_names = list(self.sections.keys())
        tabs = st.tabs([self.sections[tab]["title"] for tab in tab_names])
        
        for i, tab in enumerate(tabs):
            with tab:
                self._render_section(tab_names[i], result)
    
    def _render_section(self, section_name: str, result: Optional[Dict[str, Any]] = None) -> None:
        """Render a specific explanation section."""
        # Handle invalid section names gracefully
        if section_name not in self.sections:
            st.warning(f"Section '{section_name}' not found. Available sections: {list(self.sections.keys())}")
            return
        
        section = self.sections[section_name]
        
        if section_name == "attention_basics":
            self._render_attention_basics()
        elif section_name == "transformer_attention":
            self._render_transformer_attention()
        elif section_name == "interpretation_guide":
            self._render_interpretation_guide(result)
        elif section_name == "best_practices":
            self._render_best_practices()
        elif section_name == "visual_examples":
            self._render_visual_examples(result)
    
    def _render_attention_basics(self) -> None:
        """Render attention mechanism basics section."""
        st.markdown("""
        ## What is Attention?
        
        **Attention** is a mechanism that allows neural networks to focus on specific parts of input data when making predictions. 
        Think of it like how humans pay attention to different words when reading a sentence.
        
        ### Key Concepts:
        
        **🔍 Focus**: Attention helps the model focus on the most relevant parts of the input
        **⚖️ Weighting**: Each word gets an "attention weight" indicating its importance
        **🔄 Context**: The model considers relationships between all words in the text
        """)
        
        # Interactive attention example
        st.markdown("### Interactive Example")
        
        example_sentence = st.text_input(
            "Enter a sentence to see attention in action:",
            value="The movie was absolutely fantastic and amazing!",
            help="Try different sentences to see how attention works"
        )
        
        if example_sentence:
            self._show_attention_example(example_sentence)
    
    def _render_transformer_attention(self) -> None:
        """Render transformer attention section."""
        st.markdown("""
        ## Transformer Attention Mechanism
        
        Transformers use a sophisticated attention mechanism called **Multi-Head Self-Attention**.
        
        ### How it Works:
        
        1. **Tokenization**: Text is split into individual tokens (words/subwords)
        2. **Embedding**: Each token is converted to a numerical representation
        3. **Query, Key, Value**: For each token, three vectors are computed
        4. **Attention Calculation**: Attention weights are computed using these vectors
        5. **Weighted Sum**: Final representation combines all tokens with their weights
        """)
        
        # Visual representation
        st.markdown("### Visual Representation")
        
        # Create a simple attention matrix visualization
        tokens = ["The", "movie", "was", "great"]
        attention_matrix = [
            [0.4, 0.3, 0.2, 0.1],
            [0.2, 0.5, 0.2, 0.1],
            [0.1, 0.2, 0.6, 0.1],
            [0.1, 0.1, 0.2, 0.6]
        ]
        
        fig = go.Figure(data=go.Heatmap(
            z=attention_matrix,
            x=tokens,
            y=tokens,
            colorscale='Blues',
            text=[[f"{val:.2f}" for val in row] for row in attention_matrix],
            texttemplate="%{text}",
            textfont={"size": 12},
            showscale=True
        ))
        
        fig.update_layout(
            title="Attention Matrix Example",
            xaxis_title="Key Tokens",
            yaxis_title="Query Tokens",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Interpretation**: Each cell shows how much attention the row token pays to the column token.
        Higher values (darker colors) indicate stronger attention.
        """)
    
    def _render_interpretation_guide(self, result: Optional[Dict[str, Any]] = None) -> None:
        """Render interpretation guide section."""
        st.markdown("""
        ## How to Interpret Attention Visualizations
        
        Understanding attention weights helps you see which words influenced the model's decision.
        """)
        
        # Interpretation guidelines
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🟢 Positive Attention
            - **High attention + positive sentiment** = Strong positive influence
            - Words like "great", "amazing", "excellent"
            - These words strongly support positive classification
            
            ### 🔴 Negative Attention
            - **High attention + negative sentiment** = Strong negative influence
            - Words like "terrible", "awful", "horrible"
            - These words strongly support negative classification
            """)
        
        with col2:
            st.markdown("""
            ### ⚪ Neutral Attention
            - **Low attention** = Minimal influence on sentiment
            - Common words like "the", "is", "was"
            - These words don't significantly affect the prediction
            
            ### 🎯 Context Words
            - **Medium attention** = Contextual influence
            - Words that modify sentiment like "very", "not", "really"
            - These words amplify or negate other words' sentiment
            """)
        
        # Interactive interpretation with actual data
        if result and "attention_weights" in result:
            st.markdown("### 📊 Your Analysis Interpretation")
            
            attention_weights = result.get("attention_weights", [])
            if attention_weights:
                # Show top attention words
                top_attention = sorted(attention_weights, key=lambda x: x["attention_score"], reverse=True)[:5]
                
                st.markdown("**Top 5 Most Attended Words:**")
                for i, word in enumerate(top_attention, 1):
                    attention_score = word["attention_score"]
                    contribution_score = word["contribution_score"]
                    
                    if contribution_score > 0:
                        emoji = "🟢"
                        influence = "positive"
                    elif contribution_score < 0:
                        emoji = "🔴"
                        influence = "negative"
                    else:
                        emoji = "⚪"
                        influence = "neutral"
                    
                    st.markdown(f"{i}. {emoji} **{word['token']}** - Attention: {attention_score:.3f}, Influence: {influence}")
    
    def _render_best_practices(self) -> None:
        """Render best practices section."""
        st.markdown("""
        ## Best Practices for Interpreting Attention
        
        ### ✅ Do's:
        
        - **Look for patterns**: Focus on words with high attention scores
        - **Consider context**: Understand how words relate to each other
        - **Check confidence**: High attention doesn't always mean high confidence
        - **Compare multiple analyses**: Use comparison mode for better insights
        - **Validate with domain knowledge**: Trust your understanding of the text
        
        ### ❌ Don'ts:
        
        - **Don't ignore low attention words**: They might still be important
        - **Don't overinterpret**: Attention is one piece of the puzzle
        - **Don't assume causality**: High attention doesn't mean the word caused the prediction
        - **Don't ignore model limitations**: Attention can be misleading in some cases
        """)
        
        # Common pitfalls
        st.markdown("### ⚠️ Common Pitfalls")
        
        with st.expander("Click to see common interpretation mistakes"):
            st.markdown("""
            1. **Confusing attention with importance**: High attention doesn't always mean high importance
            2. **Ignoring word relationships**: Words work together, not in isolation
            3. **Overlooking context**: The same word can have different meanings in different contexts
            4. **Focusing only on extremes**: Medium attention words can also be significant
            5. **Not considering model architecture**: Different models may attend to different patterns
            """)
    
    def _render_visual_examples(self, result: Optional[Dict[str, Any]] = None) -> None:
        """Render visual examples section."""
        st.markdown("""
        ## Visual Examples and Patterns
        
        Understanding common attention patterns helps you interpret your own analyses.
        """)
        
        # Example patterns
        examples = [
            {
                "text": "The movie was absolutely fantastic!",
                "pattern": "Positive sentiment words get high attention",
                "explanation": "Words like 'fantastic' and 'absolutely' receive high attention scores because they strongly indicate positive sentiment."
            },
            {
                "text": "This film is not good at all.",
                "pattern": "Negation words modify attention",
                "explanation": "The word 'not' receives attention because it negates the positive word 'good', changing the overall sentiment."
            },
            {
                "text": "The acting was brilliant but the plot was terrible.",
                "pattern": "Contrasting sentiments create complex attention",
                "explanation": "Both 'brilliant' and 'terrible' receive attention, creating a mixed sentiment that requires careful interpretation."
            }
        ]
        
        for i, example in enumerate(examples, 1):
            with st.expander(f"Example {i}: {example['text']}"):
                st.markdown(f"**Pattern**: {example['pattern']}")
                st.markdown(f"**Explanation**: {example['explanation']}")
                
                # Create a simple visualization for each example
                words = example["text"].split()
                # Simulate attention scores (in real implementation, these would come from the model)
                attention_scores = [0.1, 0.2, 0.1, 0.3, 0.2, 0.1] if i == 1 else [0.1, 0.2, 0.3, 0.2, 0.1, 0.1] if i == 2 else [0.1, 0.2, 0.3, 0.1, 0.2, 0.3, 0.1]
                
                # Pad or truncate to match word count
                attention_scores = attention_scores[:len(words)]
                while len(attention_scores) < len(words):
                    attention_scores.append(0.1)
                
                fig = go.Figure(data=go.Bar(
                    x=words,
                    y=attention_scores,
                    marker_color='lightblue'
                ))
                
                fig.update_layout(
                    title=f"Simulated Attention Scores for: '{example['text']}'",
                    xaxis_title="Words",
                    yaxis_title="Attention Score",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Interactive visualization with user's data
        if result and "attention_weights" in result:
            st.markdown("### 📈 Your Data Visualization")
            
            attention_weights = result.get("attention_weights", [])
            if attention_weights:
                tokens = [item["token"] for item in attention_weights]
                scores = [item["attention_score"] for item in attention_weights]
                contributions = [item["contribution_score"] for item in attention_weights]
                
                # Color based on contribution
                colors = []
                for contrib in contributions:
                    if contrib > 0:
                        colors.append('green')
                    elif contrib < 0:
                        colors.append('red')
                    else:
                        colors.append('gray')
                
                fig = go.Figure(data=go.Bar(
                    x=tokens,
                    y=scores,
                    marker_color=colors,
                    text=[f"{score:.3f}" for score in scores],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    title="Your Attention Analysis",
                    xaxis_title="Words",
                    yaxis_title="Attention Score",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def _show_attention_example(self, sentence: str) -> None:
        """Show an interactive attention example for the given sentence."""
        words = sentence.split()
        
        st.markdown("**Attention Weights (Simulated):**")
        
        # Create a simple attention visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Word-level Attention:**")
            for i, word in enumerate(words):
                # Simulate attention based on word characteristics
                if word.lower() in ["great", "amazing", "fantastic", "excellent", "wonderful"]:
                    attention = 0.9
                    color = "🟢"
                elif word.lower() in ["terrible", "awful", "horrible", "bad", "worst"]:
                    attention = 0.9
                    color = "🔴"
                elif word.lower() in ["the", "is", "was", "a", "an", "and", "or"]:
                    attention = 0.1
                    color = "⚪"
                else:
                    attention = 0.5
                    color = "🟡"
                
                st.markdown(f"{color} **{word}**: {attention:.2f}")
        
        with col2:
            st.markdown("**Visual Representation:**")
            
            # Create a simple bar chart
            attention_scores = []
            for word in words:
                if word.lower() in ["great", "amazing", "fantastic", "excellent", "wonderful"]:
                    attention_scores.append(0.9)
                elif word.lower() in ["terrible", "awful", "horrible", "bad", "worst"]:
                    attention_scores.append(0.9)
                elif word.lower() in ["the", "is", "was", "a", "an", "and", "or"]:
                    attention_scores.append(0.1)
                else:
                    attention_scores.append(0.5)
            
            fig = go.Figure(data=go.Bar(
                x=words,
                y=attention_scores,
                marker_color='lightblue'
            ))
            
            fig.update_layout(
                title="Attention Scores",
                xaxis_title="Words",
                yaxis_title="Attention Score",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _get_attention_basics_content(self) -> str:
        """Get attention basics content."""
        return "Basic attention mechanism concepts and principles."
    
    def _get_transformer_attention_content(self) -> str:
        """Get transformer attention content."""
        return "Detailed explanation of transformer attention mechanisms."
    
    def _get_interpretation_guide_content(self) -> str:
        """Get interpretation guide content."""
        return "Step-by-step guide to interpreting attention visualizations."
    
    def _get_best_practices_content(self) -> str:
        """Get best practices content."""
        return "Best practices and common pitfalls in attention interpretation."
    
    def _get_visual_examples_content(self) -> str:
        """Get visual examples content."""
        return "Visual examples and patterns in attention analysis."
