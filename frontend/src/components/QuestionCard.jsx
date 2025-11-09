import React, { useState } from 'react';
import { CheckCircle, XCircle } from 'lucide-react';

const QuestionCard = ({ question, index, quizMode = false, onAnswerSelect, showResults = false, userAnswer = null }) => {
  const [showAnswer, setShowAnswer] = useState(false);

  const isSelected = userAnswer === question.answer;
  const isCorrect = question.answer === userAnswer;
  const showCorrect = showResults && question.answer === question.answer && isCorrect;
  const showIncorrect = showResults && userAnswer && !isCorrect;

  if (quizMode) {
    return (
      <div className="mb-6 pb-6 border-b dark:border-gray-700 last:border-b-0">
        <div className="flex items-start justify-between mb-3">
          <h5 className="font-semibold text-gray-900 dark:text-white flex-1">
            Q{index + 1}. {question.question}
          </h5>
          <span className={`px-2 py-1 rounded text-xs font-medium whitespace-nowrap ml-2 ${
            question.difficulty === 'easy' ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400' :
            question.difficulty === 'medium' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400' :
            'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-400'
          }`}>
            {question.difficulty}
          </span>
        </div>

        <div className="space-y-2">
          {question.options.map((option, optIdx) => {
            const selected = userAnswer === option;
            const correct = option === question.answer;
            const shouldShowCorrect = showResults && correct;
            const shouldShowIncorrect = showResults && selected && !correct;

            return (
              <button
                key={optIdx}
                onClick={() => onAnswerSelect && onAnswerSelect(index, option)}
                disabled={showResults}
                className={`w-full text-left px-4 py-3 rounded-lg border-2 transition-all ${
                  shouldShowCorrect ? 'border-green-500 bg-green-50 dark:bg-green-900/20' :
                  shouldShowIncorrect ? 'border-red-500 bg-red-50 dark:bg-red-900/20' :
                  selected ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20' :
                  'border-gray-200 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-600 bg-white dark:bg-gray-800'
                } ${showResults ? 'cursor-default' : 'cursor-pointer'}`}
              >
                <div className="flex items-center justify-between">
                  <span className="flex items-center gap-2 text-gray-900 dark:text-white">
                    <span className="font-medium">{String.fromCharCode(65 + optIdx)}.</span>
                    {option}
                  </span>
                  {shouldShowCorrect && <CheckCircle className="w-5 h-5 text-green-600" />}
                  {shouldShowIncorrect && <XCircle className="w-5 h-5 text-red-600" />}
                </div>
              </button>
            );
          })}
        </div>

        {showResults && (
          <div className="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <p className="text-sm text-blue-900 dark:text-blue-300">
              <strong>Explanation:</strong> {question.explanation}
            </p>
          </div>
        )}
      </div>
    );
  }

  // View mode
  return (
    <div className="border-2 border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-indigo-300 dark:hover:border-indigo-600 transition-colors bg-white dark:bg-gray-800">
      <div className="flex items-start justify-between mb-3">
        <h5 className="font-semibold text-gray-900 dark:text-white flex-1">
          {index + 1}. {question.question}
        </h5>
        <span className={`px-2 py-1 rounded text-xs font-medium whitespace-nowrap ml-2 ${
          question.difficulty === 'easy' ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400' :
          question.difficulty === 'medium' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400' :
          'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-400'
        }`}>
          {question.difficulty}
        </span>
      </div>

      <div className="space-y-2 mb-3">
        {question.options.map((opt, idx) => (
          <div
            key={idx}
            className={`p-2 rounded border transition-colors ${
              showAnswer && opt === question.answer
                ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                : 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/20'
            }`}
          >
            <span className="font-medium mr-2 text-gray-900 dark:text-white">{String.fromCharCode(65 + idx)}.</span>
            <span className="text-gray-900 dark:text-white">{opt}</span>
          </div>
        ))}
      </div>

      <button
        onClick={() => setShowAnswer(!showAnswer)}
        className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 text-sm font-medium transition-colors"
      >
        {showAnswer ? 'Hide' : 'Show'} Answer
      </button>

      {showAnswer && (
        <div className="mt-3 p-3 bg-indigo-50 dark:bg-indigo-900/20 rounded transition-colors">
          <p className="text-sm text-indigo-900 dark:text-indigo-300">
            <strong>Answer:</strong> {question.answer}
          </p>
          <p className="text-sm text-indigo-900 dark:text-indigo-300 mt-1">
            <strong>Explanation:</strong> {question.explanation}
          </p>
        </div>
      )}
    </div>
  );
};

export default QuestionCard;