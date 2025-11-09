"""
Database configuration and models
Sets up SQLAlchemy connection and defines Quiz table schema
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment or use SQLite as default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz_history.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600  # Recycle connections after 1 hour
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create base class for models
Base = declarative_base()


class Quiz(Base):
    """
    Quiz database model
    Stores quiz data including URL, title, content, and generated quiz JSON
    """
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String(500), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    date_generated = Column(DateTime, default=datetime.utcnow, nullable=False)
    scraped_content = Column(Text, nullable=True)  # Raw HTML for reference
    full_quiz_data = Column(Text, nullable=False)  # JSON string of quiz data
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}')>"


def init_db():
    """
    Initialize database tables
    Creates all tables defined by Base models if they don't exist
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        raise


def get_db():
    """
    Database session dependency
    Yields a session and ensures it's closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database on module import
if __name__ == "__main__":
    init_db()
    print("Database setup complete!")