from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import book_content, chat, auth, user
from src.middleware.error_handler import setup_error_handlers
from src.utils.logger import setup_logging


def create_app() -> FastAPI:
    app = FastAPI(
        title="Physical AI Book API",
        description="API for Physical AI educational content and RAG chatbot",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
    )

    # Setup logging
    setup_logging()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup error handlers
    setup_error_handlers(app)

    # Include API routes
    app.include_router(book_content.router, prefix="/api/v1", tags=["book"])
    app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
    app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
    app.include_router(user.router, prefix="/api/v1", tags=["user"])

    @app.get("/api/v1/health")
    async def health_check():
        return {"status": "healthy", "service": "Physical AI Book Backend"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)