# Sentiment Analysis Classifier

A modern, production-ready sentiment analysis system built with Python, FastAPI, and Streamlit, designed for enterprise ML workflows.

## 🚀 Features

- **ML-Powered Analysis**: State-of-the-art transformer models for accurate sentiment classification
- **Web Interface**: Beautiful Streamlit dashboard for interactive analysis
- **REST API**: FastAPI backend for integration with other systems
- **Real-time Training**: WebSocket support for live model updates
- **Enterprise Ready**: PostgreSQL database, Redis caching, and comprehensive monitoring

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.49+ with custom UI components
- **Backend**: FastAPI 0.116+ with async support
- **ML Framework**: PyTorch 2.8+ with Transformers 4.56+
- **Database**: PostgreSQL 15+ (Supabase)
- **Cache**: Redis (Vercel KV)
- **Dependency Management**: Poetry 2.1+
- **Build Tool**: Nx for monorepo management

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
poetry run streamlit run apps/web/main.py

# Start the FastAPI backend (in another terminal)
poetry run uvicorn apps.api.main:app --reload
```

## 📁 Project Structure

```
sentiment-analysis-classifier/
├── apps/                    # Applications
│   ├── web/                # Streamlit frontend
│   ├── api/                # FastAPI ML serving backend
│   └── ml-pipeline/        # Training and model management
├── packages/                # Shared packages
│   ├── shared/             # Common types/utilities
│   ├── ml-core/            # Core ML operations
│   └── ui-components/      # Reusable UI components
├── infrastructure/          # Infrastructure as Code
├── docs/                   # Documentation
├── scripts/                 # Build/deploy scripts
└── tests/                  # Test suite
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
poetry run pytest tests/test_ml_core.py
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

- **Unit Tests**: 70% coverage target for core functionality
- **Integration Tests**: 20% coverage for API and database interactions
- **E2E Tests**: 10% coverage using Playwright for full user journeys

## 🚀 Deployment

### Development

```bash
# Local development with hot reload
poetry run streamlit run apps/web/main.py --server.port 8501
poetry run uvicorn apps.api.main:app --reload --port 8000
```

### Production

The application is designed for deployment on:
- **Frontend**: Vercel (Streamlit)
- **Backend**: Vercel Functions (FastAPI)
- **Database**: Supabase (PostgreSQL)
- **Cache**: Vercel KV (Redis)

## 📚 API Documentation

Once the FastAPI server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

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

- **v0.1.0** - Initial project setup and environment configuration
- See [CHANGELOG.md](CHANGELOG.md) for detailed version history

---

Built with ❤️ using modern Python and ML technologies
