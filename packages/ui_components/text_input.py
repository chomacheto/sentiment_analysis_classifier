"""
Text Input Component for Sentiment Analysis

This module provides a reusable text input component with character limit validation,
professional styling, and real-time feedback.
"""

import streamlit as st
from typing import Optional

class TextInputComponent:
    """
    Reusable text input component with validation and professional styling.
    
    Features:
    - Character limit validation (1000 chars for web interface)
    - Real-time character count display
    - Professional styling and responsive design
    - Input validation feedback
    """
    
    def __init__(self, max_chars: int = 1000, placeholder: str = "Enter your text here..."):
        """
        Initialize the text input component.
        
        Args:
            max_chars: Maximum number of characters allowed
            placeholder: Placeholder text for the input area
        """
        self.max_chars = max_chars
        self.placeholder = placeholder
    
    def render(self) -> str:
        """
        Render the text input component.
        
        Returns:
            The user input text
        """
        # Create a container for the input area
        input_container = st.container()
        
        with input_container:
            # Text area with character limit
            user_input = st.text_area(
                label="",
                placeholder=self.placeholder,
                height=150,
                max_chars=self.max_chars,
                key="sentiment_text_input",
                value=st.session_state.get('current_input', ''),
                help=f"Enter text to analyze (maximum {self.max_chars} characters)"
            )
            
            # Character count display
            if user_input:
                char_count = len(user_input)
                remaining_chars = self.max_chars - char_count
                
                # Color coding for character count
                if remaining_chars <= 50:
                    color = "red"
                elif remaining_chars <= 100:
                    color = "orange"
                else:
                    color = "green"
                
                # Display character count with color coding
                st.markdown(
                    f"<div style='text-align: right; color: {color}; font-size: 0.9rem;'>"
                    f"{char_count}/{self.max_chars} characters</div>",
                    unsafe_allow_html=True
                )
                
                # Warning for approaching limit
                if remaining_chars <= 50:
                    st.warning(f"⚠️ Only {remaining_chars} characters remaining!")
                
                # Error for exceeding limit
                if char_count > self.max_chars:
                    st.error(f"❌ Text exceeds {self.max_chars} character limit!")
                    return ""
            else:
                # Show character limit info when no input
                st.markdown(
                    f"<div style='text-align: right; color: #666; font-size: 0.9rem;'>"
                    f"0/{self.max_chars} characters</div>",
                    unsafe_allow_html=True
                )
        
        return user_input or ""
    
    def validate_input(self, text: str) -> tuple[bool, Optional[str]]:
        """
        Validate the input text.
        
        Args:
            text: Text to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text or not text.strip():
            return False, "Text cannot be empty"
        
        if len(text) > self.max_chars:
            return False, f"Text exceeds {self.max_chars} character limit"
        
        return True, None
