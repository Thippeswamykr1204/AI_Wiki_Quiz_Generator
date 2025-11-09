import React, { useState } from 'react';
import { AlertCircle, Loader2, Eye, Book } from 'lucide-react';
import { generateQuiz, previewUrl } from '../services/api';
import QuizDisplay from './QuizDisplay';

const GenerateQuizTab = ({ quizData, setQuizData }) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState(null);
  const [previewing, setPreviewing] = useState(false);

  const handlePreview = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setPreviewing(true);
    setError('');
    setPreview(null);

    try {
      const data = await previewUrl(url);
      setPreview(data);
    } catch (err) {
      setError(err.message || 'Preview failed');
    } finally {
      setPreviewing(false);
    }
  };

  const handleGenerate = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setError('');
    setLoading(true);
    setQuizData(null);

    try {
      const data = await generateQuiz(url);
      setQuizData(data);
      setPreview(null);
    } catch (err) {
      setError(err.message || 'Failed to generate quiz');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Generate New Quiz
        </h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Wikipedia Article URL
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handlePreview()}
                placeholder="https://en.wikipedia.org/wiki/Artificial_intelligence"
                className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors"
                disabled={loading || previewing}
              />
              <button
                onClick={handlePreview}
                disabled={loading || previewing}
                className="px-4 py-3 bg-gray-600 dark:bg-gray-700 text-white rounded-lg hover:bg-gray-700 dark:hover:bg-gray-600 disabled:bg-gray-400 transition-colors flex items-center gap-2"
              >
                {previewing ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Eye className="w-5 h-5" />
                )}
                Preview
              </button>
            </div>
          </div>

          {preview && (
            <div className={`p-4 rounded-lg border-2 transition-colors ${
              preview.exists_in_db 
                ? 'border-yellow-300 bg-yellow-50 dark:border-yellow-700 dark:bg-yellow-900/20' 
                : 'border-green-300 bg-green-50 dark:border-green-700 dark:bg-green-900/20'
            }`}>
              <div className="flex items-start gap-4">
                {preview.image_url && (
                  <img 
                    src={preview.image_url} 
                    alt={preview.title}
                    className="w-20 h-20 object-cover rounded"
                  />
                )}
                <div className="flex-1">
                  <h3 className="font-bold text-lg text-gray-900 dark:text-white">{preview.title}</h3>
                  {preview.summary && (
                    <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">{preview.summary}</p>
                  )}
                  <div className="flex items-center gap-4 mt-2 text-sm text-gray-600 dark:text-gray-400">
                    {preview.word_count && (
                      <span>~{preview.word_count.toLocaleString()} words</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {error && (
            <div className="flex items-center gap-2 text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
              <AlertCircle className="w-5 h-5" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          <button
            onClick={handleGenerate}
            disabled={loading || previewing}
            className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400 transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating Quiz...
              </>
            ) : (
              <>
                <Book className="w-5 h-5" />
                Generate Quiz
              </>
            )}
          </button>
        </div>
      </div>

      {quizData && <QuizDisplay quiz={quizData} />}
    </div>
  );
};

export default GenerateQuizTab;