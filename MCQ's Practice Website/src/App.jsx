import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  BookOpen,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Timer,
  RotateCcw,
  Bookmark,
  Sparkles,
  Filter,
  Search,
  Award,
  BarChart3,
  Layers,
  Cpu,
  Database,
  ChevronRight,
  ChevronLeft,
  HelpCircle,
  Check,
  X,
  Flame,
  Sun,
  Moon,
  Eye,
  Shuffle,
  FileText,
  Zap,
  ArrowRight,
  Flag,
  ListFilter,
  Clock,
  ExternalLink,
  Share2,
  CheckSquare,
  Square,
  ChevronDown
} from 'lucide-react';

import { QUESTION_BANK } from './data/questions.js';
import { CATEGORIES } from './data/categories.js';
import { CHEAT_SHEET_ITEMS } from './data/cheatsheet.js';

export default function App() {
  // Navigation & UI state
  const [mode, setMode] = useState('practice'); // 'practice' | 'exam' | 'flashcards' | 'cheatsheet'
  const [selectedCategory, setSelectedCategory] = useState("All Topics");
  const [searchQuery, setSearchQuery] = useState("");
  const [bookmarkedIds, setBookmarkedIds] = useState(() => {
    try {
      const saved = localStorage.getItem('de_mcq_bookmarks');
      return saved ? new Set(JSON.parse(saved)) : new Set();
    } catch {
      return new Set();
    }
  });
  const [showOnlyBookmarks, setShowOnlyBookmarks] = useState(false);
  const [showOnlyMissed, setShowOnlyMissed] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    try {
      const saved = localStorage.getItem('de_mcq_dark_mode');
      return saved !== null ? JSON.parse(saved) : true;
    } catch {
      return true;
    }
  });

  // Save bookmarks & theme to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('de_mcq_bookmarks', JSON.stringify(Array.from(bookmarkedIds)));
    } catch (e) {
      console.error(e);
    }
  }, [bookmarkedIds]);

  useEffect(() => {
    try {
      localStorage.setItem('de_mcq_dark_mode', JSON.stringify(darkMode));
    } catch (e) {
      console.error(e);
    }
  }, [darkMode]);

  // Practice Mode state
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({}); // { [qId]: selectedOptionIndex }
  const [showExplanation, setShowExplanation] = useState({}); // { [qId]: boolean }

  // Exam Simulator state
  const [examStarted, setExamStarted] = useState(false);
  const [examFinished, setExamFinished] = useState(false);
  const [examQuestions, setExamQuestions] = useState([]);
  const [examAnswers, setExamAnswers] = useState({});
  const [markedForReview, setMarkedForReview] = useState(new Set());
  const [examTimeLeft, setExamTimeLeft] = useState(1800);
  const [examQuestionCount, setExamQuestionCount] = useState(200); // Default to all 200 questions
  const [examCurrentIdx, setExamCurrentIdx] = useState(0);
  const [examNavFilter, setExamNavFilter] = useState('all'); // 'all' | 'unanswered' | 'flagged'
  const [examReviewFilter, setExamReviewFilter] = useState('all'); // 'all' | 'incorrect' | 'flagged'

  // Flashcards state
  const [flashcardIdx, setFlashcardIdx] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  // Custom Category Dropdown state
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Question Card Ref for auto-scrolling
  const questionCardRef = useRef(null);

  // Category question count map
  const categoryCountMap = useMemo(() => {
    const counts = { "All Topics": QUESTION_BANK.length };
    QUESTION_BANK.forEach((q) => {
      counts[q.category] = (counts[q.category] || 0) + 1;
    });
    return counts;
  }, []);

  // Close custom dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Filtering questions for Practice Mode
  const filteredQuestions = useMemo(() => {
    return QUESTION_BANK.filter((q) => {
      const matchesCategory = selectedCategory === "All Topics" || q.category === selectedCategory;
      const matchesSearch =
        searchQuery.trim() === "" ||
        q.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
        q.topic.toLowerCase().includes(searchQuery.toLowerCase()) ||
        q.options.some((opt) => opt.toLowerCase().includes(searchQuery.toLowerCase()));
      const matchesBookmark = !showOnlyBookmarks || bookmarkedIds.has(q.id);
      const isIncorrect = userAnswers[q.id] !== undefined && userAnswers[q.id] !== q.correct;
      const matchesMissed = !showOnlyMissed || isIncorrect;

      return matchesCategory && matchesSearch && matchesBookmark && matchesMissed;
    });
  }, [selectedCategory, searchQuery, showOnlyBookmarks, showOnlyMissed, bookmarkedIds, userAnswers]);

  // Safe bounds check when filter changes
  useEffect(() => {
    if (filteredQuestions.length > 0 && currentIndex >= filteredQuestions.length) {
      setCurrentIndex(0);
    }
  }, [filteredQuestions.length, currentIndex]);

  // Handle bookmark toggle
  const toggleBookmark = (id) => {
    setBookmarkedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Avoid capturing shortcuts if user is typing in search input
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
        return;
      }

      if (mode === 'practice' && filteredQuestions.length > 0) {
        const q = filteredQuestions[currentIndex];
        if (!q) return;
        if (e.key >= '1' && e.key <= '4') {
          handleSelectOption(q.id, parseInt(e.key, 10) - 1);
        } else if (e.key.toLowerCase() === 'a') handleSelectOption(q.id, 0);
        else if (e.key.toLowerCase() === 'b') handleSelectOption(q.id, 1);
        else if (e.key.toLowerCase() === 'c') handleSelectOption(q.id, 2);
        else if (e.key.toLowerCase() === 'd') handleSelectOption(q.id, 3);
        else if (e.key === 'ArrowRight') handleNext();
        else if (e.key === 'ArrowLeft') handlePrev();
        else if (e.key.toLowerCase() === 's') toggleBookmark(q.id);
        else if (e.key.toLowerCase() === 'e') {
          setShowExplanation((prev) => ({ ...prev, [q.id]: !prev[q.id] }));
        }
      } else if (mode === 'exam' && examStarted && !examFinished && examQuestions.length > 0) {
        const q = examQuestions[examCurrentIdx];
        if (!q) return;
        if (e.key >= '1' && e.key <= '4') {
          handleExamSelect(q.id, parseInt(e.key, 10) - 1);
        } else if (e.key.toLowerCase() === 'a') handleExamSelect(q.id, 0);
        else if (e.key.toLowerCase() === 'b') handleExamSelect(q.id, 1);
        else if (e.key.toLowerCase() === 'c') handleExamSelect(q.id, 2);
        else if (e.key.toLowerCase() === 'd') handleExamSelect(q.id, 3);
        else if (e.key.toLowerCase() === 'f') toggleReviewMark(q.id);
        else if (e.key === 'ArrowRight') {
          setExamCurrentIdx((prev) => Math.min(examQuestions.length - 1, prev + 1));
        } else if (e.key === 'ArrowLeft') {
          setExamCurrentIdx((prev) => Math.max(0, prev - 1));
        }
      } else if (mode === 'flashcards') {
        if (e.key === ' ' || e.key === 'Enter') {
          e.preventDefault();
          setIsFlipped((prev) => !prev);
        } else if (e.key === 'ArrowRight') {
          setIsFlipped(false);
          setFlashcardIdx((prev) => Math.min(QUESTION_BANK.length - 1, prev + 1));
        } else if (e.key === 'ArrowLeft') {
          setIsFlipped(false);
          setFlashcardIdx((prev) => Math.max(0, prev - 1));
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [mode, currentIndex, filteredQuestions, isFlipped, examStarted, examFinished, examQuestions, examCurrentIdx]);

  // Exam Timer countdown
  useEffect(() => {
    let timer;
    if (examStarted && !examFinished && examTimeLeft > 0) {
      timer = setInterval(() => {
        setExamTimeLeft((prev) => {
          if (prev <= 1) {
            clearInterval(timer);
            setExamFinished(true);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [examStarted, examFinished, examTimeLeft]);

  // Format seconds to H:MM:SS or MM:SS
  const formatTime = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    if (hrs > 0) {
      return `${hrs}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  // Start Exam with configurable question count
  const startExam = (count) => {
    const totalCount = count === 'all' || count >= QUESTION_BANK.length ? QUESTION_BANK.length : count;
    // Shuffle question bank
    const shuffled = [...QUESTION_BANK].sort(() => 0.5 - Math.random());
    const selected = shuffled.slice(0, totalCount);

    setExamQuestions(selected);
    setExamQuestionCount(totalCount);
    setExamAnswers({});
    setMarkedForReview(new Set());
    setExamTimeLeft(totalCount * 60); // 1 min per question
    setExamCurrentIdx(0);
    setExamStarted(true);
    setExamFinished(false);
  };

  const handleSelectOption = (qId, optionIdx) => {
    setUserAnswers((prev) => ({ ...prev, [qId]: optionIdx }));
    setShowExplanation((prev) => ({ ...prev, [qId]: true }));
  };

  const handleExamSelect = (qId, optionIdx) => {
    setExamAnswers((prev) => ({ ...prev, [qId]: optionIdx }));
  };

  const toggleReviewMark = (qId) => {
    setMarkedForReview((prev) => {
      const next = new Set(prev);
      if (next.has(qId)) next.delete(qId);
      else next.add(qId);
      return next;
    });
  };

  const handleNext = () => {
    if (currentIndex < filteredQuestions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  // Statistics calculation for Practice Mode
  const totalAnswered = Object.keys(userAnswers).length;
  const totalCorrect = Object.entries(userAnswers).filter(
    ([id, ans]) => QUESTION_BANK.find((q) => q.id === id)?.correct === ans
  ).length;
  const totalIncorrect = totalAnswered - totalCorrect;
  const overallAccuracy = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;

  // Exam Score calculation
  const examScore = useMemo(() => {
    if (!examFinished || examQuestions.length === 0) {
      return { correct: 0, total: 0, percentage: 0, categoryStats: {} };
    }
    let correct = 0;
    const catStats = {};

    examQuestions.forEach((q) => {
      if (!catStats[q.category]) catStats[q.category] = { total: 0, correct: 0 };
      catStats[q.category].total += 1;

      if (examAnswers[q.id] === q.correct) {
        correct += 1;
        catStats[q.category].correct += 1;
      }
    });

    return {
      correct,
      total: examQuestions.length,
      percentage: Math.round((correct / examQuestions.length) * 100),
      categoryStats: catStats
    };
  }, [examFinished, examQuestions, examAnswers]);

  // Exam Review Filtered List
  const examReviewQuestions = useMemo(() => {
    if (!examFinished) return [];
    return examQuestions.filter((q) => {
      const isIncorrect = examAnswers[q.id] !== q.correct;
      const isFlagged = markedForReview.has(q.id);
      if (examReviewFilter === 'incorrect') return isIncorrect;
      if (examReviewFilter === 'flagged') return isFlagged;
      return true;
    });
  }, [examFinished, examQuestions, examAnswers, markedForReview, examReviewFilter]);

  const currentQ = filteredQuestions[currentIndex] || filteredQuestions[0];

  return (
    <div className={`min-h-screen font-sans ${darkMode ? 'bg-slate-950 text-slate-100' : 'bg-slate-100/70 text-slate-900'} transition-colors duration-200`}>
      {/* HEADER NAVBAR */}
      <header className={`sticky top-0 z-40 border-b backdrop-blur-md ${darkMode ? 'bg-slate-950/90 border-slate-800/80 shadow-slate-950/50' : 'bg-white/95 border-slate-200 shadow-sm'} px-4 py-3`}>
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 via-blue-600 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/25">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className={`text-base sm:text-lg font-black tracking-tight ${
                  darkMode
                    ? 'bg-gradient-to-r from-indigo-400 via-cyan-300 to-white bg-clip-text text-transparent'
                    : 'text-slate-900'
                }`}>
                  SQL & Data Engineering Exam Master
                </h1>
                <span className={`text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full ${
                  darkMode
                    ? 'bg-cyan-500/20 border border-cyan-500/30 text-cyan-300'
                    : 'bg-indigo-100 border border-indigo-200 text-indigo-800 font-bold'
                }`}>
                  200 MCQs
                </span>
              </div>
              <p className={`text-[11px] ${darkMode ? 'text-slate-400' : 'text-slate-600'} hidden sm:block font-medium`}>
                SQL • Kimball Dimensional Modeling • SCD Types • Cloud Warehouses • Normalization • Python
              </p>
            </div>
          </div>

          {/* Navigation Mode Tabs */}
          <div className={`flex items-center p-1 rounded-2xl gap-1 ${darkMode ? 'bg-slate-900 border border-slate-800' : 'bg-slate-100 border border-slate-300/80 shadow-inner'}`}>
            <button
              onClick={() => setMode('practice')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                mode === 'practice'
                  ? darkMode
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'bg-white text-indigo-700 shadow-sm border border-slate-200'
                  : darkMode
                  ? 'text-slate-400 hover:text-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Practice & Learn</span>
            </button>
            <button
              onClick={() => setMode('exam')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                mode === 'exam'
                  ? darkMode
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'bg-white text-indigo-700 shadow-sm border border-slate-200'
                  : darkMode
                  ? 'text-slate-400 hover:text-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Timer className="w-3.5 h-3.5" />
              <span>Exam Simulator</span>
            </button>
            <button
              onClick={() => setMode('flashcards')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                mode === 'flashcards'
                  ? darkMode
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'bg-white text-indigo-700 shadow-sm border border-slate-200'
                  : darkMode
                  ? 'text-slate-400 hover:text-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Zap className="w-3.5 h-3.5" />
              <span>Flashcards</span>
            </button>
            <button
              onClick={() => setMode('cheatsheet')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                mode === 'cheatsheet'
                  ? darkMode
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'bg-white text-indigo-700 shadow-sm border border-slate-200'
                  : darkMode
                  ? 'text-slate-400 hover:text-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Cheat Sheet</span>
            </button>
          </div>

          {/* Quick Stats & Theme Toggle */}
          <div className="flex items-center gap-3">
            <div className={`hidden md:flex items-center gap-2 px-3 py-1 rounded-full border ${
              darkMode
                ? 'bg-indigo-950/40 border-indigo-800/60 text-indigo-300'
                : 'bg-indigo-50 border-indigo-200 text-indigo-900 shadow-sm'
            }`}>
              <Flame className="w-4 h-4 text-amber-500" />
              <span className="text-xs font-bold">
                Accuracy: {totalCorrect}/{totalAnswered} ({overallAccuracy}%)
              </span>
            </div>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`p-2 rounded-xl border transition ${
                darkMode
                  ? 'bg-slate-900 border-slate-800 text-amber-400 hover:bg-slate-800 shadow-sm'
                  : 'bg-white border-slate-300 text-indigo-600 hover:bg-slate-50 shadow-sm'
              }`}
              title="Toggle Dark / Light Mode"
            >
              {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </header>

      {/* MAIN CONTENT AREA */}
      <main className="max-w-7xl mx-auto p-4 sm:p-6">
        {/* =========================================
            MODE 1: PRACTICE & LEARN MODE
            ========================================= */}
        {mode === 'practice' && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Sidebar Controls & Question Palette */}
            <div className="lg:col-span-1 space-y-4">
              {/* Filter Panel */}
              <div className={`p-4 rounded-3xl border ${darkMode ? 'bg-slate-900/90 border-slate-800' : 'bg-white border-slate-200 shadow-sm'} space-y-3`}>
                <div className="flex items-center justify-between">
                  <h3 className={`text-xs font-black uppercase tracking-wider flex items-center gap-2 ${darkMode ? 'text-indigo-400' : 'text-indigo-700'}`}>
                    <Filter className="w-4 h-4" /> Filters & Search
                  </h3>
                  <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
                    darkMode
                      ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30'
                      : 'bg-indigo-50 text-indigo-800 border-indigo-200'
                  }`}>
                    {filteredQuestions.length} / {QUESTION_BANK.length}
                  </span>
                </div>

                {/* Search Box */}
                <div className="relative">
                  <Search className={`w-4 h-4 absolute left-3 top-2.5 ${darkMode ? 'text-slate-400' : 'text-slate-500'}`} />
                  <input
                    type="text"
                    placeholder="Search keywords, topics..."
                    value={searchQuery}
                    onChange={(e) => {
                      setSearchQuery(e.target.value);
                      setCurrentIndex(0);
                    }}
                    className={`w-full pl-9 pr-3 py-2 text-xs rounded-xl border transition focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                      darkMode
                        ? 'bg-slate-950 border-slate-800 text-slate-100 placeholder-slate-500'
                        : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400'
                    }`}
                  />
                </div>

                {/* Custom Category Dropdown */}
                <div className="relative" ref={dropdownRef}>
                  <button
                    type="button"
                    onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                    className={`w-full flex items-center justify-between p-2.5 text-xs font-semibold rounded-2xl border transition-all duration-200 ${
                      isDropdownOpen
                        ? darkMode
                          ? 'bg-slate-900 border-indigo-500 ring-2 ring-indigo-500/30 text-indigo-300 shadow-md'
                          : 'bg-white border-indigo-500 ring-2 ring-indigo-500/20 text-indigo-700 shadow-sm'
                        : darkMode
                        ? 'bg-slate-950 border-slate-800 text-slate-200 hover:border-slate-700 hover:bg-slate-900'
                        : 'bg-slate-50 border-slate-300 text-slate-800 hover:bg-white hover:border-slate-400 shadow-sm'
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate">
                      <Layers className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
                      <span className="truncate">{selectedCategory}</span>
                    </div>
                    <div className="flex items-center gap-1.5 shrink-0 ml-2">
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                          darkMode ? 'bg-slate-800 text-slate-300' : 'bg-slate-200 text-slate-800'
                        }`}
                      >
                        {categoryCountMap[selectedCategory] || 0}
                      </span>
                      <ChevronDown
                        className={`w-4 h-4 ${darkMode ? 'text-slate-400' : 'text-slate-600'} transition-transform duration-200 ${
                          isDropdownOpen ? 'transform rotate-180 text-indigo-500' : ''
                        }`}
                      />
                    </div>
                  </button>

                  {/* Custom Dropdown Menu Panel */}
                  {isDropdownOpen && (
                    <div
                      className={`absolute left-0 right-0 z-50 mt-1.5 p-1.5 rounded-2xl border shadow-2xl backdrop-blur-xl max-h-72 overflow-y-auto scrollbar-thin animate-fadeIn ${
                        darkMode
                          ? 'bg-slate-900/95 border-slate-800 shadow-slate-950/80'
                          : 'bg-white/95 border-slate-200 shadow-xl'
                      }`}
                    >
                      {CATEGORIES.map((cat) => {
                        const isSelected = selectedCategory === cat;
                        const count = categoryCountMap[cat] || 0;
                        return (
                          <button
                            key={cat}
                            type="button"
                            onClick={() => {
                              setSelectedCategory(cat);
                              setCurrentIndex(0);
                              setIsDropdownOpen(false);
                            }}
                            className={`w-full flex items-center justify-between px-3 py-2 text-xs font-medium rounded-xl transition-all duration-150 mb-0.5 ${
                              isSelected
                                ? darkMode
                                  ? 'bg-indigo-600/20 text-indigo-300 font-bold border border-indigo-500/30'
                                  : 'bg-indigo-50 text-indigo-800 font-bold border border-indigo-200'
                                : darkMode
                                ? 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
                                : 'text-slate-700 hover:bg-slate-100 hover:text-slate-950'
                            }`}
                          >
                            <div className="flex items-center gap-2 truncate">
                              {isSelected ? (
                                <Check className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
                              ) : (
                                <span className="w-3.5 shrink-0" />
                              )}
                              <span className="truncate">{cat}</span>
                            </div>
                            <span
                              className={`text-[10px] px-2 py-0.5 rounded-full font-bold ml-2 shrink-0 ${
                                isSelected
                                  ? darkMode
                                    ? 'bg-indigo-500/30 text-indigo-200'
                                    : 'bg-indigo-200 text-indigo-900'
                                  : darkMode
                                  ? 'bg-slate-950 text-slate-400'
                                  : 'bg-slate-100 text-slate-600'
                              }`}
                            >
                              {count}
                            </span>
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Filter Toggles */}
                <div className={`grid grid-cols-2 gap-2 pt-2 border-t ${darkMode ? 'border-slate-800/80' : 'border-slate-200'}`}>
                  <button
                    onClick={() => setShowOnlyBookmarks(!showOnlyBookmarks)}
                    className={`flex items-center justify-center gap-1.5 py-2 px-2 rounded-xl text-xs font-bold border transition ${
                      showOnlyBookmarks
                        ? 'bg-amber-500/20 border-amber-500/40 text-amber-500'
                        : darkMode
                        ? 'border-slate-800 text-slate-400 hover:bg-slate-800'
                        : 'border-slate-300 bg-slate-50 text-slate-700 hover:bg-white'
                    }`}
                  >
                    <Bookmark className="w-3.5 h-3.5 fill-current" />
                    <span>Starred ({bookmarkedIds.size})</span>
                  </button>

                  <button
                    onClick={() => setShowOnlyMissed(!showOnlyMissed)}
                    className={`flex items-center justify-center gap-1.5 py-2 px-2 rounded-xl text-xs font-bold border transition ${
                      showOnlyMissed
                        ? 'bg-rose-500/20 border-rose-500/40 text-rose-500'
                        : darkMode
                        ? 'border-slate-800 text-slate-400 hover:bg-slate-800'
                        : 'border-slate-300 bg-slate-50 text-slate-700 hover:bg-white'
                    }`}
                  >
                    <XCircle className="w-3.5 h-3.5" />
                    <span>Missed ({totalIncorrect})</span>
                  </button>
                </div>
              </div>

              {/* Progress Summary */}
              <div className={`p-4 rounded-3xl border ${darkMode ? 'bg-slate-900/90 border-slate-800' : 'bg-white border-slate-200 shadow-sm'} space-y-3`}>
                <div className="flex justify-between items-center text-xs">
                  <span className={`font-semibold ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>Total Progress</span>
                  <span className={`font-black ${darkMode ? 'text-indigo-400' : 'text-indigo-700'}`}>
                    {totalAnswered} / {QUESTION_BANK.length} ({Math.round((totalAnswered / QUESTION_BANK.length) * 100)}%)
                  </span>
                </div>
                <div className={`w-full h-2.5 rounded-full overflow-hidden ${darkMode ? 'bg-slate-950' : 'bg-slate-200'}`}>
                  <div
                    className="bg-gradient-to-r from-indigo-600 via-blue-500 to-cyan-500 h-full rounded-full transition-all duration-300"
                    style={{ width: `${(totalAnswered / QUESTION_BANK.length) * 100}%` }}
                  />
                </div>

                <div className="grid grid-cols-3 gap-2 text-center pt-2">
                  <div className={`p-2 rounded-2xl border ${
                    darkMode
                      ? 'bg-emerald-950/30 border-emerald-900/40 text-emerald-400'
                      : 'bg-emerald-50 border-emerald-200 text-emerald-800 shadow-sm'
                  }`}>
                    <span className="text-[10px] font-bold uppercase block">Correct</span>
                    <span className="text-base font-black">{totalCorrect}</span>
                  </div>
                  <div className={`p-2 rounded-2xl border ${
                    darkMode
                      ? 'bg-rose-950/30 border-rose-900/40 text-rose-400'
                      : 'bg-rose-50 border-rose-200 text-rose-800 shadow-sm'
                  }`}>
                    <span className="text-[10px] font-bold uppercase block">Wrong</span>
                    <span className="text-base font-black">{totalIncorrect}</span>
                  </div>
                  <div className={`p-2 rounded-2xl border ${
                    darkMode
                      ? 'bg-cyan-950/30 border-cyan-900/40 text-cyan-400'
                      : 'bg-cyan-50 border-cyan-200 text-cyan-800 shadow-sm'
                  }`}>
                    <span className="text-[10px] font-bold uppercase block">Accuracy</span>
                    <span className="text-base font-black">{overallAccuracy}%</span>
                  </div>
                </div>
              </div>

              {/* FIXED & ENHANCED QUESTION NAVIGATOR */}
              <div className={`p-4 rounded-3xl border ${darkMode ? 'bg-slate-900/90 border-slate-800' : 'bg-white border-slate-200 shadow-sm'} space-y-3`}>
                <div className="flex items-center justify-between text-xs font-bold">
                  <span className={`flex items-center gap-1.5 ${darkMode ? 'text-indigo-400' : 'text-indigo-700'}`}>
                    <ListFilter className="w-3.5 h-3.5" />
                    <span>Question Navigator</span>
                  </span>
                  <span className={`${darkMode ? 'text-slate-400' : 'text-slate-600'} font-normal`}>
                    {filteredQuestions.length > 0 ? currentIndex + 1 : 0} of {filteredQuestions.length}
                  </span>
                </div>

                {/* Legend */}
                <div className={`flex items-center justify-between text-[10px] ${darkMode ? 'text-slate-400 border-slate-800/80' : 'text-slate-600 border-slate-200'} pt-1 pb-2 border-b`}>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span> Correct</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-rose-500 inline-block"></span> Wrong</span>
                  <span className="flex items-center gap-1"><span className={`w-2 h-2 rounded-full ${darkMode ? 'bg-slate-600' : 'bg-slate-300'} inline-block`}></span> Unread</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-400 inline-block"></span> Star</span>
                </div>

                {/* Grid Palette */}
                <div className="max-h-72 overflow-y-auto p-2 pr-3 grid grid-cols-5 gap-2 scrollbar-thin">
                  {filteredQuestions.map((q, idx) => {
                    const isAnswered = userAnswers[q.id] !== undefined;
                    const isCorrect = userAnswers[q.id] === q.correct;
                    const isCurrent = idx === currentIndex;
                    const isStarred = bookmarkedIds.has(q.id);

                    let bgClass = darkMode
                      ? 'bg-slate-950 text-slate-400 border border-slate-800 hover:border-slate-700 hover:text-slate-200'
                      : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 hover:border-slate-400 shadow-sm';

                    if (isAnswered) {
                      bgClass = isCorrect
                        ? 'bg-emerald-600 text-white font-bold border border-emerald-500 shadow-sm shadow-emerald-600/30'
                        : 'bg-rose-600 text-white font-bold border border-rose-500 shadow-sm shadow-rose-600/30';
                    }

                    if (isCurrent) {
                      bgClass = darkMode
                        ? 'border-2 border-cyan-400 bg-cyan-950/90 text-cyan-200 font-black shadow-md shadow-cyan-500/30'
                        : 'border-2 border-indigo-600 bg-indigo-50 text-indigo-900 font-black shadow-md';
                    }

                    return (
                      <button
                        key={q.id}
                        onClick={() => {
                          setCurrentIndex(idx);
                          questionCardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }}
                        className={`h-9 rounded-xl text-xs font-semibold flex items-center justify-center relative transition-all duration-150 ${bgClass}`}
                        title={`Q${idx + 1} (${q.id}): ${q.topic}`}
                      >
                        {idx + 1}
                        {isStarred && (
                          <span className={`absolute -top-1 -right-1 w-2.5 h-2.5 bg-amber-400 rounded-full border ${darkMode ? 'border-slate-950' : 'border-white'} shadow-sm`} />
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Active Question Card */}
            <div className="lg:col-span-3 space-y-4" ref={questionCardRef}>
              {filteredQuestions.length === 0 ? (
                <div className={`p-12 text-center rounded-3xl border ${darkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
                  <AlertCircle className="w-12 h-12 text-amber-500 mx-auto mb-3 opacity-90" />
                  <h3 className="text-lg font-bold">No Questions Match Active Filter</h3>
                  <p className={`text-sm ${darkMode ? 'text-slate-400' : 'text-slate-600'} mt-1`}>
                    Try resetting search keywords or clearing bookmark/missed toggles.
                  </p>
                  <button
                    onClick={() => {
                      setSelectedCategory("All Topics");
                      setSearchQuery("");
                      setShowOnlyBookmarks(false);
                      setShowOnlyMissed(false);
                    }}
                    className="mt-4 px-5 py-2.5 bg-indigo-600 text-white rounded-2xl text-xs font-bold hover:bg-indigo-700 shadow-md"
                  >
                    Reset All Filters
                  </button>
                </div>
              ) : currentQ ? (
                <div className={`p-6 sm:p-8 rounded-3xl border ${darkMode ? 'bg-slate-900/95 border-slate-800 shadow-2xl shadow-slate-950/50' : 'bg-white border-slate-200 shadow-lg'} space-y-6`}>
                  {/* Question Header & Tags */}
                  <div className={`flex flex-wrap items-center justify-between gap-2 pb-4 border-b ${darkMode ? 'border-slate-800/80' : 'border-slate-200'}`}>
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-black ${
                        darkMode
                          ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                          : 'bg-indigo-100 text-indigo-800 border border-indigo-200 font-bold'
                      }`}>
                        Q{currentIndex + 1} of {filteredQuestions.length}
                      </span>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        darkMode ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-700 border border-slate-200'
                      }`}>
                        {currentQ.category}
                      </span>
                      <span className={`hidden sm:inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                        darkMode
                          ? 'bg-cyan-950/40 text-cyan-300 border border-cyan-800/60'
                          : 'bg-cyan-50 text-cyan-800 border border-cyan-200 font-bold'
                      }`}>
                        {currentQ.topic}
                      </span>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => toggleBookmark(currentQ.id)}
                        className={`p-2 rounded-xl border transition ${
                          bookmarkedIds.has(currentQ.id)
                            ? 'bg-amber-500/20 border-amber-500/40 text-amber-500'
                            : darkMode
                            ? 'border-slate-800 text-slate-400 hover:text-slate-200'
                            : 'border-slate-300 bg-white text-slate-600 hover:bg-slate-50'
                        }`}
                        title="Bookmark / Star Question"
                      >
                        <Bookmark className={`w-4 h-4 ${bookmarkedIds.has(currentQ.id) ? 'fill-current' : ''}`} />
                      </button>
                      <button
                        onClick={() =>
                          setShowExplanation((prev) => ({
                            ...prev,
                            [currentQ.id]: !prev[currentQ.id]
                          }))
                        }
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold border transition ${
                          darkMode
                            ? 'bg-slate-800 border-slate-700 hover:bg-slate-700 text-slate-200'
                            : 'bg-slate-100 border-slate-300 hover:bg-slate-200 text-slate-800 shadow-sm'
                        }`}
                      >
                        <HelpCircle className="w-3.5 h-3.5 text-indigo-500" />
                        <span>{showExplanation[currentQ.id] ? 'Hide Solution' : 'Reveal Solution'}</span>
                      </button>
                    </div>
                  </div>

                  {/* Question Stem */}
                  <div className={`text-base sm:text-lg font-bold leading-relaxed ${darkMode ? 'text-slate-100' : 'text-slate-900'}`}>
                    {currentQ.question}
                  </div>

                  {/* Answer Options */}
                  <div className="space-y-3">
                    {currentQ.options.map((option, idx) => {
                      const isSelected = userAnswers[currentQ.id] === idx;
                      const hasAnswered = userAnswers[currentQ.id] !== undefined;
                      const isCorrect = idx === currentQ.correct;

                      let buttonStyle = darkMode
                        ? 'border-slate-800 bg-slate-950/60 hover:bg-slate-800/80 hover:border-slate-700 text-slate-200'
                        : 'border-slate-300 bg-white hover:bg-indigo-50/40 hover:border-indigo-400 text-slate-800 shadow-sm';

                      if (hasAnswered) {
                        if (isCorrect) {
                          buttonStyle = darkMode
                            ? 'border-emerald-500 bg-emerald-950/40 text-emerald-200 font-semibold ring-1 ring-emerald-500'
                            : 'border-emerald-600 bg-emerald-50 text-emerald-950 font-bold ring-2 ring-emerald-500/30 shadow-sm';
                        } else if (isSelected && !isCorrect) {
                          buttonStyle = darkMode
                            ? 'border-rose-500 bg-rose-950/40 text-rose-200 font-semibold ring-1 ring-rose-500'
                            : 'border-rose-600 bg-rose-50 text-rose-950 font-bold ring-2 ring-rose-500/30 shadow-sm';
                        }
                      }

                      const optionLetters = ['A', 'B', 'C', 'D'];

                      return (
                        <button
                          key={idx}
                          onClick={() => handleSelectOption(currentQ.id, idx)}
                          className={`w-full text-left p-4 rounded-2xl border transition-all duration-200 flex items-start gap-3.5 ${buttonStyle}`}
                        >
                          <div
                            className={`w-7 h-7 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 ${
                              hasAnswered && isCorrect
                                ? 'bg-emerald-600 text-white shadow-md'
                                : hasAnswered && isSelected && !isCorrect
                                ? 'bg-rose-600 text-white shadow-md'
                                : darkMode
                                ? 'bg-slate-800 text-slate-300'
                                : 'bg-slate-100 text-slate-700 border border-slate-300'
                            }`}
                          >
                            {hasAnswered && isCorrect ? (
                              <Check className="w-4 h-4" />
                            ) : hasAnswered && isSelected && !isCorrect ? (
                              <X className="w-4 h-4" />
                            ) : (
                              optionLetters[idx]
                            )}
                          </div>
                          <div className="flex-1 text-sm sm:text-base leading-snug pt-0.5">
                            {option}
                          </div>
                        </button>
                      );
                    })}
                  </div>

                  {/* Deep Technical Explanation Banner */}
                  {(showExplanation[currentQ.id] || userAnswers[currentQ.id] !== undefined) && (
                    <div className={`p-5 rounded-2xl border space-y-2.5 animate-fadeIn ${
                      darkMode
                        ? 'bg-gradient-to-br from-indigo-950/50 via-slate-900 to-cyan-950/40 border-indigo-800/60 text-slate-300'
                        : 'bg-gradient-to-br from-indigo-50 via-blue-50/80 to-cyan-50/50 border-indigo-200 text-slate-800 shadow-md'
                    }`}>
                      <div className={`flex items-center gap-2 font-black text-xs uppercase tracking-wider ${
                        darkMode ? 'text-indigo-300' : 'text-indigo-900'
                      }`}>
                        <Sparkles className="w-4 h-4 text-cyan-500" />
                        <span>Core Concept & Engineering Explanation</span>
                      </div>
                      <p className={`text-xs sm:text-sm leading-relaxed ${
                        darkMode ? 'text-slate-300' : 'text-slate-700 font-normal'
                      }`}>
                        {currentQ.explanation}
                      </p>
                      <div className={`pt-2 text-[11px] font-bold flex items-center gap-1.5 ${
                        darkMode ? 'text-cyan-400' : 'text-indigo-700'
                      }`}>
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                        <span>Correct Answer: Option {['A', 'B', 'C', 'D'][currentQ.correct]} ({currentQ.options[currentQ.correct]})</span>
                      </div>
                    </div>
                  )}

                  {/* Navigation Buttons */}
                  <div className={`flex items-center justify-between pt-4 border-t ${darkMode ? 'border-slate-800' : 'border-slate-200'}`}>
                    <button
                      onClick={handlePrev}
                      disabled={currentIndex === 0}
                      className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl text-xs sm:text-sm font-bold border transition ${
                        currentIndex === 0
                          ? darkMode
                            ? 'opacity-30 cursor-not-allowed border-slate-800 text-slate-600'
                            : 'opacity-40 cursor-not-allowed border-slate-200 bg-slate-100 text-slate-400'
                          : darkMode
                          ? 'border-slate-700 hover:bg-slate-800 text-slate-200'
                          : 'border-slate-300 bg-white hover:bg-slate-100 text-slate-800 shadow-sm'
                      }`}
                    >
                      <ChevronLeft className="w-4 h-4" /> Previous
                    </button>

                    <span className={`text-xs font-medium ${darkMode ? 'text-slate-500' : 'text-slate-500'} hidden sm:inline`}>
                      Shortcuts: [1-4] / [A-D] Select • [←/→] Navigate • [S] Star • [E] Solution
                    </span>

                    <button
                      onClick={handleNext}
                      disabled={currentIndex === filteredQuestions.length - 1}
                      className={`flex items-center gap-2 px-6 py-2.5 rounded-2xl text-xs sm:text-sm font-bold bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30 transition ${
                        currentIndex === filteredQuestions.length - 1 ? 'opacity-40 cursor-not-allowed' : ''
                      }`}
                    >
                      Next <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        )}

        {/* =========================================
            MODE 2: TIMED EXAM SIMULATOR
            ========================================= */}
        {mode === 'exam' && (
          <div className="max-w-4xl mx-auto space-y-6">
            {!examStarted ? (
              /* Exam Config Screen */
              <div className={`p-8 sm:p-12 text-center rounded-3xl border ${darkMode ? 'bg-slate-900/95 border-slate-800 shadow-2xl' : 'bg-white border-slate-200 shadow-xl'} space-y-6`}>
                <div className="w-16 h-16 bg-gradient-to-tr from-indigo-600 via-blue-600 to-cyan-500 rounded-3xl flex items-center justify-center mx-auto text-white shadow-xl shadow-indigo-500/25">
                  <Timer className="w-8 h-8" />
                </div>
                <div>
                  <h2 className={`text-2xl sm:text-3xl font-black tracking-tight ${
                    darkMode
                      ? 'bg-gradient-to-r from-indigo-300 via-cyan-300 to-white bg-clip-text text-transparent'
                      : 'text-slate-900'
                  }`}>
                    SQL & Data Warehouse Mock Exam Simulator
                  </h2>
                  <p className={`text-xs sm:text-sm ${darkMode ? 'text-slate-400' : 'text-slate-600'} max-w-lg mx-auto mt-2 leading-relaxed font-medium`}>
                    Test under real-time exam conditions with instant grading, question flagging, jump palette, domain breakdown, and the option to attempt all 200 questions.
                  </p>
                </div>

                {/* Preset Picker */}
                <div className="space-y-3 pt-2">
                  <span className={`text-xs font-bold uppercase tracking-wider ${darkMode ? 'text-slate-400' : 'text-slate-500'} block`}>
                    Choose Assessment Mode & Question Length
                  </span>
                  <div className="flex flex-wrap items-center justify-center gap-3">
                    {[15, 25, 50, 100].map((count) => (
                      <button
                        key={count}
                        onClick={() => setExamQuestionCount(count)}
                        className={`px-5 py-2.5 rounded-2xl text-xs font-bold border transition ${
                          examQuestionCount === count
                            ? 'bg-indigo-600 text-white border-indigo-500 shadow-lg shadow-indigo-600/30'
                            : darkMode
                            ? 'border-slate-800 bg-slate-950/60 hover:bg-slate-800 text-slate-300'
                            : 'border-slate-300 bg-white hover:bg-indigo-50/50 hover:border-indigo-400 text-slate-800 shadow-sm'
                        }`}
                      >
                        {count} Questions ({count} mins)
                      </button>
                    ))}

                    {/* ATTEMPT ALL 200 QUESTIONS OPTION */}
                    <button
                      onClick={() => setExamQuestionCount(200)}
                      className={`px-6 py-2.5 rounded-2xl text-xs font-black border transition flex items-center gap-2 ${
                        examQuestionCount === 200
                          ? 'bg-gradient-to-r from-cyan-600 via-blue-600 to-indigo-600 text-white border-cyan-400 shadow-xl shadow-cyan-600/30 ring-2 ring-cyan-400/50'
                          : darkMode
                          ? 'border-cyan-800/80 bg-cyan-950/30 hover:bg-cyan-950/60 text-cyan-300'
                          : 'border-indigo-300 bg-indigo-50/90 hover:bg-indigo-100 text-indigo-800 shadow-sm'
                      }`}
                    >
                      <Sparkles className="w-4 h-4 text-cyan-400 animate-pulse" />
                      <span>All 200 Questions (Full Mock • 3h 20m)</span>
                    </button>
                  </div>
                </div>

                <div className="pt-4">
                  <button
                    onClick={() => startExam(examQuestionCount)}
                    className="px-10 py-4 bg-gradient-to-r from-indigo-600 via-blue-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white rounded-2xl font-black text-sm sm:text-base shadow-xl shadow-indigo-600/30 transition-all transform hover:-translate-y-0.5"
                  >
                    Start Timed Assessment ({examQuestionCount === 200 ? 'All 200 Qs' : `${examQuestionCount} Qs`})
                  </button>
                </div>
              </div>
            ) : examFinished ? (
              /* Exam Results Summary & Review */
              <div className={`p-8 sm:p-10 rounded-3xl border ${darkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-xl'} space-y-8 animate-fadeIn`}>
                <div className="text-center space-y-2">
                  <div className={`w-16 h-16 rounded-3xl flex items-center justify-center mx-auto mb-2 ${
                    darkMode
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                      : 'bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-sm'
                  }`}>
                    <Award className="w-8 h-8" />
                  </div>
                  <h2 className={`text-2xl sm:text-3xl font-black ${darkMode ? 'text-slate-100' : 'text-slate-900'}`}>
                    Assessment Performance Diagnostic
                  </h2>
                  <p className={`text-sm ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                    Comprehensive breakdown of your domain mastery and accuracy.
                  </p>
                </div>

                {/* Score Big Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className={`p-5 rounded-3xl border text-center ${darkMode ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200 shadow-sm'}`}>
                    <span className={`text-xs font-bold ${darkMode ? 'text-indigo-400' : 'text-indigo-700'} uppercase block mb-1`}>
                      Score Achieved
                    </span>
                    <span className={`text-3xl font-black ${darkMode ? 'text-slate-100' : 'text-slate-900'}`}>
                      {examScore.correct} / {examScore.total}
                    </span>
                  </div>
                  <div className={`p-5 rounded-3xl border text-center ${darkMode ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200 shadow-sm'}`}>
                    <span className={`text-xs font-bold ${darkMode ? 'text-cyan-400' : 'text-cyan-700'} uppercase block mb-1`}>
                      Percentage
                    </span>
                    <span className={`text-3xl font-black ${darkMode ? 'text-slate-100' : 'text-slate-900'}`}>
                      {examScore.percentage}%
                    </span>
                  </div>
                  <div className={`p-5 rounded-3xl border text-center ${darkMode ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200 shadow-sm'}`}>
                    <span className={`text-xs font-bold ${darkMode ? 'text-emerald-400' : 'text-emerald-700'} uppercase block mb-1`}>
                      Readiness Status
                    </span>
                    <span className={`text-lg sm:text-xl font-black ${darkMode ? 'text-emerald-400' : 'text-emerald-700'}`}>
                      {examScore.percentage >= 80 ? '🎉 Exceptional (Ready)' : examScore.percentage >= 60 ? '👍 Proficient (Review)' : '📚 Needs Practice'}
                    </span>
                  </div>
                </div>

                {/* Domain Breakdown */}
                <div className="space-y-4">
                  <h3 className={`text-sm font-black uppercase tracking-wider flex items-center gap-2 ${darkMode ? 'text-indigo-400' : 'text-indigo-700'}`}>
                    <BarChart3 className="w-4 h-4" /> Domain-Wise Mastery Breakdown
                  </h3>
                  <div className="space-y-3">
                    {Object.entries(examScore.categoryStats).map(([cat, stats]) => {
                      const pct = Math.round((stats.correct / stats.total) * 100);
                      return (
                        <div key={cat} className="space-y-1">
                          <div className="flex justify-between text-xs font-medium">
                            <span className={darkMode ? 'text-slate-300' : 'text-slate-700 font-semibold'}>{cat}</span>
                            <span className={`font-bold ${darkMode ? 'text-slate-100' : 'text-slate-900'}`}>{stats.correct}/{stats.total} ({pct}%)</span>
                          </div>
                          <div className={`w-full h-2.5 rounded-full overflow-hidden border ${
                            darkMode ? 'bg-slate-950 border-slate-800' : 'bg-slate-200 border-slate-300'
                          }`}>
                            <div
                              className={`h-full rounded-full transition-all duration-500 ${pct >= 75 ? 'bg-emerald-500' : pct >= 50 ? 'bg-amber-500' : 'bg-rose-500'}`}
                              style={{ width: `${pct}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Question Review Section */}
                <div className={`space-y-4 pt-4 border-t ${darkMode ? 'border-slate-800' : 'border-slate-200'}`}>
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <h3 className={`text-sm font-black uppercase tracking-wider flex items-center gap-2 ${darkMode ? 'text-cyan-400' : 'text-indigo-800'}`}>
                      <CheckCircle2 className="w-4 h-4" /> Detailed Exam Question Review
                    </h3>
                    <div className="flex items-center gap-1.5">
                      <button
                        onClick={() => setExamReviewFilter('all')}
                        className={`px-3 py-1 rounded-xl text-xs font-bold transition ${
                          examReviewFilter === 'all'
                            ? 'bg-indigo-600 text-white'
                            : darkMode
                            ? 'bg-slate-800 text-slate-400'
                            : 'bg-slate-200 text-slate-700'
                        }`}
                      >
                        All ({examQuestions.length})
                      </button>
                      <button
                        onClick={() => setExamReviewFilter('incorrect')}
                        className={`px-3 py-1 rounded-xl text-xs font-bold transition ${
                          examReviewFilter === 'incorrect'
                            ? 'bg-rose-600 text-white'
                            : darkMode
                            ? 'bg-slate-800 text-slate-400'
                            : 'bg-slate-200 text-slate-700'
                        }`}
                      >
                        Incorrect ({examQuestions.length - examScore.correct})
                      </button>
                      <button
                        onClick={() => setExamReviewFilter('flagged')}
                        className={`px-3 py-1 rounded-xl text-xs font-bold transition ${
                          examReviewFilter === 'flagged'
                            ? 'bg-amber-600 text-white'
                            : darkMode
                            ? 'bg-slate-800 text-slate-400'
                            : 'bg-slate-200 text-slate-700'
                        }`}
                      >
                        Flagged ({markedForReview.size})
                      </button>
                    </div>
                  </div>

                  <div className="space-y-3 max-h-96 overflow-y-auto pr-2 scrollbar-thin">
                    {examReviewQuestions.map((q, idx) => {
                      const userAns = examAnswers[q.id];
                      const isCorrect = userAns === q.correct;
                      const isFlagged = markedForReview.has(q.id);

                      return (
                        <div
                          key={q.id}
                          className={`p-4 rounded-2xl border space-y-2 ${
                            isCorrect
                              ? darkMode
                                ? 'bg-emerald-950/20 border-emerald-900/40'
                                : 'bg-emerald-50/70 border-emerald-200 shadow-sm'
                              : darkMode
                              ? 'bg-rose-950/20 border-rose-900/40'
                              : 'bg-rose-50/70 border-rose-200 shadow-sm'
                          }`}
                        >
                          <div className="flex items-center justify-between text-xs">
                            <span className={`font-bold ${darkMode ? 'text-slate-300' : 'text-slate-800'}`}>
                              Q{idx + 1}: {q.topic}
                            </span>
                            <div className="flex items-center gap-2">
                              {isFlagged && <span className="text-amber-500 font-bold">★ Flagged</span>}
                              <span className={`px-2 py-0.5 rounded-full font-black ${
                                isCorrect
                                  ? darkMode
                                    ? 'bg-emerald-500/20 text-emerald-400'
                                    : 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                                  : darkMode
                                  ? 'bg-rose-500/20 text-rose-400'
                                  : 'bg-rose-100 text-rose-800 border border-rose-300'
                              }`}>
                                {isCorrect ? 'CORRECT' : userAns === undefined ? 'UNANSWERED' : 'WRONG'}
                              </span>
                            </div>
                          </div>
                          <p className={`text-xs sm:text-sm font-bold ${darkMode ? 'text-slate-200' : 'text-slate-900'}`}>{q.question}</p>
                          <div className="text-xs space-y-1">
                            <div className={isCorrect ? (darkMode ? 'text-emerald-400 font-bold' : 'text-emerald-700 font-bold') : (darkMode ? 'text-rose-400 font-bold' : 'text-rose-700 font-bold')}>
                              Your Answer: {userAns !== undefined ? `(${['A', 'B', 'C', 'D'][userAns]}) ${q.options[userAns]}` : 'None (Unanswered)'}
                            </div>
                            {!isCorrect && (
                              <div className={darkMode ? 'text-emerald-400 font-bold' : 'text-emerald-700 font-bold'}>
                                Correct Answer: ({['A', 'B', 'C', 'D'][q.correct]}) {q.options[q.correct]}
                              </div>
                            )}
                          </div>
                          <p className={`text-xs pt-1 border-t ${
                            darkMode ? 'text-slate-400 border-slate-800/80' : 'text-slate-700 border-slate-200'
                          }`}>{q.explanation}</p>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Actions */}
                <div className={`flex flex-wrap gap-3 justify-center pt-4 border-t ${darkMode ? 'border-slate-800' : 'border-slate-200'}`}>
                  <button
                    onClick={() => startExam(examQuestionCount)}
                    className="px-6 py-3 bg-indigo-600 text-white rounded-2xl text-xs font-bold hover:bg-indigo-500 flex items-center gap-2 shadow-lg shadow-indigo-600/30"
                  >
                    <RotateCcw className="w-4 h-4" /> Retake Assessment
                  </button>
                  <button
                    onClick={() => {
                      setExamStarted(false);
                      setMode('practice');
                    }}
                    className={`px-6 py-3 border rounded-2xl text-xs font-bold transition ${
                      darkMode
                        ? 'border-slate-700 hover:bg-slate-800 text-slate-300'
                        : 'border-slate-300 bg-white hover:bg-slate-100 text-slate-800 shadow-sm'
                    }`}
                  >
                    Return to Practice & Solutions
                  </button>
                </div>
              </div>
            ) : (
              /* Active Live Exam Interface */
              <div className="space-y-4">
                {/* Exam Top Bar */}
                <div className={`p-4 rounded-3xl border ${darkMode ? 'bg-slate-900/95 border-slate-800' : 'bg-white border-slate-200 shadow-sm'} flex items-center justify-between flex-wrap gap-3`}>
                  <div className="flex items-center gap-3">
                    <span className={`px-3.5 py-1 rounded-full text-xs font-black border ${
                      darkMode
                        ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30'
                        : 'bg-indigo-100 text-indigo-800 border-indigo-200'
                    }`}>
                      Q{examCurrentIdx + 1} of {examQuestions.length}
                    </span>
                    <button
                      onClick={() => toggleReviewMark(examQuestions[examCurrentIdx]?.id)}
                      className={`text-xs px-3 py-1.5 rounded-xl font-bold border flex items-center gap-1.5 transition ${
                        markedForReview.has(examQuestions[examCurrentIdx]?.id)
                          ? 'bg-amber-500/20 border-amber-500/50 text-amber-500'
                          : darkMode
                          ? 'border-slate-800 text-slate-400 hover:text-slate-200'
                          : 'border-slate-300 bg-white text-slate-700 hover:bg-slate-50'
                      }`}
                    >
                      <Flag className="w-3.5 h-3.5" />
                      <span>{markedForReview.has(examQuestions[examCurrentIdx]?.id) ? 'Flagged for Review' : 'Flag for Review'}</span>
                    </button>
                  </div>

                  {/* Timer Display */}
                  <div className={`flex items-center gap-2 px-4 py-1.5 rounded-xl font-mono text-sm font-black border ${
                    examTimeLeft < 300
                      ? 'bg-rose-500/20 text-rose-500 border-rose-500/40 animate-pulse'
                      : darkMode
                      ? 'bg-slate-950 border-slate-800 text-cyan-400'
                      : 'bg-indigo-50 border-indigo-200 text-indigo-800'
                  }`}>
                    <Clock className="w-4 h-4" />
                    <span>{formatTime(examTimeLeft)}</span>
                  </div>

                  <button
                    onClick={() => {
                      if (window.confirm("Are you sure you want to finish and submit your exam now?")) {
                        setExamFinished(true);
                      }
                    }}
                    className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-xs font-black shadow-md shadow-rose-600/30 transition"
                  >
                    Finish & Submit
                  </button>
                </div>

                {/* Filter and Jump Palette for Exam Mode */}
                <div className={`p-4 rounded-3xl border ${darkMode ? 'bg-slate-900/95 border-slate-800' : 'bg-white border-slate-200 shadow-sm'} space-y-2.5`}>
                  <div className="flex items-center justify-between text-xs flex-wrap gap-2">
                    <div className="flex items-center gap-1.5 font-bold">
                      <span className={darkMode ? 'text-slate-400' : 'text-slate-700'}>Jump Palette:</span>
                      <div className="flex gap-1 ml-2">
                        <button
                          onClick={() => setExamNavFilter('all')}
                          className={`px-2 py-0.5 rounded-lg text-[10px] font-bold ${
                            examNavFilter === 'all'
                              ? 'bg-indigo-600 text-white'
                              : darkMode
                              ? 'bg-slate-800 text-slate-400'
                              : 'bg-slate-200 text-slate-700'
                          }`}
                        >
                          All ({examQuestions.length})
                        </button>
                        <button
                          onClick={() => setExamNavFilter('unanswered')}
                          className={`px-2 py-0.5 rounded-lg text-[10px] font-bold ${
                            examNavFilter === 'unanswered'
                              ? 'bg-indigo-600 text-white'
                              : darkMode
                              ? 'bg-slate-800 text-slate-400'
                              : 'bg-slate-200 text-slate-700'
                          }`}
                        >
                          Unanswered ({examQuestions.filter(q => examAnswers[q.id] === undefined).length})
                        </button>
                        <button
                          onClick={() => setExamNavFilter('flagged')}
                          className={`px-2 py-0.5 rounded-lg text-[10px] font-bold ${
                            examNavFilter === 'flagged'
                              ? 'bg-indigo-600 text-white'
                              : darkMode
                              ? 'bg-slate-800 text-slate-400'
                              : 'bg-slate-200 text-slate-700'
                          }`}
                        >
                          Flagged ({markedForReview.size})
                        </button>
                      </div>
                    </div>
                    <span className={`text-[11px] ${darkMode ? 'text-slate-400' : 'text-slate-600'} font-semibold`}>
                      Answered: {Object.keys(examAnswers).length}/{examQuestions.length}
                    </span>
                  </div>

                  {/* Palette Grid */}
                  <div className="max-h-40 overflow-y-auto p-2 pr-3 grid grid-cols-10 sm:grid-cols-20 gap-1.5 scrollbar-thin">
                    {examQuestions.map((q, idx) => {
                      const isAnswered = examAnswers[q.id] !== undefined;
                      const isMarked = markedForReview.has(q.id);
                      const isCurrent = idx === examCurrentIdx;

                      if (examNavFilter === 'unanswered' && isAnswered) return null;
                      if (examNavFilter === 'flagged' && !isMarked) return null;

                      let badgeStyle = darkMode
                        ? 'bg-slate-950 text-slate-400 border border-slate-800 hover:border-slate-700'
                        : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 shadow-sm';
                      if (isAnswered) badgeStyle = 'bg-indigo-600 text-white border-indigo-500 font-bold';
                      if (isMarked) badgeStyle += ' border-2 border-amber-400 text-amber-500';
                      if (isCurrent) {
                        badgeStyle = darkMode
                          ? 'border-2 border-cyan-400 bg-cyan-950/90 text-cyan-200 font-black shadow-sm'
                          : 'border-2 border-indigo-600 bg-indigo-100 text-indigo-900 font-black shadow-sm';
                      }

                      return (
                        <button
                          key={q.id}
                          onClick={() => setExamCurrentIdx(idx)}
                          className={`h-7.5 rounded-lg text-[11px] font-semibold flex items-center justify-center transition-all ${badgeStyle}`}
                        >
                          {idx + 1}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Exam Active Question Card */}
                {examQuestions[examCurrentIdx] && (
                  <div className={`p-6 sm:p-8 rounded-3xl border ${darkMode ? 'bg-slate-900/95 border-slate-800 shadow-xl' : 'bg-white border-slate-200 shadow-lg'} space-y-6`}>
                    <div className={`text-base sm:text-lg font-bold leading-relaxed ${darkMode ? 'text-slate-100' : 'text-slate-900'}`}>
                      {examQuestions[examCurrentIdx].question}
                    </div>

                    {/* Options */}
                    <div className="space-y-3">
                      {examQuestions[examCurrentIdx].options.map((opt, optIdx) => {
                        const isSelected = examAnswers[examQuestions[examCurrentIdx].id] === optIdx;
                        return (
                          <button
                            key={optIdx}
                            onClick={() => handleExamSelect(examQuestions[examCurrentIdx].id, optIdx)}
                            className={`w-full text-left p-4 rounded-2xl border transition-all flex items-start gap-3.5 ${
                              isSelected
                                ? darkMode
                                  ? 'border-cyan-500 bg-cyan-950/40 text-cyan-200 font-semibold ring-1 ring-cyan-400'
                                  : 'border-indigo-600 bg-indigo-50 text-indigo-950 font-bold ring-2 ring-indigo-500/30 shadow-sm'
                                : darkMode
                                ? 'border-slate-800 bg-slate-950/60 hover:bg-slate-800 text-slate-200'
                                : 'border-slate-300 bg-white hover:bg-indigo-50/40 hover:border-indigo-300 text-slate-800 shadow-sm'
                            }`}
                          >
                            <div
                              className={`w-7 h-7 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 ${
                                isSelected
                                  ? darkMode
                                    ? 'bg-cyan-500 text-slate-950 font-black'
                                    : 'bg-indigo-600 text-white font-black'
                                  : darkMode
                                  ? 'bg-slate-800 text-slate-300'
                                  : 'bg-slate-100 text-slate-700 border border-slate-300'
                              }`}
                            >
                              {['A', 'B', 'C', 'D'][optIdx]}
                            </div>
                            <div className="flex-1 text-sm sm:text-base leading-snug pt-0.5">
                              {opt}
                            </div>
                          </button>
                        );
                      })}
                    </div>

                    {/* Exam Prev/Next Footer */}
                    <div className={`flex items-center justify-between pt-4 border-t ${darkMode ? 'border-slate-800' : 'border-slate-200'}`}>
                      <button
                        onClick={() => setExamCurrentIdx((prev) => Math.max(0, prev - 1))}
                        disabled={examCurrentIdx === 0}
                        className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl text-xs sm:text-sm font-bold border ${
                          examCurrentIdx === 0
                            ? darkMode
                              ? 'opacity-30 cursor-not-allowed border-slate-800 text-slate-600'
                              : 'opacity-40 cursor-not-allowed border-slate-200 bg-slate-100 text-slate-400'
                            : darkMode
                            ? 'border-slate-700 hover:bg-slate-800 text-slate-200'
                            : 'border-slate-300 bg-white hover:bg-slate-100 text-slate-800 shadow-sm'
                        }`}
                      >
                        <ChevronLeft className="w-4 h-4" /> Previous
                      </button>

                      <button
                        onClick={() => setExamCurrentIdx((prev) => Math.min(examQuestions.length - 1, prev + 1))}
                        disabled={examCurrentIdx === examQuestions.length - 1}
                        className={`flex items-center gap-2 px-6 py-2.5 rounded-2xl text-xs sm:text-sm font-bold bg-indigo-600 hover:bg-indigo-500 text-white ${
                          examCurrentIdx === examQuestions.length - 1 ? 'opacity-40 cursor-not-allowed' : ''
                        }`}
                      >
                        Next <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* =========================================
            MODE 3: RAPID FLASHCARDS
            ========================================= */}
        {mode === 'flashcards' && (
          <div className="max-w-3xl mx-auto space-y-6">
            <div className="text-center space-y-1">
              <h2 className={`text-xl sm:text-2xl font-black flex items-center justify-center gap-2 ${
                darkMode ? 'text-slate-100' : 'text-slate-900'
              }`}>
                <Zap className="w-6 h-6 text-amber-500" /> Active Recall Flashcards
              </h2>
              <p className={`text-xs ${darkMode ? 'text-slate-400' : 'text-slate-600'} font-medium`}>
                Click anywhere or press [SPACE / ENTER] to flip card.
              </p>
            </div>

            {/* Flashcard Component */}
            {QUESTION_BANK[flashcardIdx] && (
              <div
                onClick={() => setIsFlipped(!isFlipped)}
                className={`cursor-pointer min-h-[340px] p-8 sm:p-10 rounded-3xl border transition-all duration-300 transform hover:-translate-y-1 shadow-2xl ${
                  darkMode
                    ? 'bg-slate-900 border-slate-800 shadow-slate-950/60'
                    : 'bg-white border-slate-200 shadow-xl'
                } flex flex-col justify-between`}
              >
                {/* Top Badge */}
                <div className="flex items-center justify-between text-xs">
                  <span className={`px-3 py-1 rounded-full font-black ${
                    darkMode
                      ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                      : 'bg-indigo-100 text-indigo-800 border border-indigo-200'
                  }`}>
                    Card {flashcardIdx + 1} of {QUESTION_BANK.length}
                  </span>
                  <span className={`text-xs font-bold ${darkMode ? 'text-cyan-400' : 'text-indigo-600'}`}>
                    {isFlipped ? 'Answer Revealed ↻' : 'Click to Flip'}
                  </span>
                </div>

                {/* Card Body */}
                <div className="my-auto text-center py-6">
                  {!isFlipped ? (
                    <div className="space-y-4">
                      <span className={`text-xs font-bold uppercase tracking-wider ${
                        darkMode ? 'text-slate-400' : 'text-slate-500'
                      } block`}>
                        Question
                      </span>
                      <p className={`text-lg sm:text-xl font-bold leading-relaxed ${
                        darkMode ? 'text-slate-100' : 'text-slate-900'
                      }`}>
                        {QUESTION_BANK[flashcardIdx].question}
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-4 animate-fadeIn">
                      <span className={`text-xs font-black uppercase tracking-wider ${
                        darkMode ? 'text-emerald-400' : 'text-emerald-700'
                      } block`}>
                        Verified Solution
                      </span>
                      <p className={`text-lg sm:text-xl font-black ${
                        darkMode ? 'text-emerald-400' : 'text-emerald-700'
                      }`}>
                        {QUESTION_BANK[flashcardIdx].options[QUESTION_BANK[flashcardIdx].correct]}
                      </p>
                      <p className={`text-xs sm:text-sm max-w-xl mx-auto leading-relaxed pt-3 border-t ${
                        darkMode ? 'text-slate-300 border-slate-800' : 'text-slate-700 font-medium border-slate-200'
                      }`}>
                        {QUESTION_BANK[flashcardIdx].explanation}
                      </p>
                    </div>
                  )}
                </div>

                {/* Bottom Footer */}
                <div className={`flex items-center justify-between text-xs pt-4 border-t ${
                  darkMode ? 'text-slate-400 border-slate-800' : 'text-slate-600 border-slate-200 font-semibold'
                }`}>
                  <span className={darkMode ? 'text-slate-300' : 'text-slate-800'}>
                    {QUESTION_BANK[flashcardIdx].category} • {QUESTION_BANK[flashcardIdx].topic}
                  </span>
                  <span className={darkMode ? 'text-indigo-400 font-bold' : 'text-indigo-700 font-bold'}>
                    [SPACE] Flip • [←/→] Next
                  </span>
                </div>
              </div>
            )}

            {/* Flashcard Controls */}
            <div className="flex items-center justify-between max-w-md mx-auto">
              <button
                onClick={() => {
                  setIsFlipped(false);
                  setFlashcardIdx((prev) => Math.max(0, prev - 1));
                }}
                disabled={flashcardIdx === 0}
                className={`px-5 py-2.5 rounded-2xl text-xs font-bold border transition ${
                  flashcardIdx === 0
                    ? darkMode
                      ? 'opacity-30 border-slate-800 text-slate-600'
                      : 'opacity-40 border-slate-200 bg-slate-100 text-slate-400'
                    : darkMode
                    ? 'border-slate-700 hover:bg-slate-800 text-slate-200'
                    : 'border-slate-300 bg-white hover:bg-slate-100 text-slate-800 shadow-sm'
                }`}
              >
                Previous Card
              </button>

              <button
                onClick={() => {
                  setIsFlipped(false);
                  const randomIdx = Math.floor(Math.random() * QUESTION_BANK.length);
                  setFlashcardIdx(randomIdx);
                }}
                className={`p-3 rounded-2xl border transition ${
                  darkMode
                    ? 'border-slate-700 hover:bg-slate-800 text-indigo-400'
                    : 'border-slate-300 bg-white hover:bg-slate-100 text-indigo-600 shadow-sm'
                }`}
                title="Shuffle Random Card"
              >
                <Shuffle className="w-4 h-4" />
              </button>

              <button
                onClick={() => {
                  setIsFlipped(false);
                  setFlashcardIdx((prev) => Math.min(QUESTION_BANK.length - 1, prev + 1));
                }}
                disabled={flashcardIdx === QUESTION_BANK.length - 1}
                className={`px-5 py-2.5 rounded-2xl text-xs font-bold bg-indigo-600 text-white hover:bg-indigo-500 disabled:opacity-40 shadow-md shadow-indigo-600/30`}
              >
                Next Card
              </button>
            </div>
          </div>
        )}

        {/* =========================================
            MODE 4: HIGH-YIELD CHEAT SHEET
            ========================================= */}
        {mode === 'cheatsheet' && (
          <div className="max-w-5xl mx-auto space-y-6">
            <div className="text-center space-y-1">
              <h2 className={`text-xl sm:text-2xl font-black flex items-center justify-center gap-2 ${
                darkMode ? 'text-slate-100' : 'text-slate-900'
              }`}>
                <FileText className="w-6 h-6 text-indigo-600" /> High-Yield Blueprint Revision Sheet
              </h2>
              <p className={`text-xs ${darkMode ? 'text-slate-400' : 'text-slate-600'} font-medium`}>
                Core condensed summary directly mapping to key exam formulas, normalization rules, and architectural design patterns.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {CHEAT_SHEET_ITEMS.map((item, idx) => (
                <div
                  key={idx}
                  className={`p-5 rounded-3xl border shadow-sm space-y-2 hover:border-indigo-500/60 transition ${
                    darkMode
                      ? 'bg-slate-900/90 border-slate-800'
                      : 'bg-white border-slate-200 shadow-md hover:shadow-lg'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <h3 className={`text-sm font-bold ${darkMode ? 'text-slate-100' : 'text-slate-900'}`}>
                      {item.title}
                    </h3>
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                      darkMode
                        ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                        : 'bg-indigo-100 text-indigo-800 border border-indigo-200'
                    }`}>
                      {item.tag}
                    </span>
                  </div>
                  <p className={`text-xs sm:text-sm whitespace-pre-line leading-relaxed ${
                    darkMode ? 'text-slate-300' : 'text-slate-700 font-medium'
                  }`}>
                    {item.content}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
