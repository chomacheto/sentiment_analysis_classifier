# Technical Assumptions

### Repository Structure: Monorepo

Single repository containing all components (ML pipeline, API, web interface, documentation) to simplify development workflow, enable atomic commits across components, and demonstrate full-stack project organization skills in interviews. This approach facilitates easier dependency management and deployment while maintaining clear modular separation.

### Service Architecture

**CRITICAL DECISION:** Simplified modular monolithic architecture within a monorepo structure. Designed for rapid development and reliable deployment while demonstrating understanding of professional software patterns. Core services include:

- **Inference Service:** Real-time sentiment classification with basic caching
- **Training Service:** Model fine-tuning and evaluation workflows
- **API Gateway:** FastAPI-based REST endpoints with authentication and rate limiting
- **Web Interface:** Streamlit-based demo interface
- **Data Pipeline:** ETL processes for dataset handling and preprocessing

This pragmatic architecture balances technical sophistication with development velocity appropriate for solo project timeline and interview demonstration needs.

### Testing Requirements

**CRITICAL DECISION:** Pragmatic testing approach focused on demonstrating professional practices without overengineering:

- **Model Testing:** Accuracy validation, basic bias detection, and regression testing for model outputs
- **API Testing:** Core endpoint functionality and error handling using pytest
- **Integration Testing:** End-to-end pipeline validation from input to output
- **Coverage Goal:** 70% for core functions (realistic target that still demonstrates testing competency)
- **Manual Testing Convenience:** Automated test data generation and clear setup instructions

Testing strategy showcases software engineering maturity while maintaining focus on core functionality delivery.

### Additional Technical Assumptions and Requests

**Core Technology Stack (Phase 1 - MVP):**
- **Python Version:** Python 3.8+ for broad compatibility with ML libraries
- **ML Framework:** PyTorch with Hugging Face Transformers for model implementation
- **API Framework:** FastAPI for high-performance REST endpoints with automatic documentation
- **Frontend:** Streamlit for rapid prototyping and professional demo interface
- **Database:** SQLite for development with documented PostgreSQL migration path
- **Containerization:** Docker with multi-stage builds for deployment

**Infrastructure and Deployment (Risk-Mitigated):**
- **Primary Hosting:** AWS Elastic Beanstalk or Railway for reliable demo deployment
- **Backup Strategy:** Local Docker setup with clear instructions for interview demos
- **CI/CD:** GitHub Actions for automated testing and deployment
- **Monitoring:** Basic structured logging with JSON format for debugging

**Development Workflow:**
- **Code Quality:** Black formatter and basic linting for consistent style
- **Documentation:** Comprehensive README with setup and usage instructions
- **Version Control:** Git with clear commit messages and semantic versioning
- **Package Management:** pip with requirements.txt (simple dependency management)

**Optional Enhancements (Phase 2/3 if time permits):**
- **MLflow:** For model experiment tracking and comparison
- **DVC:** For dataset versioning if needed
- **Advanced Monitoring:** Performance metrics and usage analytics
- **ONNX Support:** For optimized inference if performance becomes critical

**Key Strategic Changes Applied:**
- Simplified technology stack to reduce complexity risk while maintaining professional appearance
- Pragmatic testing approach that demonstrates competency without overengineering
- Risk-mitigated deployment strategy with reliable backup options for demo scenarios
- Clear phase-based implementation prioritizing core functionality over advanced tooling
- Focus on technologies that directly support interview demonstration and portfolio impact

---
