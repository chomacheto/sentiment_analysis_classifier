# Tech Stack

This is the **DEFINITIVE technology selection** for the entire project. All development must use these exact versions.

### Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|------------|
| **Frontend Language** | Python | 3.11+ | Streamlit compatibility | Latest stable Python with ML ecosystem support |
| **Frontend Framework** | Streamlit | 1.28+ | Interactive ML web interface | Perfect for ML demos, rapid prototyping, and production deployment |
| **UI Component Library** | Custom + Streamlit Components | Latest | Professional dashboard aesthetic | Combines Streamlit's ease with custom CSS for enterprise look |
| **State Management** | Streamlit Session State | Built-in | Simple state persistence | Native Streamlit approach, no external dependencies |
| **Backend Language** | Python | 3.11+ | ML ecosystem compatibility | Same language across stack, optimal for ML operations |
| **Backend Framework** | FastAPI | 0.104+ | High-performance ML API | Async support, automatic docs, perfect for ML serving |
| **API Style** | REST + WebSocket | OpenAPI 3.0 | Standard ML API patterns | REST for CRUD, WebSocket for real-time training progress |
| **Database** | PostgreSQL (Supabase) | 15+ | Reliable data storage | ACID compliance, JSON support, excellent for ML metadata |
| **Cache** | Redis (Vercel KV) | Latest | ML inference caching | Sub-millisecond response for repeated queries |
| **File Storage** | Supabase Storage | Latest | Model artifacts & datasets | Integrated with database, version control for models |
| **Authentication** | Supabase Auth | Latest | Secure user management | Built-in JWT, social logins, role-based access |
| **Frontend Testing** | Streamlit Testing | Latest | Component testing | Native Streamlit testing framework |
| **Backend Testing** | Pytest + FastAPI TestClient | Latest | API testing | Industry standard Python testing stack |
| **E2E Testing** | Playwright | Latest | Full user journey testing | Cross-browser, reliable ML workflow testing |
| **Build Tool** | Poetry | 1.7+ | Dependency management | Modern Python packaging, dependency resolution |
| **Bundler** | Nx | Latest | Monorepo management | Advanced workspace management for ML projects |
| **IaC Tool** | Vercel CLI + Supabase CLI | Latest | Platform-specific deployment | Native tools for chosen platforms |
| **CI/CD** | GitHub Actions | Latest | Automated testing & deployment | Industry standard, excellent ML workflow support |
| **Monitoring** | Vercel Analytics + Custom | Latest | Performance tracking | Built-in Vercel monitoring + custom ML metrics |
| **Logging** | Structlog + Vercel | Latest | Structured logging | Production-ready logging with ML context |
| **CSS Framework** | Tailwind CSS | 3.3+ | Utility-first styling | Rapid development, consistent design system |
