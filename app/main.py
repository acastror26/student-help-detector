from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.container import Container
from app.api import endpoints
from sqlalchemy.orm import sessionmaker
from app.data.entities.models import Base
from app.config.settings import settings
from sqlalchemy import create_engine
from dependency_injector.wiring import inject, Provide
import logging
import logstash

# Set up logging
logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)
logger.addHandler(logstash.TCPLogstashHandler(settings.LOGSTASH_HOST, settings.LOGSTASH_PORT, version=1))

# Create the FastAPI app
app = FastAPI()

# Dependency Injection
container = Container()
app.container = container

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(endpoints.router)

# Root endpoint for sanity check
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "FastAPI Hexagonal Architecture App running!"}

# Dependency injector wiring
@app.on_event("startup")
@inject
def startup(container: Container = Provide[Container]):
    logger.info("Application startup - Dependency Injection container initialized")
