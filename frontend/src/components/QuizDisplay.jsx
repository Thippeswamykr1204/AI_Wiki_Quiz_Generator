import React, { useState, useMemo } from 'react';
import { ExternalLink, Book, Users, MapPin, Building2, Clock, Trophy, Award, Eye, FileCode, Loader2 } from 'lucide-react';
import { submitQuiz } from '../services/api';
import EntityCard from './EntityCard';
import QuestionCard from './QuestionCard';

const QuizDisplay = ({ quiz }) => {
  const [quizMode, setQuizMode] = useState(false);
  const [userAnswers, setUserAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [scoreData, setScoreData] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const groupedQuestions = useMemo(() => {
    const groups = {};
    quiz.quiz.forEach((q, idx) => {
      const section = q.section || 'General';
      if (!groups[section]) groups[section] = [];
      groups[section].push({ ...q, originalIndex: idx });
    });
    return groups;
  }, [quiz]);

  const handleStartQuiz = () => {
    setQuizMode(true);
    setStartTime(Date.now());
    setUserAnswers({});
    setShowResults(false);
    setScoreData(null);
  };

  const handleAnswerSelect = (idx, answer) => {
    if (!showResults) {
      setUserAnswers({ ...userAnswers, [idx]: answer });
    }
  };

  const handleSubmitQuiz = async () => {
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    setSubmitting(true);

    try {
      const formattedAnswers = {};
      Object.keys(userAnswers).forEach(key => {
        formattedAnswers[parseInt(key)] = userAnswers[key];
      });
      
      const score = await submitQuiz(quiz.id, formattedAnswers, timeTaken);
      setScoreData(score);
      setShowResults(true);
    } catch (err) {
      console.error('Quiz submission error:', err);
      alert('Failed to submit quiz: ' + (err.message || 'Unknown error'));
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetakeQuiz = () => {
    setUserAnswers({});
    setShowResults(false);
    setScoreData(null);
    setStartTime(Date.now());
  };

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white">{quiz.title}</h3>
              {quiz.is_cached && (
                <span className="px-2 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400 text-xs rounded-full">
                  Cached
                </span>
              )}
            </div>
            <a
              href={quiz.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 flex items-center gap-1 text-sm"
            >
              View Article <ExternalLink className="w-4 h-4" />
            </a>
          </div>
          <button
            onClick={() => quizMode ? setQuizMode(false) : handleStartQuiz()}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium flex items-center gap-2"
          >
            {quizMode ? (
              <>
                <Eye className="w-4 h-4" />
                View Details
              </>
            ) : (
              <>
                <Trophy className="w-4 h-4" />
                Take Quiz
              </>
            )}
          </button>
        </div>

        {!quizMode && (
          <>
            <p className="text-gray-700 dark:text-gray-300 mb-6">{quiz.summary}</p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <EntityCard icon={<Users className="w-5 h-5" />} title="People" items={quiz.key_entities.people} color="blue" />
              <EntityCard icon={<Building2 className="w-5 h-5" />} title="Organizations" items={quiz.key_entities.organizations} color="purple" />
              <EntityCard icon={<MapPin className="w-5 h-5" />} title="Locations" items={quiz.key_entities.locations} color="green" />
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
                <Book className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                Article Sections
              </h4>
              <div className="flex flex-wrap gap-2">
                {quiz.sections.map((section, idx) => (
                  <span key={idx} className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm">
                    {section}
                  </span>
                ))}
              </div>
            </div>
          </>
        )}
      </div>

      {quizMode ? (
        <div className="space-y-4">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <Trophy className="w-6 h-6 text-yellow-500" />
                Quiz Mode
              </h3>
              {showResults && scoreData && (
                <div className="text-right">
                  <div className="flex items-center gap-2">
                    <Award className="w-8 h-8 text-yellow-500" />
                    <div>
                      <p className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">
                        {scoreData.score_percentage.toFixed(0)}%
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {scoreData.correct_answers}/{scoreData.total_questions} correct
                      </p>
                    </div>
                  </div>
                  {scoreData.time_taken && (
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 flex items-center gap-1 justify-end">
                      <Clock className="w-3 h-3" />
                      {Math.floor(scoreData.time_taken / 60)}:{(scoreData.time_taken % 60).toString().padStart(2, '0')}
                    </p>
                  )}
                </div>
              )}
            </div>

            {Object.entries(groupedQuestions).map(([section, questions]) => (
              <div key={section} className="mb-8 last:mb-0">
                <h4 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 pb-2 border-b-2 border-indigo-200 dark:border-indigo-800 flex items-center gap-2">
                  <FileCode className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  {section}
                </h4>

                {questions.map((q) => (
                  <QuestionCard 
                    key={q.originalIndex}
                    question={q}
                    index={q.originalIndex}
                    quizMode={true}
                    onAnswerSelect={handleAnswerSelect}
                    showResults={showResults}
                    userAnswer={userAnswers[q.originalIndex]}
                  />
                ))}
              </div>
            ))}

            {!showResults ? (
              <button
                onClick={handleSubmitQuiz}
                disabled={Object.keys(userAnswers).length !== quiz.quiz.length || submitting}
                className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400 transition-colors flex items-center justify-center gap-2"
              >
                {submitting ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Submitting...
                  </>
                ) : (
                  <>
                    <Trophy className="w-5 h-5" />
                    Submit Quiz
                  </>
                )}
              </button>
            ) : (
              <button
                onClick={handleRetakeQuiz}
                className="w-full bg-gray-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-gray-700 transition-colors flex items-center justify-center gap-2"
              >
                <Trophy className="w-5 h-5" />
                Retake Quiz
              </button>
            )}
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {Object.entries(groupedQuestions).map(([section, questions]) => (
            <div key={section} className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <FileCode className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
                {section}
              </h3>
              <div className="space-y-4">
                {questions.map((q) => (
                  <QuestionCard key={q.originalIndex} question={q} index={q.originalIndex} />
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {!quizMode && quiz.related_topics && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors">
          <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Related Topics</h4>
          <div className="flex flex-wrap gap-2">
            {quiz.related_topics.map((topic, idx) => (
              <span
                key={idx}
                className="px-4 py-2 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 rounded-lg text-sm font-medium hover:bg-indigo-200 dark:hover:bg-indigo-900/50 transition-colors cursor-pointer"
              >
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default QuizDisplay;