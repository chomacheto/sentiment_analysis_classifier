"""
Sidebar Component for Sentiment Analysis Web Interface

This module provides a sidebar component with navigation, model information,
and user preferences for the Streamlit web interface.
"""

import streamlit as st
from typing import Dict, Any

class SidebarComponent:
    """
    Sidebar component with navigation and model information.
    
    Features:
    - Clear navigation structure
    - Model information display
    - User preferences and settings
    - Professional styling
    """
    
    def __init__(self):
        """Initialize the sidebar component."""
        pass
    
    def render(self) -> None:
        """Render the sidebar component."""
        with st.sidebar:
            # Header
            st.markdown(
                """
                <div style="text-align: center; padding: 1rem 0;">
                    <h2 style="margin: 0; color: #667eea;">🧠</h2>
                    <h3 style="margin: 0; color: #333;">Sentiment AI</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.divider()
            
            # Navigation
            self._render_navigation()
            
            st.divider()
            
            # Model Information
            self._render_model_info()
            
            st.divider()
            
            # User Preferences
            self._render_user_preferences()
            
            st.divider()
            
            # Footer
            self._render_footer()
    
    def _render_navigation(self) -> None:
        """Render navigation section."""
        st.markdown("**🧭 Navigation**")
        
        # Current page indicator
        st.info("📍 **Current:** Web Interface")
        
        # Navigation links (for future expansion)
        st.markdown("**📋 Available Pages:**")
        st.markdown("- 🏠 **Web Interface** (Current)")
        st.markdown("- 📊 **API Documentation** (Coming Soon)")
        st.markdown("- 📈 **Analytics Dashboard** (Coming Soon)")
        st.markdown("- ⚙️ **Settings** (Coming Soon)")
    
    def _render_model_info(self) -> None:
        """Render model information section."""
        st.markdown("**🤖 Model Information**")
        
        # Get model info from session state if available
        if 'sentiment_pipeline' in st.session_state and st.session_state.sentiment_pipeline:
            try:
                model_info = st.session_state.sentiment_pipeline.get_model_info()
                
                if model_info.get("status") == "initialized":
                    st.success("✅ Model Loaded")
                    
                    # Model details
                    with st.expander("📋 Model Details"):
                        st.write(f"**Model:** {model_info.get('model_name', 'Unknown')}")
                        st.write(f"**Type:** {model_info.get('model_type', 'Unknown')}")
                        st.write(f"**Framework:** {model_info.get('framework', 'Unknown')}")
                        st.write(f"**Device:** {model_info.get('device', 'Unknown')}")
                        
                        # Performance indicator
                        if model_info.get("device") == "CUDA":
                            st.success("🚀 GPU Acceleration Active")
                        else:
                            st.info("💻 CPU Processing")
                else:
                    st.warning("⚠️ Model Not Initialized")
                    
            except Exception as e:
                st.error(f"❌ Error loading model info: {str(e)}")
        else:
            st.info("⏳ Model initializing...")
    
    def _render_user_preferences(self) -> None:
        """Render user preferences section."""
        st.markdown("**⚙️ User Preferences**")
        
        # Theme selection
        theme = st.selectbox(
            "🎨 Theme",
            ["Light", "Dark", "Auto"],
            index=0,
            help="Select your preferred theme"
        )
        
        # Display mode
        display_mode = st.selectbox(
            "📱 Display Mode",
            ["Wide", "Centered", "Compact"],
            index=0,
            help="Select your preferred display layout"
        )
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox(
            "🔄 Auto-refresh",
            value=False,
            help="Automatically refresh results"
        )
        
        # Attention analysis toggle
        attention_analysis = st.checkbox(
            "🧠 Enable Attention Analysis",
            value=False,
            help="Enable word-level attention visualization (slower but more detailed)"
        )
        
        # Store preferences in session state
        st.session_state.user_preferences = {
            "theme": theme,
            "display_mode": display_mode,
            "auto_refresh": auto_refresh,
            "attention_analysis": attention_analysis
        }
        
        # Apply theme if changed
        if theme == "Dark":
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
    
    def _render_footer(self) -> None:
        """Render footer section."""
        st.markdown("**📚 Resources**")
        
        # Help and documentation
        if st.button("📖 Help & Docs", use_container_width=True):
            st.info("Documentation coming soon!")
        
        # About section
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Sentiment Analysis Classifier**
            
            A professional web interface for AI-powered sentiment analysis.
            
            **Version:** 2.1.0
            **Framework:** Streamlit + Transformers
            **Model:** DistilBERT (English)
            
            Built with ❤️ using modern AI technologies.
            """)
        
        # Contact information
        st.markdown("**📧 Support**")
        st.markdown("For support and feedback, please contact the development team.")
        
        # Version info
        st.caption("v2.1.0 | Streamlit Web Interface")
