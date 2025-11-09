"""
FastAPI Main Application
Handles all API endpoints for quiz generation and retrieval
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
from datetime import datetime

from database import get_db, init_db, Quiz
from scraper import scrape_wikipedia, preview_wikipedia_url
from llm_quiz_generator import generate_quiz
from models import (
    QuizResponse, QuizHistoryItem, URLInput, URLPreviewResponse,
    QuizSubmission, QuizScoreResponse
)

# ============================================================
# Initialize FastAPI app
# ============================================================
app = FastAPI(
    title="AI Wiki Quiz Generator API",
    description="Generate quizzes from Wikipedia articles using AI",
    version="2.0.0"
)

# ============================================================
# CORS Configuration
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend can be on different domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Startup Event
# ============================================================
@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    print("\n" + "=" * 60)
    print("🚀 AI Wiki Quiz Generator API Starting...")
    print("=" * 60)
    init_db()
    print("✅ Server ready")
    print("🔗 API Docs: http://localhost:8000/docs")
    print("=" * 60 + "\n")


# ============================================================
# API ROUTES
# ============================================================

@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "message": "AI Wiki Quiz Generator API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/preview_url", response_model=URLPreviewResponse)
def preview_url(input_data: URLInput, db: Session = Depends(get_db)):
    """
    Preview Wikipedia URL before generating quiz
    - Validates URL
    - Fetches title and summary
    - Checks if already cached in database
    """
    try:
        url = input_data.url
        print(f"\n🔍 Preview Request: {url}")

        # Check if exists in database
        existing = db.query(Quiz).filter(Quiz.url == url).first()

        # Get preview from Wikipedia
        preview_data = preview_wikipedia_url(url)

        if not preview_data.get("is_valid"):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid URL: {preview_data.get('error', 'Unknown error')}"
            )

        response = URLPreviewResponse(
            url=url,
            title=preview_data["title"],
            summary=preview_data.get("summary"),
            is_valid=True,
            exists_in_db=existing is not None,
            cached_quiz_id=existing.id if existing else None,
            image_url=preview_data.get("image_url"),
            word_count=preview_data.get("word_count")
        )

        print(f"✅ Preview: {preview_data['title']} (Cached: {existing is not None})")
        return response

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Preview Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate_quiz", response_model=QuizResponse)
def generate_quiz_endpoint(input_data: URLInput, db: Session = Depends(get_db)):
    """
    Generate quiz from Wikipedia URL
    - Checks cache first
    - Scrapes article
    - Generates quiz with AI
    - Stores in database
    - Returns quiz data
    """
    try:
        url = input_data.url

        print(f"\n{'=' * 60}")
        print(f"🔍 Quiz Request: {url}")
        print(f"{'=' * 60}")

        # Step 1: Check cache
        existing = db.query(Quiz).filter(Quiz.url == url).first()
        if existing:
            print(f"✅ Cache hit (ID: {existing.id})")
            quiz_data = json.loads(existing.full_quiz_data)
            return QuizResponse(
                id=existing.id,
                url=existing.url,
                date_generated=existing.date_generated,
                is_cached=True,
                **quiz_data
            )

        # Step 2: Scrape Wikipedia
        print("🌐 Scraping...")
        article_text, title, raw_html = scrape_wikipedia(url)
        print(f"✅ Scraped: {title}")

        # Step 3: Generate quiz with AI
        print("🤖 Generating quiz...")
        quiz_data = generate_quiz(article_text, title)
        print(f"✅ Generated {len(quiz_data['quiz'])} questions")

        # Step 4: Save to database
        print("💾 Saving...")
        new_quiz = Quiz(
            url=url,
            title=quiz_data["title"],
            scraped_content=raw_html[:50000],
            full_quiz_data=json.dumps(quiz_data, ensure_ascii=False)
        )
        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        print(f"✅ Saved (ID: {new_quiz.id})")

        print(f"{'=' * 60}\n")

        # Step 5: Return response
        return QuizResponse(
            id=new_quiz.id,
            url=new_quiz.url,
            date_generated=new_quiz.date_generated,
            is_cached=False,
            **quiz_data
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {e}\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/submit_quiz", response_model=QuizScoreResponse)
def submit_quiz(submission: QuizSubmission, db: Session = Depends(get_db)):
    """
    Score a completed quiz
    - Validates answers
    - Calculates score
    - Returns detailed results
    """
    try:
        quiz_id = submission.quiz_id
        user_answers = submission.answers

        print(f"\n📊 Scoring Quiz {quiz_id}...")

        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        quiz_data = json.loads(quiz.full_quiz_data)
        questions = quiz_data.get("quiz", [])

        correct_count = 0
        results = []

        for idx, question in enumerate(questions):
            user_answer = user_answers.get(idx) or user_answers.get(str(idx))
            correct_answer = question["answer"]
            is_correct = user_answer == correct_answer

            if is_correct:
                correct_count += 1

            results.append({
                "question_index": idx,
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question["explanation"],
                "section": question.get("section", "General")
            })

        total = len(questions)
        percentage = (correct_count / total * 100) if total > 0 else 0

        print(f"✅ Score: {correct_count}/{total} ({percentage:.1f}%)")

        return QuizScoreResponse(
            quiz_id=quiz_id,
            total_questions=total,
            correct_answers=correct_count,
            score_percentage=round(percentage, 2),
            results=results,
            time_taken=submission.time_taken
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Scoring error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history", response_model=list[QuizHistoryItem])
def get_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get quiz history with question counts"""
    try:
        quizzes = db.query(Quiz).order_by(
            Quiz.date_generated.desc()
        ).offset(skip).limit(limit).all()

        history_items = []
        for quiz in quizzes:
            try:
                quiz_data = json.loads(quiz.full_quiz_data)
                q_count = len(quiz_data.get("quiz", []))
            except:
                q_count = None

            history_items.append(QuizHistoryItem(
                id=quiz.id,
                url=quiz.url,
                title=quiz.title,
                date_generated=quiz.date_generated,
                question_count=q_count
            ))

        return history_items

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/quiz/{quiz_id}", response_model=QuizResponse)
def get_quiz_details(quiz_id: int, db: Session = Depends(get_db)):
    """Get specific quiz details by ID"""
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        quiz_data = json.loads(quiz.full_quiz_data)

        return QuizResponse(
            id=quiz.id,
            url=quiz.url,
            date_generated=quiz.date_generated,
            is_cached=True,
            **quiz_data
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Run the App
# ============================================================
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Wiki Quiz Generator API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")