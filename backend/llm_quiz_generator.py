"""
Diagnostic Quiz Generator - Troubleshoots empty related topics
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import json

load_dotenv()


def generate_quiz(article_text: str, article_title: str) -> dict:
    """Generate quiz with detailed diagnostics"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # Using the correct model for your API
        google_api_key=api_key,
        temperature=0.7,
        max_tokens=8000
    )
    
    # Simplified, clearer prompt focusing on related topics
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an educational quiz creator. Create a quiz from the article.

IMPORTANT: Return a valid JSON object with this EXACT structure:

{{
  "title": "article title",
  "summary": "2-3 sentence summary",
  "key_entities": {{
    "people": ["person1", "person2"],
    "organizations": ["org1", "org2"],
    "locations": ["location1", "location2"]
  }},
  "sections": ["section1", "section2"],
  "quiz": [
    {{
      "question": "question text?",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "difficulty": "easy",
      "explanation": "explanation text",
      "section": "section name"
    }}
  ],
  "related_topics": ["topic1", "topic2", "topic3", "topic4", "topic5"]
}}

REQUIREMENTS:
1. Generate 7-10 quiz questions
2. Generate AT LEAST 5 related_topics (topics for further study)
3. Each question must have exactly 4 options
4. Answer must exactly match one option
5. Difficulty: easy, medium, or hard

For related_topics, suggest topics like:
- Related concepts not fully covered in the article
- Similar technologies or methodologies
- Broader or narrower topics
- Applications or use cases
- Historical context or future developments

Return ONLY the JSON object, no other text."""),
        ("human", """Article: {title}

Content:
{article_text}

