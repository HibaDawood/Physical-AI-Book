# Quickstart Guide: Physical AI Book + RAG Chatbot

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (for local development)
- Git
- An OpenAI API key
- A Qdrant Cloud account
- A Neon PostgreSQL account

### 1. Clone the Repository
```bash
git clone <repository-url>
cd physical-ai-book
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual values:
# OPENAI_API_KEY=your_openai_key
# QDRANT_URL=your_qdrant_cluster_url
# QDRANT_API_KEY=your_qdrant_api_key
# DATABASE_URL=your_neon_database_url
# JWT_SECRET_KEY=your_jwt_secret

# Run database migrations (if applicable)
# This step depends on your ORM choice

# Start the backend server
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup (Docusaurus)
```bash
# From project root
cd frontend

# Install dependencies
npm install

# Set up environment variables for frontend
# Create or update .env file with:
# REACT_APP_API_BASE_URL=http://localhost:8000

# Start the development server
npm start
```

### 4. Initial Content Population
```bash
# After running the backend, populate book content using a script
cd backend
python scripts/populate_book_content.py
```

## API Testing

### Test the health endpoint
```bash
curl http://localhost:8000/health
```

### Test a simple chat query
```bash
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token" \
  -d '{
    "query": "What is Physical AI?",
    "language": "en"
  }'
```

## Building for Production

### Backend
```bash
# Build backend Docker image
docker build -t physical-ai-backend -f backend/Dockerfile .

# Run backend Docker container
docker run -p 8000:8000 --env-file backend/.env physical-ai-backend
```

### Frontend
```bash
# Build static assets
cd frontend
npm run build

# The built assets will be in the build/ directory
# These can be deployed to GitHub Pages
```

## Deployment

### Frontend to GitHub Pages
```bash
# After building the frontend
npm run deploy
```

### Backend to Cloud Platform
We recommend deploying the backend to cloud platforms like:
- Render
- Vercel
- AWS
- Google Cloud

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_openai_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_database_url
JWT_SECRET_KEY=your_jwt_secret
DEBUG=true  # Set to false for production
```

### Frontend (.env)
```
REACT_APP_API_BASE_URL=your_backend_api_url
```

## Project Structure
```
physical-ai-book/
├── backend/
│   ├── src/
│   │   ├── models/      # Pydantic models and data models
│   │   ├── services/    # Business logic
│   │   ├── api/         # API routes
│   │   └── main.py      # FastAPI app entrypoint
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/ (Docusaurus)
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Docusaurus pages
│   │   └── services/    # API clients
│   ├── docusaurus.config.js
│   └── package.json
├── scripts/             # Utility scripts
└── specs/               # Feature specifications
```

## Key Scripts

### Content Management
```bash
# Populate initial book content
python scripts/populate_book_content.py

# Update embeddings after content changes
python scripts/update_embeddings.py

# Run comprehensive tests
python -m pytest
```

## Troubleshooting

### Common Issues

1. **Embedding errors**: Make sure your OpenAI API key is valid and has sufficient credits
2. **Database connection errors**: Check your Neon PostgreSQL connection string
3. **Qdrant connection errors**: Verify your Qdrant cluster URL and API key
4. **CORS errors**: Ensure your frontend URL is in the backend's CORS allowlist

### Useful Commands
```bash
# Check backend logs
docker logs physical-ai-backend

# Check if backend is running
curl http://localhost:8000/health

# Run backend in debug mode
uvicorn src.main:app --reload --port 8000 --log-level debug
```