"""
Visualization Export Component

This module provides functionality for exporting attention visualizations
and analysis results in various formats including PNG, PDF, and CSV.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional
import base64
import io
from datetime import datetime
import pandas as pd

class VisualizationExport:
    """
    Component for exporting attention visualizations and analysis results.
    
    Features:
    - PNG/PDF export for attention heatmaps
    - CSV export for attention data
    - Screenshot functionality for visualizations
    - Integration with existing export capabilities
    """
    
    def __init__(self):
        """Initialize the visualization export component."""
        pass
    
    def render(self, result: Optional[Dict[str, Any]] = None) -> None:
        """
        Render the visualization export component.
        
        Args:
            result: Optional sentiment analysis result with attention data
        """
        st.subheader("💾 Export Visualizations")
        
        if not result or "attention_weights" not in result:
            st.info("Enable attention analysis to export visualizations")
            return
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Export Attention Data**")
            if st.button("📄 Export to CSV", help="Export attention weights and contributions to CSV"):
                self._export_attention_csv(result)
            
            if st.button("📊 Export to Excel", help="Export comprehensive analysis to Excel"):
                self._export_attention_excel(result)
        
        with col2:
            st.markdown("**🖼️ Export Visualizations**")
            if st.button("🖼️ Export Heatmap PNG", help="Export attention heatmap as PNG"):
                self._export_heatmap_png(result)
            
            if st.button("📄 Export Heatmap PDF", help="Export attention heatmap as PDF"):
                self._export_heatmap_pdf(result)
        
        # Advanced export options
        with st.expander("🔧 Advanced Export Options"):
            self._render_advanced_export_options(result)
    
    def _export_attention_csv(self, result: Dict[str, Any]) -> None:
        """Export attention data to CSV format."""
        try:
            attention_weights = result.get("attention_weights", [])
            
            if not attention_weights:
                st.warning("No attention data to export")
                return
            
            # Create DataFrame
            df = pd.DataFrame(attention_weights)
            
            # Add metadata
            df['sentiment_label'] = result.get("sentiment_label", "unknown")
            df['confidence_score'] = result.get("confidence_score", 0.0)
            df['timestamp'] = datetime.now().isoformat()
            
            # Generate CSV
            csv = df.to_csv(index=False)
            
            # Create download button
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"attention_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            st.success("CSV export ready!")
            
        except Exception as e:
            st.error(f"Failed to export CSV: {str(e)}")
    
    def _export_attention_excel(self, result: Dict[str, Any]) -> None:
        """Export comprehensive analysis to Excel format."""
        try:
            # Create multiple sheets
            with pd.ExcelWriter('attention_analysis.xlsx', engine='openpyxl') as writer:
                # Attention weights sheet
                attention_weights = result.get("attention_weights", [])
                if attention_weights:
                    df_weights = pd.DataFrame(attention_weights)
                    df_weights.to_excel(writer, sheet_name='Attention_Weights', index=False)
                
                # Top contributing words sheet
                top_words = result.get("top_contributing_words", [])
                if top_words:
                    df_top = pd.DataFrame(top_words)
                    df_top.to_excel(writer, sheet_name='Top_Contributors', index=False)
                
                # Summary sheet
                summary_data = {
                    'Metric': ['Sentiment', 'Confidence', 'Words Analyzed', 'Export Date'],
                    'Value': [
                        result.get("sentiment_label", "unknown"),
                        result.get("confidence_score", 0.0),
                        len(attention_weights),
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ]
                }
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Read the file and create download button
            with open('attention_analysis.xlsx', 'rb') as f:
                excel_data = f.read()
            
            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name=f"attention_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.success("Excel export ready!")
            
        except Exception as e:
            st.error(f"Failed to export Excel: {str(e)}")
    
    def _export_heatmap_png(self, result: Dict[str, Any]) -> None:
        """Export attention heatmap as PNG."""
        try:
            attention_weights = result.get("attention_weights", [])
            
            if not attention_weights:
                st.warning("No attention data to visualize")
                return
            
            # Create heatmap
            tokens = [item["token"] for item in attention_weights]
            attention_scores = [item["attention_score"] for item in attention_weights]
            contribution_scores = [item["contribution_score"] for item in attention_weights]
            
            # Color mapping
            colors = []
            for score in contribution_scores:
                if score > 0:
                    colors.append('green')
                elif score < 0:
                    colors.append('red')
                else:
                    colors.append('gray')
            
            fig = go.Figure(data=go.Bar(
                x=tokens,
                y=attention_scores,
                marker_color=colors,
                text=[f"{score:.3f}" for score in attention_scores],
                textposition='auto'
            ))
            
            fig.update_layout(
                title=f"Attention Heatmap - {result.get('sentiment_label', 'unknown').capitalize()}",
                xaxis_title="Words",
                yaxis_title="Attention Score",
                height=400
            )
            
            # Convert to PNG
            img_bytes = fig.to_image(format="png")
            
            st.download_button(
                label="📥 Download PNG",
                data=img_bytes,
                file_name=f"attention_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
            
            st.success("PNG export ready!")
            
        except Exception as e:
            st.error(f"Failed to export PNG: {str(e)}")
    
    def _export_heatmap_pdf(self, result: Dict[str, Any]) -> None:
        """Export attention heatmap as PDF."""
        try:
            attention_weights = result.get("attention_weights", [])
            
            if not attention_weights:
                st.warning("No attention data to visualize")
                return
            
            # Create heatmap
            tokens = [item["token"] for item in attention_weights]
            attention_scores = [item["attention_score"] for item in attention_weights]
            contribution_scores = [item["contribution_score"] for item in attention_weights]
            
            # Color mapping
            colors = []
            for score in contribution_scores:
                if score > 0:
                    colors.append('green')
                elif score < 0:
                    colors.append('red')
                else:
                    colors.append('gray')
            
            fig = go.Figure(data=go.Bar(
                x=tokens,
                y=attention_scores,
                marker_color=colors,
                text=[f"{score:.3f}" for score in attention_scores],
                textposition='auto'
            ))
            
            fig.update_layout(
                title=f"Attention Heatmap - {result.get('sentiment_label', 'unknown').capitalize()}",
                xaxis_title="Words",
                yaxis_title="Attention Score",
                height=400
            )
            
            # Convert to PDF
            pdf_bytes = fig.to_image(format="pdf")
            
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"attention_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
            
            st.success("PDF export ready!")
            
        except Exception as e:
            st.error(f"Failed to export PDF: {str(e)}")
    
    def _render_advanced_export_options(self, result: Dict[str, Any]) -> None:
        """Render advanced export options."""
        st.markdown("**Advanced Export Settings:**")
        
        # Export format selection
        export_format = st.selectbox(
            "Export Format:",
            ["PNG", "PDF", "SVG", "HTML"],
            help="Choose the format for visualization exports"
        )
        
        # Image quality settings
        if export_format in ["PNG", "PDF"]:
            quality = st.slider(
                "Image Quality:",
                min_value=1,
                max_value=10,
                value=8,
                help="Higher quality = larger file size"
            )
        
        # Include metadata
        include_metadata = st.checkbox(
            "Include Analysis Metadata",
            value=True,
            help="Include sentiment, confidence, and timestamp in exports"
        )
        
        # Custom filename
        custom_filename = st.text_input(
            "Custom Filename:",
            value=f"attention_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            help="Custom filename for exports (without extension)"
        )
        
        # Export button
        if st.button("🚀 Export with Custom Settings"):
            self._export_with_custom_settings(
                result, export_format, include_metadata, custom_filename
            )
    
    def _export_with_custom_settings(
        self, 
        result: Dict[str, Any], 
        format_type: str, 
        include_metadata: bool, 
        filename: str
    ) -> None:
        """Export with custom settings."""
        try:
            attention_weights = result.get("attention_weights", [])
            
            if not attention_weights:
                st.warning("No attention data to export")
                return
            
            # Create visualization
            tokens = [item["token"] for item in attention_weights]
            attention_scores = [item["attention_score"] for item in attention_weights]
            contribution_scores = [item["contribution_score"] for item in attention_weights]
            
            # Color mapping
            colors = []
            for score in contribution_scores:
                if score > 0:
                    colors.append('green')
                elif score < 0:
                    colors.append('red')
                else:
                    colors.append('gray')
            
            fig = go.Figure(data=go.Bar(
                x=tokens,
                y=attention_scores,
                marker_color=colors,
                text=[f"{score:.3f}" for score in attention_scores],
                textposition='auto'
            ))
            
            title = f"Attention Heatmap - {result.get('sentiment_label', 'unknown').capitalize()}"
            if include_metadata:
                title += f" (Confidence: {result.get('confidence_score', 0.0):.3f})"
            
            fig.update_layout(
                title=title,
                xaxis_title="Words",
                yaxis_title="Attention Score",
                height=400
            )
            
            # Export based on format
            if format_type == "PNG":
                img_bytes = fig.to_image(format="png")
                mime_type = "image/png"
                extension = "png"
            elif format_type == "PDF":
                img_bytes = fig.to_image(format="pdf")
                mime_type = "application/pdf"
                extension = "pdf"
            elif format_type == "SVG":
                img_bytes = fig.to_image(format="svg")
                mime_type = "image/svg+xml"
                extension = "svg"
            elif format_type == "HTML":
                img_bytes = fig.to_html()
                mime_type = "text/html"
                extension = "html"
            else:
                st.error(f"Unsupported format: {format_type}")
                return
            
            st.download_button(
                label=f"📥 Download {format_type.upper()}",
                data=img_bytes,
                file_name=f"{filename}.{extension}",
                mime=mime_type
            )
            
            st.success(f"{format_type.upper()} export ready!")
            
        except Exception as e:
            st.error(f"Failed to export {format_type}: {str(e)}")