Generate the quiz JSON with all required fields including related_topics.""")
    ])
    
    # Don't use JsonOutputParser initially - let's see raw output
    chain = prompt | llm
    
    try:
        print(f"\n{'='*70}")
        print(f"🤖 GENERATING QUIZ: {article_title}")
        print(f"{'='*70}\n")
        
        # Get raw response
        raw_response = chain.invoke({
            "title": article_title,
            "article_text": article_text[:20000]
        })
        
        print(f"{'='*70}")
        print("RAW RESPONSE FROM GEMINI:")
        print(f"{'='*70}")
        print(f"Type: {type(raw_response)}")
        
        # Extract content from response object
        if hasattr(raw_response, 'content'):
            response_text = raw_response.content
        else:
            response_text = str(raw_response)
        
        print(f"\nResponse length: {len(response_text)} characters")
        print(f"\nFirst 500 chars:")
        print(response_text[:500])
        print(f"\nLast 500 chars:")
        print(response_text[-500:])
        print(f"{'='*70}\n")
        
        # Clean the response
        response_text = response_text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            print("⚠️  Removing markdown code blocks...")
            lines = response_text.split("\n")
            # Remove first and last lines (```)
            response_text = "\n".join(lines[1:-1])
            if response_text.startswith("json"):
                response_text = response_text[4:].strip()
        
        # Parse JSON
        print("Attempting to parse JSON...")
        result = json.loads(response_text)
        
        print(f"\n{'='*70}")
        print("PARSED JSON STRUCTURE:")
        print(f"{'='*70}")
        print(f"Keys in result: {list(result.keys())}")
        print(f"\nField analysis:")
        print(f"  - title: '{result.get('title', 'MISSING')}'")
        print(f"  - summary length: {len(result.get('summary', ''))} chars")
        print(f"  - quiz questions: {len(result.get('quiz', []))}")
        print(f"  - sections: {len(result.get('sections', []))}")
        print(f"  - related_topics: {result.get('related_topics', 'MISSING')}")
        print(f"  - related_topics type: {type(result.get('related_topics', None))}")
        print(f"  - related_topics length: {len(result.get('related_topics', []))}")
        
        if 'key_entities' in result:
            print(f"  - key_entities.people: {len(result['key_entities'].get('people', []))}")
            print(f"  - key_entities.organizations: {len(result['key_entities'].get('organizations', []))}")
            print(f"  - key_entities.locations: {len(result['key_entities'].get('locations', []))}")
        
        print(f"{'='*70}\n")
        
        # Show full related_topics
        if 'related_topics' in result:
            print(f"RELATED TOPICS CONTENT:")
            print(f"  {result['related_topics']}")
            print()
        
        # Validate
        validated_result = validate_quiz_output(result, article_title)
        
        print(f"\n✅ FINAL OUTPUT:")
        print(f"  → Questions: {len(validated_result['quiz'])}")
        print(f"  → Related topics: {validated_result['related_topics']}")
        print(f"  → Related topics count: {len(validated_result['related_topics'])}")
        
        return validated_result
        
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON PARSING ERROR:")
        print(f"  Error: {str(e)}")
        print(f"  Position: line {e.lineno}, column {e.colno}")
        print(f"\n  Problematic section:")
        lines = response_text.split("\n")
        start = max(0, e.lineno - 3)
        end = min(len(lines), e.lineno + 3)
        for i in range(start, end):
            marker = ">>>" if i == e.lineno - 1 else "   "
            print(f"  {marker} {i+1}: {lines[i]}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"  Message: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def validate_quiz_output(result: dict, article_title: str) -> dict:
    """Validate with detailed logging"""
    
    print(f"\n{'='*70}")
    print("VALIDATION:")
    print(f"{'='*70}")
    
    # Get related topics with debugging
    related_topics_raw = result.get("related_topics", [])
    print(f"Related topics raw value: {related_topics_raw}")
    print(f"Related topics raw type: {type(related_topics_raw)}")
    
    # Handle different types
    if related_topics_raw is None:
        print("⚠️  related_topics is None")
        related_topics = []
    elif isinstance(related_topics_raw, str):
        print("⚠️  related_topics is a string, splitting...")
        related_topics = [t.strip() for t in related_topics_raw.split(",") if t.strip()]
    elif isinstance(related_topics_raw, list):
        print(f"✓ related_topics is a list with {len(related_topics_raw)} items")
        related_topics = [str(t).strip() for t in related_topics_raw if t]
    else:
        print(f"⚠️  related_topics is unexpected type: {type(related_topics_raw)}")
        related_topics = []
    
    print(f"Related topics after processing: {related_topics}")
    
    validated = {
        "title": result.get("title", article_title),
        "summary": result.get("summary", "No summary available."),
        "key_entities": {
            "people": result.get("key_entities", {}).get("people", [])[:10],
            "organizations": result.get("key_entities", {}).get("organizations", [])[:10],
            "locations": result.get("key_entities", {}).get("locations", [])[:10]
        },
        "sections": result.get("sections", [])[:15],
        "quiz": [],
        "related_topics": related_topics[:10]
    }
    
    # Validate questions
    quiz_questions = result.get("quiz", [])
    print(f"\nProcessing {len(quiz_questions)} questions...")
    
    for idx, q in enumerate(quiz_questions[:10], 1):
        if not isinstance(q, dict):
            continue
        
        required = ["question", "options", "answer", "difficulty", "explanation"]
        if not all(f in q for f in required):
            print(f"  ⚠️  Q{idx}: Missing required fields")
            continue
        
        options = q.get("options", [])
        if not isinstance(options, list) or len(options) != 4:
            print(f"  ⚠️  Q{idx}: Invalid options")
            continue
        
        options = [str(opt).strip() for opt in options if opt]
        if len(options) != 4 or len(set(options)) != 4:
            print(f"  ⚠️  Q{idx}: Duplicate options")
            continue
        
        answer = str(q.get("answer", "")).strip()
        if answer not in options:
            # Case-insensitive match
            for opt in options:
                if opt.lower() == answer.lower():
                    answer = opt
                    break
            else:
                answer = options[0]
        
        difficulty = q.get("difficulty", "medium").lower()
        if difficulty not in ["easy", "medium", "hard"]:
            difficulty = "medium"
        
        validated["quiz"].append({
            "question": q["question"].strip(),
            "options": options,
            "answer": answer,
            "difficulty": difficulty,
            "explanation": q["explanation"].strip(),
            "section": q.get("section", "General")
        })
        
        print(f"  ✓ Q{idx}: Valid")
    
    if len(validated["quiz"]) < 7:
        raise ValueError(f"Only {len(validated['quiz'])} valid questions (minimum 7)")
    
    print(f"\nValidation complete:")
    print(f"  → {len(validated['quiz'])} questions")
    print(f"  → {len(validated['related_topics'])} related topics")
    print(f"{'='*70}")
    
    return validated


if __name__ == "__main__":
    test_text = """
    Python is a high-level, interpreted programming language created by Guido van Rossum 
    and first released in 1991. It emphasizes code readability with significant indentation.
    Python is dynamically typed and supports multiple programming paradigms including 
    object-oriented, functional, and procedural programming.
    
    Python 2.0 was released in 2000 with features like list comprehensions. Python 3.0, 
    released in 2008, was a major revision not completely backward-compatible with earlier versions.
    
    Python is widely used in web development (Django, Flask), data science (pandas, NumPy), 
    machine learning (TensorFlow, scikit-learn), automation, and scientific computing.
    """
    
    try:
        quiz = generate_quiz(test_text, "Python Programming")
        print(f"\n{'='*70}")
        print("SUCCESS!")
        print(f"{'='*70}")
        print(f"Title: {quiz['title']}")
        print(f"Questions: {len(quiz['quiz'])}")
        print(f"Related Topics: {quiz['related_topics']}")
    except Exception as e:
        print(f"\n{'='*70}")
        print("FAILED!")
        print(f"{'='*70}")
        print(f"Error: {e}")