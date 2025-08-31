# Streamlit Web Interface

A professional web interface for the Sentiment Analysis Classifier built with Streamlit.

## Features

- **Clean, Professional Design**: Modern UI with custom CSS and responsive layout
- **Real-time Sentiment Analysis**: Instant results with confidence scoring
- **Character Limit Validation**: 1000 character limit with real-time feedback
- **Professional Styling**: Custom CSS with Tailwind-like utility classes
- **Responsive Design**: Works on desktop and mobile browsers
- **Session State Management**: Persistent user interactions and analysis history
- **Error Handling**: Clear error messages and user feedback
- **Loading States**: Visual feedback during processing

## Quick Start

### Prerequisites

- Python 3.11+
- Streamlit 1.28+
- Required ML dependencies (see requirements.txt)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

3. Open your browser and navigate to `http://localhost:8501`

## Usage

1. **Text Input**: Enter text in the input area (max 1000 characters)
2. **Analysis**: Click "Analyze Sentiment" to process your text
3. **Results**: View sentiment label, confidence score, and processing time
4. **History**: Access your analysis history in the expandable sections

## Components

### TextInputComponent
- Character limit validation
- Real-time character count
- Professional styling

### SentimentDisplay
- Sentiment label with color coding
- Confidence percentage and visual meter
- Processing time display
- Model confidence breakdown

### SidebarComponent
- Navigation structure
- Model information
- User preferences
- Theme selection

## Architecture

The web interface follows a component-based architecture:

```
apps/web/
├── app.py                 # Main Streamlit application
├── static/
│   └── styles.css        # Custom CSS with utility classes
└── requirements.txt       # Python dependencies

packages/ui_components/
├── text_input.py         # Text input component
├── sentiment_display.py  # Results display component
├── sidebar.py           # Sidebar navigation component
└── __init__.py          # Package initialization
```

## Styling

The interface uses a combination of:
- **Custom CSS**: Professional color scheme and typography
- **Tailwind-like Utilities**: Responsive design utilities
- **Streamlit Components**: Native Streamlit widgets and layouts
- **Responsive Design**: Mobile-first approach with breakpoints

## Testing

Run the test suite:

```bash
python -m pytest tests/test_web_interface.py -v
```

Test coverage includes:
- Component initialization
- Input validation
- UI rendering
- Integration testing

## Future Enhancements

- **Real-time Updates**: WebSocket integration for live results
- **Batch Processing**: Multiple text analysis
- **Export Functionality**: Download results as CSV/JSON
- **Advanced Analytics**: Sentiment trends and insights
- **User Authentication**: Multi-user support
- **API Integration**: REST API consumption

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the project root is in your Python path
2. **Model Loading**: Check that ML dependencies are properly installed
3. **Styling Issues**: Verify CSS files are accessible
4. **Performance**: Ensure adequate system resources for ML models

### Debug Mode

Enable debug logging by setting environment variables:
```bash
export STREAMLIT_LOG_LEVEL=debug
export STREAMLIT_SERVER_HEADLESS=true
```

## Contributing

1. Follow the established coding standards
2. Add tests for new functionality
3. Maintain >90% test coverage
4. Update documentation as needed

## License

This project is licensed under the same terms as the main repository.
