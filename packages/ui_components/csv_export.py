"""
CSV Export Component

This module provides CSV export functionality for prediction results including
timestamp, text input, sentiment, confidence, and processing time with
export format options and customization.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import json

class CSVExport:
    """
    Component for exporting prediction results to various formats.
    
    Features:
    - CSV export for prediction results
    - Include timestamp, text input, sentiment, confidence, and processing time
    - Export button with file download handling
    - Export format options and customization
    - Multiple export formats (CSV, JSON, Excel)
    """
    
    def __init__(self):
        """Initialize the CSV export component."""
        self.export_formats = {
            'csv': {
                'name': 'CSV',
                'extension': '.csv',
                'mime_type': 'text/csv',
                'description': 'Comma-separated values format'
            },
            'json': {
                'name': 'JSON',
                'extension': '.json',
                'mime_type': 'application/json',
                'description': 'JavaScript Object Notation format'
            },
            'excel': {
                'name': 'Excel',
                'extension': '.xlsx',
                'mime_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'description': 'Microsoft Excel format'
            }
        }
    
    def render(self, prediction_history: List[Dict[str, Any]] = None, single_result: Dict[str, Any] = None) -> None:
        """
        Render the export component.
        
        Args:
            prediction_history: List of prediction history entries for bulk export
            single_result: Single prediction result for individual export
        """
        if not prediction_history and not single_result:
            st.info("📤 No data available for export. Complete a sentiment analysis first.")
            return
        
        st.markdown("## 💾 Export Results")
        
        # Export options
        self._render_export_options(prediction_history, single_result)
        
        # Export controls
        self._render_export_controls(prediction_history, single_result)
    
    def _render_export_options(self, prediction_history: List[Dict[str, Any]], single_result: Dict[str, Any]) -> None:
        """Render export format and customization options."""
        st.markdown("**🔧 Export Options**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export format selection
            export_format = st.selectbox(
                "Export Format",
                options=list(self.export_formats.keys()),
                format_func=lambda x: self.export_formats[x]['name'],
                help="Choose the file format for export"
            )
            
            # Export scope
            if prediction_history and single_result:
                export_scope = st.radio(
                    "Export Scope",
                    options=['single', 'bulk'],
                    format_func=lambda x: 'Single Result' if x == 'single' else 'All History',
                    help="Export single result or entire prediction history"
                )
            elif prediction_history:
                export_scope = 'bulk'
            else:
                export_scope = 'single'
        
        with col2:
            # Customization options
            include_metadata = st.checkbox(
                "Include Metadata",
                value=True,
                help="Include additional metadata like text length, word count, etc."
            )
            
            include_model_confidence = st.checkbox(
                "Include Model Confidence",
                value=True,
                help="Include detailed model confidence scores for all sentiment classes"
            )
            
            # Timestamp format
            timestamp_format = st.selectbox(
                "Timestamp Format",
                options=['iso', 'readable', 'unix'],
                format_func=lambda x: {
                    'iso': 'ISO 8601 (2024-01-15T10:30:00)',
                    'readable': 'Human Readable (Jan 15, 2024 10:30 AM)',
                    'unix': 'Unix Timestamp (1705312200)'
                }[x],
                help="Choose timestamp format for export"
            )
        
        # Store options in session state
        st.session_state.export_options = {
            'format': export_format,
            'scope': export_scope,
            'include_metadata': include_metadata,
            'include_model_confidence': include_model_confidence,
            'timestamp_format': timestamp_format
        }
    
    def _render_export_controls(self, prediction_history: List[Dict[str, Any]], single_result: Dict[str, Any]) -> None:
        """Render export controls and buttons."""
        if 'export_options' not in st.session_state:
            return
        
        options = st.session_state.export_options
        
        st.markdown("**📤 Export Controls**")
        
        # Show export preview
        self._render_export_preview(prediction_history, single_result, options)
        
        # Export buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if options['scope'] == 'single' and single_result:
                if st.button(
                    f"📥 Export Single Result ({self.export_formats[options['format']]['name']})",
                    type="primary",
                    use_container_width=True,
                    help=f"Export the current prediction result as {self.export_formats[options['format']]['name']}"
                ):
                    self._export_single_result(single_result, options)
            
            elif options['scope'] == 'bulk' and prediction_history:
                if st.button(
                    f"📥 Export All History ({self.export_formats[options['format']]['name']})",
                    type="primary",
                    use_container_width=True,
                    help=f"Export all prediction history as {self.export_formats[options['format']]['name']}"
                ):
                    self._export_bulk_history(prediction_history, options)
        
        with col2:
            # Clear export options
            if st.button(
                "🗑️ Reset Options",
                use_container_width=True,
                help="Reset export options to default values"
            ):
                if 'export_options' in st.session_state:
                    del st.session_state.export_options
                st.rerun()
    
    def _render_export_preview(self, prediction_history: List[Dict[str, Any]], single_result: Dict[str, Any], options: Dict[str, Any]) -> None:
        """Render a preview of what will be exported."""
        st.markdown("**👀 Export Preview**")
        
        if options['scope'] == 'single' and single_result:
            preview_data = self._prepare_single_export_data(single_result, options)
            st.write("**Single Result Export Preview:**")
            st.json(preview_data)
        elif options['scope'] == 'bulk' and prediction_history:
            # Show first few entries as preview
            preview_data = []
            for i, pred in enumerate(prediction_history[:3]):  # Show first 3
                preview_data.append(self._prepare_single_export_data(pred, options))
            
            st.write(f"**Bulk Export Preview (showing first 3 of {len(prediction_history)}):**")
            st.json(preview_data)
            
            if len(prediction_history) > 3:
                st.info(f"📄 Full export will include {len(prediction_history)} prediction entries.")
    
    def _prepare_single_export_data(self, prediction: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare a single prediction for export."""
        export_data = {
            'id': prediction.get('id', 'N/A'),
            'timestamp': self._format_timestamp(prediction.get('timestamp'), options['timestamp_format']),
            'input_text': prediction.get('input_text', ''),
            'sentiment_label': prediction.get('sentiment_label', ''),
            'confidence_score': prediction.get('confidence_score', 0.0),
            'processing_time_ms': prediction.get('processing_time_ms', 0.0)
        }
        
        # Add metadata if requested
        if options['include_metadata']:
            export_data.update({
                'text_length': len(prediction.get('input_text', '')),
                'word_count': len(prediction.get('input_text', '').split()),
                'model_used': 'DistilBERT Sentiment Analysis'
            })
        
        # Add model confidence if requested
        if options['include_model_confidence'] and prediction.get('model_confidence'):
            confidence_data = {}
            for score_data in prediction['model_confidence']:
                label = score_data.get('label', 'Unknown')
                score = score_data.get('score', 0.0)
                confidence_data[f'confidence_{label.lower()}'] = score
            
            export_data.update(confidence_data)
        
        return export_data
    
    def _format_timestamp(self, timestamp, format_type: str) -> str:
        """Format timestamp according to selected format."""
        if not timestamp:
            return 'N/A'
        
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                return timestamp
        
        if format_type == 'iso':
            return timestamp.isoformat()
        elif format_type == 'readable':
            return timestamp.strftime('%b %d, %Y %I:%M %p')
        elif format_type == 'unix':
            return str(int(timestamp.timestamp()))
        else:
            return timestamp.isoformat()
    
    def _export_single_result(self, single_result: Dict[str, Any], options: Dict[str, Any]) -> None:
        """Export a single prediction result."""
        try:
            export_data = self._prepare_single_export_data(single_result, options)
            export_format = options['format']
            
            if export_format == 'csv':
                self._export_to_csv([export_data], "single_result")
            elif export_format == 'json':
                self._export_to_json([export_data], "single_result")
            elif export_format == 'excel':
                self._export_to_excel([export_data], "single_result")
            
            st.success(f"✅ Single result exported successfully as {self.export_formats[export_format]['name']}!")
            
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")
    
    def _export_bulk_history(self, prediction_history: List[Dict[str, Any]], options: Dict[str, Any]) -> None:
        """Export bulk prediction history."""
        try:
            # Prepare all data
            export_data = []
            for pred in prediction_history:
                export_data.append(self._prepare_single_export_data(pred, options))
            
            export_format = options['format']
            
            if export_format == 'csv':
                self._export_to_csv(export_data, "prediction_history")
            elif export_format == 'json':
                self._export_to_json(export_data, "prediction_history")
            elif export_format == 'excel':
                self._export_to_excel(export_data, "prediction_history")
            
            st.success(f"✅ Bulk history exported successfully as {self.export_formats[export_format]['name']}!")
            
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")
    
    def _export_to_csv(self, export_data: List[Dict[str, Any]], export_type: str) -> None:
        """Export data to CSV format."""
        try:
            # Create DataFrame
            df = pd.DataFrame(export_data)
            
            # Convert to CSV
            csv_data = df.to_csv(index=False)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"sentiment_analysis_{export_type}_{timestamp}.csv"
            
            # Create download button
            st.download_button(
                label=f"📥 Download {filename}",
                data=csv_data,
                file_name=filename,
                mime=self.export_formats['csv']['mime_type']
            )
            
        except Exception as e:
            raise Exception(f"CSV export failed: {str(e)}")
    
    def _export_to_json(self, export_data: List[Dict[str, Any]], export_type: str) -> None:
        """Export data to JSON format."""
        try:
            # Convert to JSON
            json_data = json.dumps(export_data, indent=2, default=str)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"sentiment_analysis_{export_type}_{timestamp}.json"
            
            # Create download button
            st.download_button(
                label=f"📥 Download {filename}",
                data=json_data,
                file_name=filename,
                mime=self.export_formats['json']['mime_type']
            )
            
        except Exception as e:
            raise Exception(f"JSON export failed: {str(e)}")
    
    def _export_to_excel(self, export_data: List[Dict[str, Any]], export_type: str) -> None:
        """Export data to Excel format."""
        try:
            # Create DataFrame
            df = pd.DataFrame(export_data)
            
            # Convert to Excel
            from io import BytesIO
            buffer = BytesIO()
            
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Sentiment Analysis', index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Sentiment Analysis']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            buffer.seek(0)
            excel_data = buffer.read()
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"sentiment_analysis_{export_type}_{timestamp}.xlsx"
            
            # Create download button
            st.download_button(
                label=f"📥 Download {filename}",
                data=excel_data,
                file_name=filename,
                mime=self.export_formats['excel']['mime_type']
            )
            
        except Exception as e:
            raise Exception(f"Excel export failed: {str(e)}")
    
    def get_export_summary(self, prediction_history: List[Dict[str, Any]], single_result: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a summary of what would be exported.
        
        Args:
            prediction_history: List of prediction history entries
            single_result: Single prediction result
            
        Returns:
            Dictionary containing export summary information
        """
        summary = {
            'total_entries': 0,
            'export_types': [],
            'data_fields': [],
            'estimated_size': '0 KB'
        }
        
        if single_result:
            summary['export_types'].append('Single Result')
            summary['total_entries'] = 1
        elif prediction_history:
            summary['export_types'].append('Bulk History')
            summary['total_entries'] = len(prediction_history)
        
        # Estimate data size
        if summary['total_entries'] > 0:
            sample_size = min(100, summary['total_entries'])  # Sample up to 100 entries
            sample_data = prediction_history[:sample_size] if prediction_history else [single_result]
            
            total_chars = sum(len(str(pred.get('input_text', ''))) for pred in sample_data)
            avg_chars_per_entry = total_chars / len(sample_data)
            estimated_total_chars = avg_chars_per_entry * summary['total_entries']
            
            # Rough size estimation (1 character ≈ 1 byte)
            estimated_size_bytes = estimated_total_chars + (summary['total_entries'] * 500)  # Add overhead
            if estimated_size_bytes < 1024:
                summary['estimated_size'] = f"{estimated_size_bytes} B"
            elif estimated_size_bytes < 1024 * 1024:
                summary['estimated_size'] = f"{estimated_size_bytes / 1024:.1f} KB"
            else:
                summary['estimated_size'] = f"{estimated_size_bytes / (1024 * 1024):.1f} MB"
        
        # Data fields that will be included
        summary['data_fields'] = [
            'ID', 'Timestamp', 'Input Text', 'Sentiment Label', 
            'Confidence Score', 'Processing Time'
        ]
        
        return summary
