"""
Pydantic models for request/response validation
Defines the structure of quiz data and API responses
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime


class QuizQuestion(BaseModel):
    """Single quiz question schema"""
    question: str = Field(..., description="The quiz question text")
    options: List[str] = Field(..., min_length=4, max_length=4, description="Four answer options")
    answer: str = Field(..., description="The correct answer")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")
    explanation: str = Field(..., description="Explanation for the answer")
    section: Optional[str] = Field(None, description="Article section this question relates to")
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        """Ensure difficulty is valid"""
        allowed = ['easy', 'medium', 'hard']
        return v.lower() if v.lower() in allowed else 'medium'


class KeyEntities(BaseModel):
    """Key entities extracted from article"""
    people: List[str] = Field(default_factory=list, description="Notable people")
    organizations: List[str] = Field(default_factory=list, description="Organizations")
    locations: List[str] = Field(default_factory=list, description="Locations")


class QuizResponse(BaseModel):
    """Complete quiz response"""
    id: int
    url: str
    title: str
    summary: str
    key_entities: KeyEntities
    sections: List[str]
    quiz: List[QuizQuestion]
    related_topics: List[str]
    date_generated: datetime
    is_cached: bool = False


class QuizHistoryItem(BaseModel):
    """Quiz history list item"""
    id: int
    url: str
    title: str
    date_generated: datetime
    question_count: Optional[int] = None


class URLInput(BaseModel):
    """URL input validation"""
    url: str = Field(..., min_length=10, max_length=500)
    
    @validator('url')
    def validate_wikipedia_url(cls, v):
        """Validate Wikipedia URL"""
        v = v.strip()
        if "wikipedia.org/wiki/" not in v:
            raise ValueError("Must be a Wikipedia article URL")
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class URLPreviewResponse(BaseModel):
    """URL preview response"""
    url: str
    title: str
    summary: Optional[str] = None
    is_valid: bool
    exists_in_db: bool
    cached_quiz_id: Optional[int] = None
    image_url: Optional[str] = None
    word_count: Optional[int] = None


class QuizSubmission(BaseModel):
    """Quiz submission for scoring"""
    quiz_id: int
    answers: Dict[int, str] = Field(..., description="Map of question index to answer")
    time_taken: Optional[int] = Field(None, description="Time taken in seconds")


class QuizScoreResponse(BaseModel):
    """Quiz score response"""
    quiz_id: int
    total_questions: int
    correct_answers: int
    score_percentage: float
    results: List[Dict]
    time_taken: Optional[int] = None