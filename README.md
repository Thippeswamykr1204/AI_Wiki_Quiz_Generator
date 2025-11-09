# 🎓 AI Wiki Quiz Generator - DeepKlarity Technologies

Transform Wikipedia articles into engaging, educational quizzes using AI (Google Gemini).

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104-green.svg)

## ✨ Features

### Core Features
- 🤖 **AI-Powered Quiz Generation** - Uses Google Gemini API
- 📚 **Wikipedia Integration** - Scrapes and processes articles
- 🎯 **Interactive Quiz Mode** - Take quizzes with automatic scoring
- ⏱️ **Time Tracking** - Tracks quiz completion time
- 💾 **Smart Caching** - Prevents duplicate URL processing
- 📊 **Quiz History** - View all previously generated quizzes

### Bonus Features Implemented
- ✅ URL preview before generation
- ✅ Section-wise question grouping
- ✅ Dark/Light mode with system detection
- ✅ Raw HTML storage in database
- ✅ Comprehensive scoring system

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - High-performance web framework
- **SQLAlchemy** - ORM for database
- **BeautifulSoup4** - Web scraping
- **LangChain** - LLM integration
- **Google Gemini API** - AI quiz generation
- **PostgreSQL/SQLite** - Database

### Frontend
- **React 18.2**
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js 18+ and npm
- Google Gemini API Key ([Get one free](https://makersuite.google.com/app/apikey))
- PostgreSQL (optional, SQLite for development)

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd ai-quiz-generator
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your GEMINI_API_KEY
nano .env  # or use any text editor
```

**Add to `.env`:**
```env
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///./quiz_history.db
```

### 3. Frontend Setup

Open a new terminal:
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Start Backend

In the backend terminal:
```bash
cd backend
source venv/bin/activate  # if not already activated
python main.py
```

### 5. Access Application

- **Frontend:** http://localhost:3000
- **Backend API Docs:** http://localhost:8000/docs
- **Backend API:** http://localhost:8000

## 📝 Usage

1. **Generate Quiz:**
   - Enter a Wikipedia URL (e.g., `https://en.wikipedia.org/wiki/Python_(programming_language)`)
   - Click "Preview" to see article information
   - Click "Generate Quiz" to create the quiz
   - Wait 20-30 seconds for AI generation

2. **Take Quiz:**
   - Click "Take Quiz" button
   - Answer all questions
   - Click "Submit Quiz" to see your score
   - View detailed results with explanations

3. **View History:**
   - Click "Quiz History" tab
   - See all generated quizzes
   - Click "View Details" to see full quiz

4. **Dark Mode:**
   - Click the sun/moon toggle in header
   - Theme preference is saved automatically

## 🌐 API Endpoints

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/preview_url` | POST | Preview Wikipedia article |
| `/generate_quiz` | POST | Generate quiz from URL |
| `/submit_quiz` | POST | Submit quiz for scoring |
| `/history` | GET | Get all quiz history |
| `/quiz/{id}` | GET | Get specific quiz details |

### Example API Request:
```bash
curl -X POST http://localhost:8000/generate_quiz \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Artificial_intelligence"}'
```

## 🧪 Testing

### Manual Testing
1. Test with sample URLs:
   - https://en.wikipedia.org/wiki/Python_(programming_language)
   - https://en.wikipedia.org/wiki/Artificial_intelligence
   - https://en.wikipedia.org/wiki/Machine_learning

2. Test all features:
   - ✓ URL preview
   - ✓ Quiz generation
   - ✓ Caching (try same URL twice)
   - ✓ Quiz mode
   - ✓ Scoring
   - ✓ History
   - ✓ Dark mode

### API Testing
Use the interactive docs at http://localhost:8000/docs

## 🚀 Deployment

### Backend Deployment (Render)

1. Create account at https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     - `GEMINI_API_KEY`: Your API key
     - `DATABASE_URL`: Auto-provided by Render
5. Deploy

### Frontend Deployment (Vercel)

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `cd frontend && vercel`
3. Set environment variable:
   - `VITE_API_URL`: Your backend URL
4. Deploy: `vercel --prod`

## 📁 Project Structure
```
ai-quiz-generator/
├── backend/
│   ├── .env.example
│   ├── .gitignore
│   ├── requirements.txt
│   ├── database.py          # Database models
│   ├── models.py            # Pydantic schemas
│   ├── scraper.py           # Wikipedia scraper
│   ├── llm_quiz_generator.py # AI integration
│   ├── main.py              # FastAPI app
│   ├── Procfile             # Heroku config
│   └── runtime.txt          # Python version
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main component
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── .env.example
│   ├── .gitignore
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.cjs
│   ├── index.html
│   └── vercel.json
├── .gitignore
└── README.md
```

## 🐛 Troubleshooting

### Backend Issues

**Error: "GEMINI_API_KEY not found"**
- Add API key to `backend/.env`

**Error: "Database error"**
- Check `DATABASE_URL` in `.env`
- For SQLite: Use `sqlite:///./quiz_history.db`

**Error: "404 models/gemini-pro"**
- Model name is correct: `gemini-pro`
- Check API key is valid

### Frontend Issues

**Error: "Cannot connect to backend"**
- Ensure backend is running on port 8000
- Check `vite.config.js` proxy settings

**Error: "npm install fails"**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

## 🤝 Contributing

This is a project assignment for DeepKlarity Technologies.

## 📄 License

MIT License

## 👨‍💻 Author

**Your Name**
- GitHub: [@Thippeswamy K R](https://github.com/thippeswamykr1204)
- Email: thippeswamykr1204@gmail.com

---

**Project Assignment for DeepKlarity Technologies**

Last Updated: November 2024