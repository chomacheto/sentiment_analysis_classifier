# Data Models

### SentimentAnalysis Model

**Purpose:** Core entity representing a single sentiment analysis request and result

**Key Attributes:**
- `id`: UUID - Unique identifier for the analysis
- `text_input`: TEXT - Raw text input from user
- `sentiment_label`: VARCHAR(20) - Predicted sentiment (positive, negative, neutral)
- `confidence_score`: DECIMAL(5,4) - Model confidence (0.0000 to 1.0000)
- `model_used`: VARCHAR(50) - Name/version of the model used
- `processing_time_ms`: INTEGER - Time taken for inference
- `created_at`: TIMESTAMP - When analysis was performed
- `user_id`: UUID - User who requested analysis (nullable for anonymous)

**TypeScript Interface:**
```typescript
interface SentimentAnalysis {
  id: string;
  textInput: string;
  sentimentLabel: 'positive' | 'negative' | 'neutral';
  confidenceScore: number;
  modelUsed: string;
  processingTimeMs: number;
  createdAt: Date;
  userId?: string;
  metadata?: {
    wordCount: number;
    language: string;
    preprocessingSteps: string[];
  };
}
```

### ModelVersion Model

**Purpose:** Tracks different versions of ML models for comparison and A/B testing

**Key Attributes:**
- `id`: UUID - Unique model identifier
- `model_name`: VARCHAR(100) - Human-readable model name
- `model_type`: VARCHAR(50) - Model architecture (BERT, DistilBERT, RoBERTa)
- `version_tag`: VARCHAR(20) - Semantic version
- `huggingface_id`: VARCHAR(200) - Hugging Face model identifier
- `accuracy_score`: DECIMAL(5,4) - Validation accuracy on test set
- `is_active`: BOOLEAN - Whether this model is currently serving requests
