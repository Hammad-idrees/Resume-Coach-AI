import { useState, useRef, useEffect } from 'react';
import { 
  MessageCircle, Send, Play, BarChart3, CheckCircle, 
  Clock, Award, Sparkles 
} from 'lucide-react';
import { interviewApi } from '../lib/api';
import type { 
  InterviewQuestion, 
  InterviewMessage,
  InterviewScoreResponse 
} from '../types/interview';

const InterviewSimulation = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [jobRole, setJobRole] = useState('');
  const [numQuestions, setNumQuestions] = useState(5);
  
  const [interviewStarted, setInterviewStarted] = useState(false);
  const [questions, setQuestions] = useState<InterviewQuestion[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [messages, setMessages] = useState<InterviewMessage[]>([]);
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [isGeneratingQuestions, setIsGeneratingQuestions] = useState(false);
  
  const [interviewCompleted, setInterviewCompleted] = useState(false);
  const [finalScore, setFinalScore] = useState<InterviewScoreResponse | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const answerInputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startInterview = async () => {
    if (!jobDescription.trim()) {
      alert('Please enter a job description');
      return;
    }

    setIsGeneratingQuestions(true);

    try {
      const response = await interviewApi.generateQuestions({
        job_description: jobDescription,
        job_role: jobRole || undefined,
        num_questions: numQuestions,
      });

      const generatedQuestions = response.data.questions;
      setQuestions(generatedQuestions);
      setInterviewStarted(true);
      setCurrentQuestionIndex(0);

      // Add welcome message and first question
      const welcomeMessage: InterviewMessage = {
        id: Date.now(),
        role: 'assistant',
        content: `Welcome to your interview simulation! I'll be asking you ${generatedQuestions.length} questions. Take your time to provide thoughtful answers. Let's begin!`,
        timestamp: new Date(),
      };

      const firstQuestionMessage: InterviewMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: generatedQuestions[0].question,
        timestamp: new Date(),
        question: generatedQuestions[0],
      };

      setMessages([welcomeMessage, firstQuestionMessage]);
    } catch (error: any) {
      console.error('Error generating questions:', error);
      alert(error.response?.data?.detail || 'Failed to generate interview questions. Please try again.');
    } finally {
      setIsGeneratingQuestions(false);
    }
  };

  const submitAnswer = async () => {
    if (!currentAnswer.trim()) {
      alert('Please provide an answer');
      return;
    }

    const currentQuestion = questions[currentQuestionIndex];
    
    // Add user's answer to messages
    const userMessage: InterviewMessage = {
      id: Date.now(),
      role: 'user',
      content: currentAnswer,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentAnswer('');
    setIsEvaluating(true);

    try {
      // Evaluate the answer
      const evaluationResponse = await interviewApi.evaluateAnswer({
        question: currentQuestion.question,
        answer: currentAnswer,
        category: currentQuestion.category,
        difficulty: currentQuestion.difficulty,
      });

      const evaluation = evaluationResponse.data;

      // Add evaluation feedback
      const feedbackMessage: InterviewMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Score: ${evaluation.score}/10\n\n${evaluation.overall_feedback}`,
        timestamp: new Date(),
        evaluation: evaluation,
      };

      setMessages(prev => [...prev, feedbackMessage]);

      // Move to next question or complete interview
      if (currentQuestionIndex < questions.length - 1) {
        const nextQuestionIndex = currentQuestionIndex + 1;
        setCurrentQuestionIndex(nextQuestionIndex);

        setTimeout(() => {
          const nextQuestionMessage: InterviewMessage = {
            id: Date.now() + 2,
            role: 'assistant',
            content: questions[nextQuestionIndex].question,
            timestamp: new Date(),
            question: questions[nextQuestionIndex],
          };

          setMessages(prev => [...prev, nextQuestionMessage]);
        }, 1000);
      } else {
        // Interview completed - calculate final score
        completeInterview();
      }
    } catch (error: any) {
      console.error('Error evaluating answer:', error);
      alert(error.response?.data?.detail || 'Failed to evaluate answer. Please try again.');
    } finally {
      setIsEvaluating(false);
    }
  };

  const completeInterview = async () => {
    // Collect all evaluations
    const evaluations = messages
      .filter(msg => msg.evaluation)
      .map(msg => ({
        score: msg.evaluation!.score,
        category: msg.question?.category || 'General',
      }));

    try {
      const scoreResponse = await interviewApi.calculateScore({ evaluations });
      const finalScoreData = scoreResponse.data;

      setFinalScore(finalScoreData);
      setInterviewCompleted(true);

      // Add completion message
      const completionMessage: InterviewMessage = {
        id: Date.now() + 3,
        role: 'assistant',
        content: `🎉 Interview completed! Your overall score is ${finalScoreData.overall_score.toFixed(1)}/100 (Grade: ${finalScoreData.grade})`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, completionMessage]);
    } catch (error: any) {
      console.error('Error calculating final score:', error);
      alert('Failed to calculate final score');
    }
  };

  const resetInterview = () => {
    setInterviewStarted(false);
    setQuestions([]);
    setMessages([]);
    setCurrentQuestionIndex(0);
    setCurrentAnswer('');
    setInterviewCompleted(false);
    setFinalScore(null);
    setJobDescription('');
    setJobRole('');
    setNumQuestions(5);
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getGradeColor = (grade: string) => {
    if (grade.startsWith('A')) return 'text-green-600 bg-green-50';
    if (grade.startsWith('B')) return 'text-blue-600 bg-blue-50';
    if (grade.startsWith('C')) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 p-3 md:p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-lg p-4 md:p-6 mb-4 md:mb-6">
          <div className="flex items-center space-x-2 md:space-x-3 mb-2">
            <MessageCircle className="w-6 h-6 md:w-8 md:h-8 text-purple-600" />
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">Interview Simulation</h1>
          </div>
          <p className="text-sm md:text-base text-gray-600">
            Practice your interview skills with AI-powered evaluation and real-time feedback
          </p>
        </div>

        {!interviewStarted ? (
          /* Setup Screen */
          <div className="bg-white rounded-xl shadow-lg p-4 md:p-8">
            <h2 className="text-xl md:text-2xl font-bold text-gray-800 mb-4 md:mb-6 flex items-center">
              <Play className="w-5 h-5 md:w-6 md:h-6 text-purple-600 mr-2" />
              Start Your Interview
            </h2>

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Job Description *
                </label>
                <textarea
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  className="w-full h-40 p-4 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all resize-none"
                  placeholder="Paste the job description here... (e.g., 'Senior Software Engineer with 5+ years experience in Python, React, AWS...')"
                />
                <p className="text-sm text-gray-500 mt-1">
                  {jobDescription.length} characters
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Job Role (Optional)
                  </label>
                  <input
                    type="text"
                    value={jobRole}
                    onChange={(e) => setJobRole(e.target.value)}
                    className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
                    placeholder="e.g., Software Engineer, Data Scientist"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Number of Questions
                  </label>
                  <select
                    value={numQuestions}
                    onChange={(e) => setNumQuestions(Number(e.target.value))}
                    className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
                  >
                    <option value={3}>3 Questions (Quick)</option>
                    <option value={5}>5 Questions (Standard)</option>
                    <option value={7}>7 Questions (Comprehensive)</option>
                    <option value={10}>10 Questions (Full Interview)</option>
                  </select>
                </div>
              </div>

              <button
                onClick={startInterview}
                disabled={isGeneratingQuestions || !jobDescription.trim()}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                {isGeneratingQuestions ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                    <span>Generating Questions...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    <span>Start Interview</span>
                  </>
                )}
              </button>
            </div>
          </div>
        ) : (
          /* Interview Screen */
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Chat Area */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col" style={{ height: '600px' }}>
                {/* Progress Bar */}
                <div className="bg-purple-50 border-b border-purple-100 p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-purple-800">
                      Question {currentQuestionIndex + 1} of {questions.length}
                    </span>
                    <span className="text-sm text-purple-600">
                      {Math.round(((currentQuestionIndex + 1) / questions.length) * 100)}% Complete
                    </span>
                  </div>
                  <div className="w-full bg-purple-200 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-purple-600 to-blue-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
                    />
                  </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-2xl p-4 ${
                          message.role === 'user'
                            ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                            : 'bg-white border-2 border-gray-200 text-gray-800 shadow-sm'
                        }`}
                      >
                        {message.question && (
                          <div className="mb-2">
                            <span className="inline-block px-3 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded-full">
                              {message.question.category}
                            </span>
                          </div>
                        )}
                        <p className="whitespace-pre-wrap">{message.content}</p>
                        
                        {message.evaluation && (
                          <div className="mt-4 pt-4 border-t border-gray-200">
                            <div className="grid grid-cols-2 gap-2 mb-3">
                              <div className="bg-purple-50 p-2 rounded">
                                <p className="text-xs text-purple-600 font-semibold">Word Count</p>
                                <p className="text-lg font-bold text-purple-800">{message.evaluation.word_count}</p>
                              </div>
                              <div className="bg-blue-50 p-2 rounded">
                                <p className="text-xs text-blue-600 font-semibold">Sentiment</p>
                                <p className="text-sm font-bold text-blue-800 capitalize">{message.evaluation.sentiment}</p>
                              </div>
                            </div>
                            
                            {message.evaluation.strengths.length > 0 && (
                              <div className="mb-2">
                                <p className="text-xs font-semibold text-green-700 mb-1">✓ Strengths:</p>
                                <ul className="text-xs text-gray-700 space-y-1">
                                  {message.evaluation.strengths.map((strength, idx) => (
                                    <li key={idx}>• {strength}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            
                            {message.evaluation.improvements.length > 0 && (
                              <div>
                                <p className="text-xs font-semibold text-orange-700 mb-1">💡 Improvements:</p>
                                <ul className="text-xs text-gray-700 space-y-1">
                                  {message.evaluation.improvements.map((improvement, idx) => (
                                    <li key={idx}>• {improvement}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                {!interviewCompleted && (
                  <div className="border-t border-gray-200 p-4 bg-white">
                    <div className="flex space-x-3">
                      <textarea
                        ref={answerInputRef}
                        value={currentAnswer}
                        onChange={(e) => setCurrentAnswer(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' && e.ctrlKey) {
                            submitAnswer();
                          }
                        }}
                        disabled={isEvaluating}
                        className="flex-1 p-3 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all resize-none"
                        placeholder="Type your answer here... (Ctrl+Enter to submit)"
                        rows={3}
                      />
                      <button
                        onClick={submitAnswer}
                        disabled={isEvaluating || !currentAnswer.trim()}
                        className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                      >
                        {isEvaluating ? (
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                        ) : (
                          <Send className="w-5 h-5" />
                        )}
                      </button>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">
                      {currentAnswer.length} characters • Press Ctrl+Enter to submit
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Sidebar - Progress & Stats */}
            <div className="space-y-6">
              {/* Current Question Info */}
              {questions[currentQuestionIndex] && !interviewCompleted && (
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                    <Clock className="w-5 h-5 text-purple-600 mr-2" />
                    Current Question
                  </h3>
                  <div className="space-y-3">
                    <div>
                      <p className="text-xs text-gray-500 font-semibold">Category</p>
                      <p className="text-sm font-bold text-purple-600">{questions[currentQuestionIndex].category}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 font-semibold">Difficulty</p>
                      <p className="text-sm font-bold text-blue-600 capitalize">{questions[currentQuestionIndex].difficulty}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Questions List */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                  <BarChart3 className="w-5 h-5 text-purple-600 mr-2" />
                  Questions
                </h3>
                <div className="space-y-2">
                  {questions.map((q, idx) => {
                    const answered = idx < currentQuestionIndex || (idx === currentQuestionIndex && interviewCompleted);
                    const current = idx === currentQuestionIndex && !interviewCompleted;
                    
                    return (
                      <div
                        key={q.id}
                        className={`p-3 rounded-lg border-2 ${
                          current
                            ? 'border-purple-600 bg-purple-50'
                            : answered
                            ? 'border-green-300 bg-green-50'
                            : 'border-gray-200 bg-gray-50'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-semibold text-gray-700">
                            Q{idx + 1}: {q.category}
                          </span>
                          {answered && <CheckCircle className="w-4 h-4 text-green-600" />}
                          {current && <Clock className="w-4 h-4 text-purple-600 animate-pulse" />}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Final Score Card */}
              {interviewCompleted && finalScore && (
                <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl shadow-lg p-6 border-2 border-purple-200">
                  <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                    <Award className="w-5 h-5 text-purple-600 mr-2" />
                    Final Results
                  </h3>
                  
                  <div className="bg-white rounded-lg p-4 mb-4 text-center">
                    <p className="text-sm text-gray-600 mb-1">Overall Score</p>
                    <p className="text-5xl font-bold text-purple-600 mb-2">
                      {finalScore.overall_score.toFixed(1)}
                    </p>
                    <div className={`inline-block px-4 py-2 rounded-full font-bold text-lg ${getGradeColor(finalScore.grade)}`}>
                      Grade: {finalScore.grade}
                    </div>
                  </div>

                  <div className="space-y-3 mb-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Avg per Question:</span>
                      <span className="font-bold text-gray-800">{finalScore.average_score.toFixed(1)}/10</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Questions Answered:</span>
                      <span className="font-bold text-gray-800">{finalScore.questions_answered}/{finalScore.total_questions}</span>
                    </div>
                  </div>

                  <p className="text-sm text-gray-700 bg-white rounded-lg p-3 mb-4">
                    {finalScore.summary}
                  </p>

                  <div className="bg-white rounded-lg p-3">
                    <p className="text-xs font-semibold text-gray-700 mb-2">Category Breakdown:</p>
                    <div className="space-y-2">
                      {Object.entries(finalScore.category_breakdown).map(([category, score]) => (
                        <div key={category} className="flex justify-between items-center">
                          <span className="text-xs text-gray-600">{category}:</span>
                          <span className={`text-sm font-bold ${getScoreColor(score)}`}>
                            {score.toFixed(1)}/10
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <button
                    onClick={resetInterview}
                    className="w-full mt-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all flex items-center justify-center space-x-2"
                  >
                    <Sparkles className="w-4 h-4" />
                    <span>Start New Interview</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default InterviewSimulation;
