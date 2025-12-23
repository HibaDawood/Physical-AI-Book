# Physical AI Book + RAG Chatbot

A comprehensive educational platform for Physical AI with an integrated RAG chatbot that answers questions based only on book content.

## Features

- **Educational Book Content**: Comprehensive chapters on Physical AI, Robotics AI, Agentic AI, Sensors + AI Integration, and Edge AI
- **RAG Chatbot**: AI-powered assistant that answers questions based only on book content
- **Premium UI**: VIP design with smooth animations and modern dashboard
- **Multilingual Support**: Toggle between English and Urdu
- **Interactive Elements**: Highlight and ask AI about specific text selections
- **Floating Chat Interface**: Available on all pages for seamless access

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (with Neon)
- **Vector Database**: Qdrant (for embeddings and RAG)
- **AI Integration**: GEMINI API for embeddings and completions
- **Authentication**: JWT-based auth system

### Frontend
- **Framework**: Docusaurus
- **Language**: React
- **Styling**: Custom CSS with premium design elements

## Architecture

The system is divided into two main components:

### Backend Structure
```
backend/
├── src/
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   ├── api/              # API routes
│   ├── database/         # DB models and session
│   ├── ai_services/      # RAG and AI logic
│   ├── auth/             # Authentication
│   ├── middleware/       # Request processing
│   └── utils/            # Utility functions
├── tests/
├── requirements.txt
└── pyproject.toml
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/       # React components
│   ├── pages/            # Page components
│   ├── services/         # API services
│   ├── theme/            # Theme files
│   └── utils/            # Utility functions
├── docs/                 # Book content
├── package.json
└── docusaurus.config.js
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- An GEMINI API key
- A Qdrant Cloud account
- A Neon PostgreSQL account

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Edit `.env` with your configuration:
```
OPENAI_API_KEY=your_openai_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_database_url
JWT_SECRET_KEY=your_jwt_secret
```

6. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## API Endpoints

### Book Content
- `GET /api/v1/book/contents` - Get all book content with filters
- `GET /api/v1/book/contents/{content_id}` - Get specific content
- `GET /api/v1/book/chapters` - Get hierarchical chapter list

### Chat
- `POST /api/v1/chat/query` - Submit query to RAG chatbot

### User & Auth
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/user/profile` - Get user profile

### Bookmarks
- `POST /api/v1/user/bookmarks` - Create bookmark
- `GET /api/v1/user/bookmarks` - Get user bookmarks

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

## Running Tests

### Backend
```bash
python -m pytest
```

## Deployment

### Frontend to GitHub Pages
```bash
npm run build
npm run deploy
```

### Backend to Cloud Platform
We recommend deploying the backend to cloud platforms like:
- Render
- Vercel
- AWS
- Google Cloud

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues, please file them in the [Issues](https://github.com/your-username/physical-ai-book/issues) section.