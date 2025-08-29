# API Specification

### REST API Endpoints

**Core Endpoints:**
- `POST /api/analyze` - Single text sentiment analysis
- `POST /api/analyze/batch` - Batch text processing
- `GET /api/models` - List available models
- `POST /api/models/compare` - Compare multiple models
- `POST /api/fine-tune` - Start model fine-tuning
- `GET /api/health` - System health check

**Authentication:** JWT tokens via Supabase Auth
**Rate Limiting:** 100 requests/minute per user, 1000 requests/minute per IP
**Response Format:** Standardized JSON with error handling
