# Unified Project Structure

```
sentiment-analysis-classifier/
├── apps/
│   ├── web/           # Streamlit frontend
│   ├── api/           # FastAPI ML serving backend
│   └── ml-pipeline/   # Training and model management
├── packages/
│   ├── shared/        # Common types/utilities
│   ├── ml-core/       # Core ML operations
│   └── ui-components/ # Reusable UI components
├── infrastructure/     # IaC definitions
├── docs/              # Documentation
└── scripts/           # Build/deploy scripts
```
