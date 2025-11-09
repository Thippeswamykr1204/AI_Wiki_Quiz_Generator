import React, { useState } from 'react';
import { Trophy, Moon, Sun } from 'lucide-react';
import { useTheme } from './hooks/useTheme';
import GenerateQuizTab from './components/GenerateQuizTab';
import HistoryTab from './components/HistoryTab';
import QuizModal from './components/QuizModal';

const App = () => {
  const { theme, toggleTheme } = useTheme();
  const [activeTab, setActiveTab] = useState('generate');
  const [quizData, setQuizData] = useState(null);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 transition-colors">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-md transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                DeepKlarity AI Quiz Generator
              </h1>
              <p className="text-gray-600 dark:text-gray-300 mt-1 flex items-center gap-2">
                <Trophy className="w-4 h-4 text-yellow-500" />
                Transform Wikipedia articles into engaging quizzes
              </p>
            </div>
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? (
                <Sun className="w-5 h-5 text-yellow-400" />
              ) : (
                <Moon className="w-5 h-5 text-gray-700" />
              )}
            </button>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-1 inline-flex transition-colors">
          <button
            onClick={() => setActiveTab('generate')}
            className={`px-6 py-3 rounded-md font-medium transition-all ${
              activeTab === 'generate'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            Generate Quiz
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-6 py-3 rounded-md font-medium transition-all ${
              activeTab === 'history'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            Quiz History
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'generate' ? (
          <GenerateQuizTab quizData={quizData} setQuizData={setQuizData} />
        ) : (
          <HistoryTab setSelectedQuiz={setSelectedQuiz} setShowModal={setShowModal} />
        )}
      </div>

      {/* Quiz Modal */}
      {showModal && selectedQuiz && (
        <QuizModal
          quiz={selectedQuiz}
          onClose={() => {
            setShowModal(false);
            setSelectedQuiz(null);
          }}
        />
      )}
    </div>
  );
};

export default App;