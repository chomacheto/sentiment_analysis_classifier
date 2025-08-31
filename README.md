# Sentiment Analysis Classifier

A modern, production-ready sentiment analysis system built with Python and Streamlit, featuring explainable AI, comprehensive sample data, and educational tools for portfolio demonstration.

## 🚀 Features

- **ML-Powered Analysis**: State-of-the-art transformer models for accurate sentiment classification
- **Explainable AI**: Word-level attention visualization with interactive heatmaps and contribution scores
- **Sample Data Gallery**: 20+ curated examples across 8 categories (reviews, social media, formal docs, sarcasm)
- **Educational Tools**: Interactive tutorial system, expected vs. actual results comparison
- **Use Case Documentation**: Comprehensive guides for different text types and industry applications
- **Performance Benchmarks**: Accuracy metrics and industry comparisons
- **Web Interface**: Beautiful Streamlit dashboard with professional styling
- **Real-time Analysis**: Instant sentiment classification with confidence scores
- **Export Capabilities**: CSV export for results and visualizations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.28+ with custom CSS and Tailwind CSS 3.3+
- **ML Framework**: PyTorch with Transformers for sentiment analysis
- **Visualization**: Plotly for interactive charts and attention heatmaps
- **Data Storage**: Local JSON files for sample data and benchmarks
- **Dependency Management**: Poetry for package management
- **Testing**: Pytest with 99% test coverage for new components

## 📋 Prerequisites

- Python 3.11+ (required for Streamlit compatibility)
- Poetry 1.7+ for dependency management
- Git for version control

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd sentiment_analysis_classifier
```

### 2. Environment Setup

```bash
# Create virtual environment
py -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (Linux/Mac)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install Poetry (if not already installed)
pip install poetry

# Install project dependencies
poetry install
```

### 4. Run the Application

```bash
# Start the Streamlit web interface
poetry run streamlit run apps/web/app.py
```

The application will be available at `http://localhost:8501`

## 🎯 Key Features in Detail

### 📚 Sample Data Gallery
- **20+ Curated Examples**: Diverse text samples across 8 categories
- **One-Click Loading**: Instantly load samples into the analysis interface
- **Smart Filtering**: Filter by category, difficulty level, and sentiment
- **Educational Metadata**: Each sample includes expected sentiment, difficulty, and use case

### 🔍 Explainable AI
- **Word-Level Attention**: Interactive heatmaps showing which words influence predictions
- **Contribution Scores**: Numerical scores for each word's impact on sentiment
- **Comparison Mode**: Compare attention patterns between different predictions
- **Export Visualizations**: Save attention heatmaps as images

### 🎓 Educational Tools
- **Interactive Tutorial**: Step-by-step guide for first-time users
- **Results Comparison**: Compare expected vs. actual sentiment predictions
- **Use Case Documentation**: Industry-specific examples and best practices
- **Performance Benchmarks**: Accuracy metrics on standard datasets

### 📊 Analysis Features
- **Real-time Processing**: Instant sentiment classification
- **Confidence Metrics**: Detailed confidence scores and uncertainty analysis
- **Prediction History**: Track and compare previous analyses
- **Export Results**: Download analysis results as CSV files

## 📁 Project Structure

```
sentiment-analysis-classifier/
├── apps/                    # Applications
│   ├── web/                # Streamlit frontend
│   │   ├── app.py          # Main web application
│   │   ├── static/         # CSS and static assets
│   │   └── requirements.txt
│   ├── api/                # API components (future)
│   └── ml_pipeline/        # CLI tools for model management
├── packages/                # Shared packages
│   ├── ml_core/            # Core ML operations
│   │   ├── sentiment_pipeline.py
│   │   ├── models.py
│   │   ├── config.py
│   │   └── validators.py
│   ├── ui_components/      # Reusable UI components
│   │   ├── example_gallery.py
│   │   ├── attention_visualization.py
│   │   ├── interactive_tutorial.py
│   │   ├── results_comparison.py
│   │   └── ... (other components)
│   └── shared/             # Common utilities
├── data/                   # Data files
│   └── samples/            # Sample data and benchmarks
│       ├── sample_data.json
│       ├── use_cases.json
│       └── benchmarks.json
├── docs/                   # Documentation
│   ├── architecture/       # System architecture docs
│   ├── stories/           # User stories and requirements
│   └── prd/               # Product requirements
├── tests/                  # Test suite
└── scripts/                # Build/deploy scripts
```

## 🔧 Development

### Adding Dependencies

```bash
# Add production dependency
poetry add package-name

# Add development dependency
poetry add --group dev package-name
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=.

# Run specific test file
poetry run pytest tests/test_sample_data.py

# Run tests for specific component
poetry run pytest tests/test_attention_visualization.py
```

### Code Quality

```bash
# Linting
poetry run flake8

# Type checking
poetry run mypy .

# Formatting
poetry run black .
```

## 📊 Testing Strategy

- **Unit Tests**: 99% coverage for new components
- **Integration Tests**: Component integration testing
- **UI Tests**: Streamlit component testing
- **Data Validation**: Sample data and benchmark validation

## 🚀 Deployment

### Development

```bash
# Local development with hot reload
poetry run streamlit run apps/web/app.py --server.port 8501
```

### Production

The application is designed for deployment on:
- **Streamlit Cloud**: Direct deployment from GitHub
- **Docker**: Containerized deployment with Dockerfile
- **Vercel**: Serverless deployment (future)

## 📚 Documentation

- **Architecture**: [docs/architecture/](docs/architecture/) - System design and components
- **User Stories**: [docs/stories/](docs/stories/) - Feature requirements and implementation
- **API Documentation**: [docs/architecture/api-specification.md](docs/architecture/api-specification.md)
- **Testing Strategy**: [docs/architecture/testing-strategy.md](docs/architecture/testing-strategy.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the [documentation](docs/) for detailed guides
- Review the [architecture documentation](docs/architecture/) for system design

## 🔄 Version History

- **v2.4.0** - Sample data gallery, educational tools, and use case documentation
- **v2.3.0** - Explainable AI with word-level attention visualization
- **v2.2.0** - Confidence visualization and performance metrics
- **v2.1.0** - Streamlit web interface foundation
- **v1.4.0** - Docker containerization
- **v1.3.0** - Command-line interface
- **v1.2.0** - Basic sentiment classification pipeline
- **v1.1.0** - Initial project setup
- See [CHANGELOG.md](CHANGELOG.md) for detailed version history

---

Built with ❤️ using modern Python and ML technologies for portfolio demonstration and educational purposes.
