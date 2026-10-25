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
  ChevronDown,
  Copy,
  Lightbulb,
  Workflow,
  ShieldAlert,
  Compass
} from 'lucide-react';

import { QUESTION_BANK } from './data/questions.js';
import { CATEGORIES, DIFFICULTIES } from './data/categories.js';
import { CHEAT_SHEET_ITEMS } from './data/cheatsheet.js';
import { CONCEPTS_DATA } from './data/concepts.js';

export default function App() {
  // Navigation & UI state
  // Modes: 'practice' | 'exam' | 'concepts' | 'flashcards' | 'cheatsheet'
  const [mode, setMode] = useState('practice');
  const [selectedCategory, setSelectedCategory] = useState("All Topics");
  const [selectedDifficulty, setSelectedDifficulty] = useState("All Difficulties");
  const [showOnlyScenarios, setShowOnlyScenarios] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [copiedCodeId, setCopiedCodeId] = useState(null);

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

  // Save bookmarks & theme
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
  const [activeSolutionTab, setActiveSolutionTab] = useState('intuition'); // 'intuition' | 'visual' | 'technical' | 'tip'

  // Exam Simulator state
  const [examStarted, setExamStarted] = useState(false);
  const [examFinished, setExamFinished] = useState(false);
  const [examQuestions, setExamQuestions] = useState([]);
  const [examAnswers, setExamAnswers] = useState({});
  const [markedForReview, setMarkedForReview] = useState(new Set());
  const [examTimeLeft, setExamTimeLeft] = useState(1800);
  const [examQuestionCount, setExamQuestionCount] = useState(200);
  const [examCategoryFilter, setExamCategoryFilter] = useState("All Topics");
  const [examDifficultyFilter, setExamDifficultyFilter] = useState("All Difficulties");
  const [examCurrentIdx, setExamCurrentIdx] = useState(0);
  const [examNavFilter, setExamNavFilter] = useState('all'); // 'all' | 'unanswered' | 'flagged'
  const [examReviewFilter, setExamReviewFilter] = useState('all'); // 'all' | 'incorrect' | 'flagged'
  const [showSubmitModal, setShowSubmitModal] = useState(false);

  // Flashcards state
  const [flashcardIdx, setFlashcardIdx] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  // Concept Hub state
  const [conceptSearch, setConceptSearch] = useState("");
  const [conceptDomainFilter, setConceptDomainFilter] = useState("All Domains");
  const [expandedConceptId, setExpandedConceptId] = useState("concept-medallion");

  // Custom Category Dropdown state
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  const questionCardRef = useRef(null);

  // Category counts
  const categoryCountMap = useMemo(() => {
    const counts = { "All Topics": QUESTION_BANK.length };
    QUESTION_BANK.forEach((q) => {
      counts[q.category] = (counts[q.category] || 0) + 1;
    });
    return counts;
  }, []);

  // Close dropdown on click outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Filtering for Practice Mode
  const filteredQuestions = useMemo(() => {
    return QUESTION_BANK.filter((q) => {
      const matchesCategory = selectedCategory === "All Topics" || q.category === selectedCategory;
      const matchesDifficulty = selectedDifficulty === "All Difficulties" || q.difficulty === selectedDifficulty;
      const matchesScenario = !showOnlyScenarios || q.isScenario;
      
      const query = searchQuery.trim().toLowerCase();
      const matchesSearch =
        query === "" ||
        q.question.toLowerCase().includes(query) ||
        q.topic.toLowerCase().includes(query) ||
        (q.beginnerConcept && q.beginnerConcept.toLowerCase().includes(query)) ||
        (q.explanation && q.explanation.toLowerCase().includes(query)) ||
        q.options.some((opt) => opt.toLowerCase().includes(query));

      const matchesBookmark = !showOnlyBookmarks || bookmarkedIds.has(q.id);
      const isIncorrect = userAnswers[q.id] !== undefined && userAnswers[q.id] !== q.correct;
      const matchesMissed = !showOnlyMissed || isIncorrect;

      return matchesCategory && matchesDifficulty && matchesScenario && matchesSearch && matchesBookmark && matchesMissed;
    });
  }, [selectedCategory, selectedDifficulty, showOnlyScenarios, searchQuery, showOnlyBookmarks, showOnlyMissed, bookmarkedIds, userAnswers]);

  // Safe bounds check
  useEffect(() => {
    if (filteredQuestions.length > 0 && currentIndex >= filteredQuestions.length) {
      setCurrentIndex(0);
    }
  }, [filteredQuestions.length, currentIndex]);

  const toggleBookmark = (id) => {
    setBookmarkedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
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

  // Exam Timer
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

  const formatTime = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    if (hrs > 0) {
      return `${hrs}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  // Start Exam
  const startExam = (count) => {
    let pool = [...QUESTION_BANK];
    if (examCategoryFilter !== "All Topics") {
      pool = pool.filter((q) => q.category === examCategoryFilter);
    }
    if (examDifficultyFilter !== "All Difficulties") {
      pool = pool.filter((q) => q.difficulty === examDifficultyFilter);
    }

    const totalCount = count === 'all' || count >= pool.length ? pool.length : count;
    const shuffled = [...pool].sort(() => 0.5 - Math.random());
    const selected = shuffled.slice(0, totalCount);

    setExamQuestions(selected);
    setExamQuestionCount(totalCount);
    setExamAnswers({});
    setMarkedForReview(new Set());
    setExamTimeLeft(totalCount * 60); // 1 minute per question
    setExamCurrentIdx(0);
    setExamStarted(true);
    setExamFinished(false);
    setShowSubmitModal(false);
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

  // Copy diagram or code to clipboard
  const handleCopyCode = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedCodeId(id);
    setTimeout(() => setCopiedCodeId(null), 2000);
  };

  // Practice Stats
  const totalAnswered = Object.keys(userAnswers).length;
  const totalCorrect = Object.entries(userAnswers).filter(
    ([id, ans]) => QUESTION_BANK.find((q) => q.id === id)?.correct === ans
  ).length;
  const totalIncorrect = totalAnswered - totalCorrect;
  const overallAccuracy = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;

  // Exam Score Analytics
  const examScore = useMemo(() => {
    if (!examFinished || examQuestions.length === 0) {
      return { correct: 0, total: 0, percentage: 0, categoryStats: {}, difficultyStats: {} };
    }
    let correct = 0;
    const catStats = {};
    const diffStats = {
      Easy: { total: 0, correct: 0 },
      Medium: { total: 0, correct: 0 },
      Hard: { total: 0, correct: 0 }
    };

    examQuestions.forEach((q) => {
      // Category stats
      if (!catStats[q.category]) catStats[q.category] = { total: 0, correct: 0 };
      catStats[q.category].total += 1;

      // Difficulty stats
      if (!diffStats[q.difficulty]) diffStats[q.difficulty] = { total: 0, correct: 0 };
      diffStats[q.difficulty].total += 1;

      if (examAnswers[q.id] === q.correct) {
        correct += 1;
        catStats[q.category].correct += 1;
        diffStats[q.difficulty].correct += 1;
      }
    });

    return {
      correct,
      total: examQuestions.length,
      percentage: Math.round((correct / examQuestions.length) * 100),
      categoryStats: catStats,
      difficultyStats: diffStats
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

  // Filtered concepts
  const filteredConcepts = useMemo(() => {
    return CONCEPTS_DATA.filter((c) => {
      const matchesDomain = conceptDomainFilter === "All Domains" || c.domain === conceptDomainFilter;
      const q = conceptSearch.trim().toLowerCase();
      const matchesSearch =
        q === "" ||
        c.title.toLowerCase().includes(q) ||
        c.summary.toLowerCase().includes(q) ||
        c.beginnerAnalogy.toLowerCase().includes(q) ||
        c.keyRules.some((r) => r.toLowerCase().includes(q));
      return matchesDomain && matchesSearch;
    });
  }, [conceptDomainFilter, conceptSearch]);

  const currentQ = filteredQuestions[currentIndex] || filteredQuestions[0];
  const activeFlashcard = QUESTION_BANK[flashcardIdx] || QUESTION_BANK[0];

  return (
    <div className={`min-h-screen font-sans ${darkMode ? 'bg-slate-950 text-slate-100' : 'bg-slate-50/80 text-slate-900'} transition-colors duration-200`}>
      {/* HEADER NAVBAR */}
      <header className={`sticky top-0 z-40 border-b backdrop-blur-md ${darkMode ? 'bg-slate-950/90 border-slate-800/80 shadow-slate-950/50' : 'bg-white/95 border-slate-200 shadow-sm'} px-4 py-3`}>
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 via-blue-600 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/25 shrink-0">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className={`text-base sm:text-lg font-black tracking-tight ${
                  darkMode
                    ? 'bg-gradient-to-r from-indigo-400 via-cyan-300 to-white bg-clip-text text-transparent'
                    : 'text-slate-900'
                }`}>
                  SQL, DWH & Databricks Master
                </h1>
                <span className={`text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full ${
                  darkMode
                    ? 'bg-cyan-500/20 border border-cyan-500/30 text-cyan-300'
                    : 'bg-indigo-100 border border-indigo-200 text-indigo-800 font-bold'
                }`}>
                  200 Client MCQs
                </span>
              </div>
              <p className={`text-[11px] ${darkMode ? 'text-slate-400' : 'text-slate-600'} hidden sm:block font-medium`}>
                SQL Fundamentals • Advanced Optimization • Medallion Lakehouse • Kimball Modeling • SCD Types 1-6 • Unity Catalog
              </p>
            </div>
          </div>

          {/* Navigation Mode Tabs */}
          <div className={`flex items-center p-1 rounded-2xl gap-1 overflow-x-auto max-w-full ${darkMode ? 'bg-slate-900 border border-slate-800' : 'bg-slate-100 border border-slate-300/80 shadow-inner'}`}>
            <button
              onClick={() => setMode('practice')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${
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
              onClick={() => setMode('concepts')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${
                mode === 'concepts'
                  ? darkMode
                    ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/30'
                    : 'bg-white text-cyan-700 shadow-sm border border-slate-200'
                  : darkMode
                  ? 'text-slate-400 hover:text-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Layers className="w-3.5 h-3.5 text-cyan-400" />
              <span>Concepts & Visuals</span>
              <span className="text-[9px] px-1.5 py-0.2 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-400/30 font-black">NEW</span>
            </button>

            <button
              onClick={() => setMode('exam')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${
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
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${
                mode === 'flashcards'
                  ? darkMode
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'bg-white text-indigo-700 shadow-sm border border-slate-200'
                  : darkMode
                  ? 'text-slate-400 hover:text-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Flashcards</span>
            </button>

            <button
              onClick={() => setMode('cheatsheet')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${
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
              <span>Cheatsheet</span>
            </button>
          </div>

          {/* Right Header Stats & Controls */}
          <div className="flex items-center gap-2">
            <div className={`hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl border text-xs font-bold ${
              darkMode
                ? 'bg-slate-900 border-slate-800 text-slate-300'
                : 'bg-indigo-50 border-indigo-200 text-indigo-900 shadow-sm'
            }`}>
              <Flame className="w-4 h-4 text-amber-500" />
              <span>
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
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                        darkMode ? 'bg-slate-800 text-slate-300' : 'bg-slate-200 text-slate-800'
                      }`}>
                        {categoryCountMap[selectedCategory] || 0}
                      </span>
                      <ChevronDown className={`w-4 h-4 ${darkMode ? 'text-slate-400' : 'text-slate-600'} transition-transform duration-200 ${
                        isDropdownOpen ? 'transform rotate-180 text-indigo-500' : ''
                      }`} />
                    </div>
                  </button>

                  {/* Dropdown Menu */}
                  {isDropdownOpen && (
                    <div className={`absolute left-0 right-0 z-50 mt-1.5 p-1.5 rounded-2xl border shadow-2xl backdrop-blur-xl max-h-72 overflow-y-auto scrollbar-thin ${
                      darkMode ? 'bg-slate-900/95 border-slate-800 shadow-slate-950/80' : 'bg-white/95 border-slate-200 shadow-xl'
                    }`}>
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
                              {isSelected ? <Check className="w-3.5 h-3.5 text-indigo-500 shrink-0" /> : <span className="w-3.5 shrink-0" />}
                              <span className="truncate">{cat}</span>
                            </div>
                            <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ml-2 shrink-0 ${
                              isSelected
                                ? darkMode ? 'bg-indigo-500/30 text-indigo-200' : 'bg-indigo-200 text-indigo-900'
                                : darkMode ? 'bg-slate-950 text-slate-400' : 'bg-slate-100 text-slate-600'
                            }`}>
                              {count}
                            </span>
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Difficulty Filter Pills */}
                <div>
                  <label className={`text-[11px] font-bold block mb-1.5 ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                    Difficulty Level:
                  </label>
                  <div className="grid grid-cols-4 gap-1">
                    {DIFFICULTIES.map((diff) => {
                      const isSelected = selectedDifficulty === diff;
                      let activeStyle = darkMode
                        ? 'bg-indigo-600 text-white font-bold'
                        : 'bg-indigo-600 text-white font-bold shadow-sm';
                      
                      if (diff === "Easy" && isSelected) activeStyle = 'bg-emerald-600 text-white font-bold';
                      if (diff === "Medium" && isSelected) activeStyle = 'bg-amber-600 text-white font-bold';
                      if (diff === "Hard" && isSelected) activeStyle = 'bg-rose-600 text-white font-bold';

                      return (
                        <button
                          key={diff}
                          onClick={() => {
                            setSelectedDifficulty(diff);
                            setCurrentIndex(0);
                          }}
                          className={`py-1.5 text-[10px] rounded-xl font-bold transition text-center border ${
                            isSelected
                              ? `${activeStyle} border-transparent`
                              : darkMode
                              ? 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                              : 'bg-slate-50 border-slate-300 text-slate-700 hover:bg-slate-100'
                          }`}
                        >
                          {diff.replace("All Difficulties", "All")}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Scenario Toggle Button */}
                <button
                  onClick={() => {
                    setShowOnlyScenarios(!showOnlyScenarios);
                    setCurrentIndex(0);
                  }}
                  className={`w-full py-2 px-3 rounded-2xl text-xs font-bold flex items-center justify-between border transition ${
                    showOnlyScenarios
                      ? 'bg-purple-600 text-white border-purple-500 shadow-md shadow-purple-600/30'
                      : darkMode
                      ? 'bg-slate-950 border-slate-800 text-purple-400 hover:bg-slate-800'
                      : 'bg-purple-50 border-purple-200 text-purple-800 hover:bg-purple-100'
                  }`}
                >
                  <span className="flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                    <span>Virtual Client Scenarios Only</span>
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/20 font-black">
                    20
                  </span>
                </button>

                {/* Bookmarks & Missed Toggles */}
                <div className="grid grid-cols-2 gap-2 pt-1 border-t border-slate-800/40">
                  <button
                    onClick={() => {
                      setShowOnlyBookmarks(!showOnlyBookmarks);
                      setCurrentIndex(0);
                    }}
                    className={`py-2 px-3 rounded-2xl text-xs font-bold flex items-center justify-center gap-1.5 border transition ${
                      showOnlyBookmarks
                        ? 'bg-amber-500 text-white border-amber-400 shadow-md'
                        : darkMode
                        ? 'bg-slate-950 border-slate-800 text-slate-400 hover:bg-slate-800'
                        : 'bg-slate-50 border-slate-300 text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    <Bookmark className={`w-3.5 h-3.5 ${showOnlyBookmarks ? 'fill-current' : ''}`} />
                    <span>Starred ({bookmarkedIds.size})</span>
                  </button>

                  <button
                    onClick={() => {
                      setShowOnlyMissed(!showOnlyMissed);
                      setCurrentIndex(0);
                    }}
                    className={`py-2 px-3 rounded-2xl text-xs font-bold flex items-center justify-center gap-1.5 border transition ${
                      showOnlyMissed
                        ? 'bg-rose-600 text-white border-rose-500 shadow-md'
                        : darkMode
                        ? 'bg-slate-950 border-slate-800 text-slate-400 hover:bg-slate-800'
                        : 'bg-slate-50 border-slate-300 text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    <XCircle className="w-3.5 h-3.5" />
                    <span>Missed ({totalIncorrect})</span>
                  </button>
                </div>
              </div>

              {/* Question Navigator Grid */}
              <div className={`p-4 rounded-3xl border ${darkMode ? 'bg-slate-900/90 border-slate-800' : 'bg-white border-slate-200 shadow-sm'} space-y-3`}>
                <div className="flex items-center justify-between">
                  <h4 className={`text-xs font-black uppercase tracking-wider ${darkMode ? 'text-slate-300' : 'text-slate-700'}`}>
                    Question Palette
                  </h4>
                  <span className={`text-[11px] font-bold ${darkMode ? 'text-slate-400' : 'text-slate-500'}`}>
                    Jump to Q#
                  </span>
                </div>

                {/* Legend */}
                <div className="flex flex-wrap items-center gap-2 text-[10px] font-bold text-slate-400 pb-1">
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span> Correct</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-rose-500 inline-block"></span> Missed</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-400 inline-block"></span> Star</span>
                </div>

                {/* Grid Palette */}
                <div className="max-h-72 overflow-y-auto p-1 pr-2 grid grid-cols-5 gap-1.5 scrollbar-thin">
                  {filteredQuestions.map((q, idx) => {
                    const isAnswered = userAnswers[q.id] !== undefined;
                    const isCorrect = userAnswers[q.id] === q.correct;
                    const isCurrent = idx === currentIndex;
                    const isStarred = bookmarkedIds.has(q.id);

                    let bgClass = darkMode
                      ? 'bg-slate-950 text-slate-400 border border-slate-800 hover:border-slate-700 hover:text-slate-200'
                      : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 shadow-sm';

                    if (isAnswered) {
                      bgClass = isCorrect
                        ? 'bg-emerald-600 text-white font-bold border border-emerald-500 shadow-sm'
                        : 'bg-rose-600 text-white font-bold border border-rose-500 shadow-sm';
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
                        title={`Q${q.num} [${q.difficulty}]: ${q.topic}`}
                      >
                        {q.num}
                        {isStarred && (
                          <span className={`absolute -top-1 -right-1 w-2.5 h-2.5 bg-amber-400 rounded-full border ${darkMode ? 'border-slate-950' : 'border-white'} shadow-sm`} />
                        )}
                        {/* Difficulty dot */}
                        <span className={`absolute bottom-0.5 right-1 w-1.5 h-1.5 rounded-full ${
                          q.difficulty === 'Easy' ? 'bg-emerald-400/80' : q.difficulty === 'Hard' ? 'bg-rose-400/80' : 'bg-amber-400/80'
                        }`} />
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Active Question Main Card */}
            <div className="lg:col-span-3 space-y-4" ref={questionCardRef}>
              {filteredQuestions.length === 0 ? (
                <div className={`p-12 text-center rounded-3xl border ${darkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
                  <AlertCircle className="w-12 h-12 text-amber-500 mx-auto mb-3 opacity-90" />
                  <h3 className="text-lg font-bold">No Questions Match Active Filter</h3>
                  <p className={`text-sm ${darkMode ? 'text-slate-400' : 'text-slate-600'} mt-1`}>
                    Try resetting search keywords or clearing difficulty and scenario filters.
                  </p>
                  <button
                    onClick={() => {
                      setSelectedCategory("All Topics");
                      setSelectedDifficulty("All Difficulties");
                      setShowOnlyScenarios(false);
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
                  {/* Question Header & Badges */}
                  <div className={`flex flex-wrap items-center justify-between gap-2 pb-4 border-b ${darkMode ? 'border-slate-800/80' : 'border-slate-200'}`}>
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-black ${
                        darkMode
                          ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                          : 'bg-indigo-100 text-indigo-800 border border-indigo-200 font-bold'
                      }`}>
                        Question {currentQ.num} of 200
                      </span>

                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        darkMode ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-700 border border-slate-200'
                      }`}>
                        {currentQ.category}
                      </span>

                      {/* Difficulty Badge */}
                      <span className={`px-2.5 py-0.5 rounded-full text-xs font-black border ${
                        currentQ.difficulty === 'Easy'
                          ? darkMode ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' : 'bg-emerald-50 text-emerald-800 border-emerald-200'
                          : currentQ.difficulty === 'Hard'
                          ? darkMode ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' : 'bg-rose-50 text-rose-800 border-rose-200'
                          : darkMode ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' : 'bg-amber-50 text-amber-800 border-amber-200'
                      }`}>
                        {currentQ.difficulty}
                      </span>

                      {/* Scenario Badge */}
                      {currentQ.isScenario && (
                        <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border flex items-center gap-1 ${
                          darkMode ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' : 'bg-purple-100 text-purple-900 border-purple-200'
                        }`}>
                          <Sparkles className="w-3 h-3 text-purple-400" />
                          <span>{currentQ.scenarioTitle || "Client Scenario"}</span>
                        </span>
                      )}

                      <span className={`hidden sm:inline-block px-3 py-0.5 rounded-full text-xs font-medium ${
                        darkMode ? 'text-slate-400' : 'text-slate-500'
                      }`}>
                        • {currentQ.topic}
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

                  {/* ENRICHED MULTI-SECTION SOLUTION & VISUALIZATION BANNER */}
                  {(showExplanation[currentQ.id] || userAnswers[currentQ.id] !== undefined) && (
                    <div className={`p-5 rounded-3xl border space-y-4 animate-fadeIn ${
                      darkMode
                        ? 'bg-gradient-to-br from-indigo-950/40 via-slate-900 to-cyan-950/30 border-indigo-800/60 text-slate-300'
                        : 'bg-gradient-to-br from-indigo-50/90 via-blue-50/70 to-cyan-50/50 border-indigo-200 text-slate-800 shadow-md'
                    }`}>
                      {/* Solution Header & Tab Navigation */}
                      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-indigo-500/20 pb-3">
                        <div className="flex items-center gap-2">
                          <Sparkles className="w-4 h-4 text-cyan-400" />
                          <span className="text-xs font-black uppercase tracking-wider text-indigo-400">
                            Comprehensive Solution & Visualization
                          </span>
                        </div>
                        {/* Tab Switcher */}
                        <div className={`flex items-center p-0.5 rounded-xl gap-1 text-[11px] font-bold ${
                          darkMode ? 'bg-slate-950/80 border border-slate-800' : 'bg-white border border-slate-300 shadow-sm'
                        }`}>
                          <button
                            onClick={() => setActiveSolutionTab('intuition')}
                            className={`px-2.5 py-1 rounded-lg transition ${
                              activeSolutionTab === 'intuition'
                                ? 'bg-indigo-600 text-white'
                                : darkMode ? 'text-slate-400 hover:text-slate-200' : 'text-slate-600 hover:text-slate-900'
                            }`}
                          >
                            💡 Intuition
                          </button>
                          <button
                            onClick={() => setActiveSolutionTab('visual')}
                            className={`px-2.5 py-1 rounded-lg transition ${
                              activeSolutionTab === 'visual'
                                ? 'bg-cyan-600 text-white'
                                : darkMode ? 'text-slate-400 hover:text-slate-200' : 'text-slate-600 hover:text-slate-900'
                            }`}
                          >
                            📐 Architecture Flow
                          </button>
                          <button
                            onClick={() => setActiveSolutionTab('technical')}
                            className={`px-2.5 py-1 rounded-lg transition ${
                              activeSolutionTab === 'technical'
                                ? 'bg-indigo-600 text-white'
                                : darkMode ? 'text-slate-400 hover:text-slate-200' : 'text-slate-600 hover:text-slate-900'
                            }`}
                          >
                            🎯 Technical
                          </button>
                          <button
                            onClick={() => setActiveSolutionTab('tip')}
                            className={`px-2.5 py-1 rounded-lg transition ${
                              activeSolutionTab === 'tip'
                                ? 'bg-amber-600 text-white'
                                : darkMode ? 'text-slate-400 hover:text-slate-200' : 'text-slate-600 hover:text-slate-900'
                            }`}
                          >
                            💼 Client Tip
                          </button>
                        </div>
                      </div>

                      {/* Correct Answer Banner */}
                      <div className={`p-3 rounded-2xl flex items-center justify-between border ${
                        darkMode ? 'bg-emerald-950/40 border-emerald-500/30 text-emerald-200' : 'bg-emerald-50 border-emerald-200 text-emerald-900'
                      }`}>
                        <div className="flex items-center gap-2">
                          <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                          <span className="text-xs sm:text-sm font-bold">
                            Correct Answer: Option {['A', 'B', 'C', 'D'][currentQ.correct]}
                          </span>
                        </div>
                        <span className="text-xs font-semibold truncate max-w-[250px] sm:max-w-md hidden sm:inline">
                          "{currentQ.options[currentQ.correct]}"
                        </span>
                      </div>

                      {/* Tab 1: Beginner Intuition */}
                      {activeSolutionTab === 'intuition' && (
                        <div className="space-y-2 animate-fadeIn">
                          <div className="flex items-center gap-2 text-xs font-bold text-amber-400">
                            <Lightbulb className="w-4 h-4 text-amber-400" />
                            <span>Beginner Mental Model (Intuition Without Jargon)</span>
                          </div>
                          <p className={`text-xs sm:text-sm leading-relaxed ${darkMode ? 'text-slate-200' : 'text-slate-700'}`}>
                            {currentQ.beginnerConcept}
                          </p>
                        </div>
                      )}

                      {/* Tab 2: Visual Diagram & Architecture Flow */}
                      {activeSolutionTab === 'visual' && (
                        <div className="space-y-2 animate-fadeIn">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-bold text-cyan-400 flex items-center gap-1.5">
                              <Workflow className="w-4 h-4 text-cyan-400" />
                              <span>Architectural Diagram & Data Flow</span>
                            </span>
                            <button
                              onClick={() => handleCopyCode(currentQ.visualDiagram, currentQ.id)}
                              className={`text-[11px] px-2 py-1 rounded-lg border flex items-center gap-1 ${
                                copiedCodeId === currentQ.id
                                  ? 'bg-emerald-600 text-white border-emerald-500'
                                  : darkMode
                                  ? 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'
                                  : 'bg-white border-slate-300 text-slate-700 hover:bg-slate-100'
                              }`}
                            >
                              <Copy className="w-3 h-3" />
                              <span>{copiedCodeId === currentQ.id ? 'Copied!' : 'Copy Diagram'}</span>
                            </button>
                          </div>
                          <pre className={`p-4 rounded-2xl text-[11px] sm:text-xs font-mono leading-snug overflow-x-auto border ${
                            darkMode
                              ? 'bg-slate-950 border-slate-800 text-cyan-300'
                              : 'bg-slate-900 border-slate-700 text-cyan-200'
                          }`}>
                            {currentQ.visualDiagram}
                          </pre>
                        </div>
                      )}

                      {/* Tab 3: Technical Breakdown */}
                      {activeSolutionTab === 'technical' && (
                        <div className="space-y-2 animate-fadeIn">
                          <div className="flex items-center gap-2 text-xs font-bold text-indigo-400">
                            <Cpu className="w-4 h-4 text-indigo-400" />
                            <span>Deep Engineering Explanation & Options Analysis</span>
                          </div>
                          <p className={`text-xs sm:text-sm leading-relaxed ${darkMode ? 'text-slate-300' : 'text-slate-700'}`}>
                            {currentQ.explanation}
                          </p>
                        </div>
                      )}

                      {/* Tab 4: Client Interview Pro-Tip */}
                      {activeSolutionTab === 'tip' && (
                        <div className="space-y-2 animate-fadeIn">
                          <div className="flex items-center gap-2 text-xs font-bold text-amber-400">
                            <Award className="w-4 h-4 text-amber-400" />
                            <span>Client / Big-4 Technical Interview Strategy</span>
                          </div>
                          <p className={`text-xs sm:text-sm leading-relaxed ${darkMode ? 'text-slate-300' : 'text-slate-700'}`}>
                            {currentQ.interviewTip}
                          </p>
                        </div>
                      )}
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
            MODE 2: CONCEPT & VISUALIZATION HUB (BRAND NEW!)
            ========================================= */}
        {mode === 'concepts' && (
          <div className="space-y-6">
            {/* Concept Hub Intro Banner */}
            <div className={`p-6 sm:p-8 rounded-3xl border ${
              darkMode
                ? 'bg-gradient-to-r from-indigo-950/60 via-slate-900 to-cyan-950/40 border-slate-800'
                : 'bg-gradient-to-r from-indigo-50 via-white to-cyan-50 border-slate-200 shadow-sm'
            }`}>
              <div className="max-w-3xl space-y-2">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-cyan-500/20 text-cyan-300 border border-cyan-400/30">
                    Architectural Blueprints & Mental Models
                  </span>
                </div>
                <h2 className="text-xl sm:text-2xl font-black tracking-tight">
                  Concept Explanation & Visualization Hub
                </h2>
                <p className={`text-xs sm:text-sm ${darkMode ? 'text-slate-300' : 'text-slate-600'} leading-relaxed`}>
                  Master every core architecture from scratch. Even complete beginners can grasp Databricks, Delta Lake, Spark distributed memory, and Kimball dimensional modeling through intuitive analogies and ASCII execution blueprints.
                </p>
              </div>

              {/* Search & Domain Filter Bar */}
              <div className="mt-6 flex flex-wrap items-center gap-3">
                <div className="relative flex-1 min-w-[240px]">
                  <Search className={`w-4 h-4 absolute left-3 top-3 ${darkMode ? 'text-slate-400' : 'text-slate-500'}`} />
                  <input
                    type="text"
                    placeholder="Search concepts, architectures, SQL rules..."
                    value={conceptSearch}
                    onChange={(e) => setConceptSearch(e.target.value)}
                    className={`w-full pl-9 pr-3 py-2.5 text-xs rounded-2xl border transition focus:outline-none focus:ring-2 focus:ring-cyan-500 ${
                      darkMode
                        ? 'bg-slate-950 border-slate-800 text-slate-100 placeholder-slate-500'
                        : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'
                    }`}
                  />
                </div>
              </div>
            </div>

            {/* Concepts List Grid */}
            <div className="grid grid-cols-1 gap-6">
              {filteredConcepts.map((concept) => {
                const isExpanded = expandedConceptId === concept.id;
                return (
                  <div
                    key={concept.id}
                    className={`rounded-3xl border transition-all duration-200 overflow-hidden ${
                      isExpanded
                        ? darkMode
                          ? 'bg-slate-900/95 border-cyan-500/50 shadow-2xl shadow-cyan-950/30'
                          : 'bg-white border-cyan-400 shadow-xl'
                        : darkMode
                        ? 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                        : 'bg-white border-slate-200 hover:border-slate-300 shadow-sm'
                    }`}
                  >
                    {/* Header bar */}
                    <div
                      onClick={() => setExpandedConceptId(isExpanded ? null : concept.id)}
                      className="p-5 sm:p-6 flex items-center justify-between gap-4 cursor-pointer select-none"
                    >
                      <div className="space-y-1.5 flex-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider ${
                            darkMode ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30' : 'bg-cyan-100 text-cyan-800 border border-cyan-200'
                          }`}>
                            {concept.badge}
                          </span>
                          <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                            darkMode ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-700'
                          }`}>
                            {concept.domain}
                          </span>
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                            concept.difficulty === 'Easy'
                              ? 'bg-emerald-500/20 text-emerald-400'
                              : concept.difficulty === 'Hard'
                              ? 'bg-rose-500/20 text-rose-400'
                              : 'bg-amber-500/20 text-amber-400'
                          }`}>
                            {concept.difficulty}
                          </span>
                        </div>
                        <h3 className="text-base sm:text-lg font-black tracking-tight">
                          {concept.title}
                        </h3>
                        <p className={`text-xs ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                          {concept.summary}
                        </p>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        <span className="text-xs font-bold text-cyan-400 hidden sm:inline">
                          {isExpanded ? 'Collapse' : 'Explore Architecture'}
                        </span>
                        <ChevronDown className={`w-5 h-5 text-cyan-400 transition-transform duration-200 ${
                          isExpanded ? 'transform rotate-180' : ''
                        }`} />
                      </div>
                    </div>

                    {/* Expanded Detail Panel */}
                    {isExpanded && (
                      <div className={`p-5 sm:p-6 pt-0 space-y-6 border-t ${darkMode ? 'border-slate-800/80' : 'border-slate-100'}`}>
                        {/* 1. Beginner Intuition Box */}
                        <div className={`p-4 rounded-2xl border space-y-1.5 ${
                          darkMode ? 'bg-amber-950/20 border-amber-500/30 text-amber-200' : 'bg-amber-50 border-amber-200 text-amber-900'
                        }`}>
                          <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wider text-amber-500">
                            <Lightbulb className="w-4 h-4" />
                            <span>Beginner Mental Model (Plain-English Analogy)</span>
                          </div>
                          <p className="text-xs sm:text-sm leading-relaxed font-normal">
                            {concept.beginnerAnalogy}
                          </p>
                        </div>

                        {/* 2. Visual ASCII Architecture Diagram */}
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-black uppercase tracking-wider text-cyan-400 flex items-center gap-1.5">
                              <Workflow className="w-4 h-4 text-cyan-400" />
                              <span>Architectural Data Flow & Schema Layout</span>
                            </span>
                            <button
                              onClick={() => handleCopyCode(concept.visualDiagram, concept.id)}
                              className={`text-[11px] px-2.5 py-1 rounded-xl border flex items-center gap-1.5 font-bold transition ${
                                copiedCodeId === concept.id
                                  ? 'bg-emerald-600 text-white border-emerald-500'
                                  : darkMode
                                  ? 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'
                                  : 'bg-white border-slate-300 text-slate-700 hover:bg-slate-100'
                              }`}
                            >
                              <Copy className="w-3.5 h-3.5" />
                              <span>{copiedCodeId === concept.id ? 'Copied!' : 'Copy Blueprint'}</span>
                            </button>
                          </div>
                          <pre className={`p-5 rounded-2xl text-[11px] sm:text-xs font-mono leading-relaxed overflow-x-auto border ${
                            darkMode
                              ? 'bg-slate-950 border-slate-800 text-cyan-300 shadow-inner'
                              : 'bg-slate-900 border-slate-700 text-cyan-200'
                          }`}>
                            {concept.visualDiagram}
                          </pre>
                        </div>

                        {/* 3. Core Architectural Rules */}
                        <div className="space-y-2">
                          <h4 className="text-xs font-black uppercase tracking-wider text-indigo-400">
                            Key Architectural Rules to Memorize
                          </h4>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                            {concept.keyRules.map((rule, idx) => (
                              <div
                                key={idx}
                                className={`p-3 rounded-2xl border text-xs leading-snug flex items-start gap-2 ${
                                  darkMode ? 'bg-slate-950/60 border-slate-800 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-700'
                                }`}
                              >
                                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                                <span>{rule}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* 4. Client Interview Trap & Code Example */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                          {/* Interview Trap */}
                          <div className={`p-4 rounded-2xl border space-y-1.5 ${
                            darkMode ? 'bg-rose-950/20 border-rose-500/30 text-rose-200' : 'bg-rose-50 border-rose-200 text-rose-900'
                          }`}>
                            <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wider text-rose-400">
                              <ShieldAlert className="w-4 h-4 text-rose-500" />
                              <span>Client Interview Trap / Anti-Pattern Alert</span>
                            </div>
                            <p className="text-xs sm:text-sm leading-relaxed">
                              {concept.interviewGotchas}
                            </p>
                          </div>

                          {/* Reference Code Snippet */}
                          <div className={`p-4 rounded-2xl border space-y-1.5 ${
                            darkMode ? 'bg-slate-950 border-slate-800' : 'bg-slate-900 text-slate-100 border-slate-700'
                          }`}>
                            <div className="flex items-center justify-between">
                              <span className="text-xs font-bold text-slate-400">
                                Implementation Reference
                              </span>
                              <button
                                onClick={() => handleCopyCode(concept.codeExample, `code-${concept.id}`)}
                                className="text-[10px] text-cyan-400 hover:text-cyan-300 font-bold"
                              >
                                {copiedCodeId === `code-${concept.id}` ? 'Copied' : 'Copy SQL'}
                              </button>
                            </div>
                            <pre className="text-[11px] font-mono leading-relaxed overflow-x-auto text-cyan-300">
                              {concept.codeExample}
                            </pre>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* =========================================
            MODE 3: EXAM SIMULATOR MODE
            ========================================= */}
        {mode === 'exam' && (
          <div>
            {!examStarted ? (
              /* Exam Config Screen */
              <div className={`max-w-2xl mx-auto p-6 sm:p-10 rounded-3xl border text-center space-y-6 ${
                darkMode ? 'bg-slate-900 border-slate-800 shadow-2xl' : 'bg-white border-slate-200 shadow-xl'
              }`}>
                <div className="w-16 h-16 rounded-3xl bg-indigo-600/20 text-indigo-500 border border-indigo-500/30 flex items-center justify-center mx-auto shadow-lg">
                  <Timer className="w-8 h-8" />
                </div>
                <div>
                  <h2 className="text-xl sm:text-2xl font-black">
                    Databricks & SQL Client Mock Exam Simulator
                  </h2>
                  <p className={`text-xs sm:text-sm ${darkMode ? 'text-slate-400' : 'text-slate-600'} mt-1`}>
                    Timed certification-style exam with randomized questions, flagged review, and category breakdown.
                  </p>
                </div>

                {/* Filters for Exam */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
                  <div>
                    <label className={`text-xs font-bold block mb-1 ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                      Filter by Domain:
                    </label>
                    <select
                      value={examCategoryFilter}
                      onChange={(e) => setExamCategoryFilter(e.target.value)}
                      className={`w-full p-2.5 text-xs rounded-xl border ${
                        darkMode ? 'bg-slate-950 border-slate-800 text-slate-200' : 'bg-slate-50 border-slate-300 text-slate-800'
                      }`}
                    >
                      {CATEGORIES.map((cat) => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className={`text-xs font-bold block mb-1 ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                      Filter by Difficulty:
                    </label>
                    <select
                      value={examDifficultyFilter}
                      onChange={(e) => setExamDifficultyFilter(e.target.value)}
                      className={`w-full p-2.5 text-xs rounded-xl border ${
                        darkMode ? 'bg-slate-950 border-slate-800 text-slate-200' : 'bg-slate-50 border-slate-300 text-slate-800'
                      }`}
                    >
                      {DIFFICULTIES.map((d) => (
                        <option key={d} value={d}>{d}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Select Question Count */}
                <div className="space-y-3">
                  <span className={`text-xs font-bold block ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                    Choose Number of Questions:
                  </span>
                  <div className="grid grid-cols-5 gap-2">
                    {[10, 25, 50, 100, 200].map((cnt) => (
                      <button
                        key={cnt}
                        onClick={() => startExam(cnt)}
                        className="py-3 px-2 rounded-2xl text-xs font-black border transition bg-indigo-600 hover:bg-indigo-500 text-white shadow-md shadow-indigo-600/25 flex flex-col items-center justify-center gap-1"
                      >
                        <span className="text-base">{cnt}</span>
                        <span className="text-[10px] font-medium opacity-80">{cnt} Mins</span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : examFinished ? (
              /* Exam Finished Score Report */
              <div className="max-w-4xl mx-auto space-y-6">
                <div className={`p-8 rounded-3xl border text-center space-y-4 ${
                  darkMode ? 'bg-slate-900 border-slate-800 shadow-2xl' : 'bg-white border-slate-200 shadow-xl'
                }`}>
                  <div className={`w-20 h-20 rounded-3xl mx-auto flex items-center justify-center text-3xl font-black ${
                    examScore.percentage >= 70
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 shadow-emerald-500/20'
                      : 'bg-rose-500/20 text-rose-400 border border-rose-500/40 shadow-rose-500/20'
                  }`}>
                    {examScore.percentage}%
                  </div>
                  <div>
                    <h2 className="text-2xl font-black">
                      {examScore.percentage >= 70 ? '🎉 Congratulations! You Passed!' : '📚 Needs Review - Keep Practicing!'}
                    </h2>
                    <p className={`text-xs sm:text-sm ${darkMode ? 'text-slate-400' : 'text-slate-600'} mt-1`}>
                      You answered {examScore.correct} out of {examScore.total} questions correctly. Passing score threshold is 70%.
                    </p>
                  </div>

                  {/* Difficulty Breakdown */}
                  <div className="grid grid-cols-3 gap-3 max-w-lg mx-auto pt-2">
                    {['Easy', 'Medium', 'Hard'].map((diff) => {
                      const stat = examScore.difficultyStats[diff] || { total: 0, correct: 0 };
                      const pct = stat.total > 0 ? Math.round((stat.correct / stat.total) * 100) : 0;
                      return (
                        <div key={diff} className={`p-3 rounded-2xl border text-center ${
                          darkMode ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200'
                        }`}>
                          <span className="text-[10px] font-bold uppercase tracking-wider block text-slate-400">
                            {diff}
                          </span>
                          <span className="text-lg font-black block mt-0.5">
                            {stat.correct}/{stat.total}
                          </span>
                          <span className={`text-[10px] font-bold ${pct >= 70 ? 'text-emerald-400' : 'text-amber-400'}`}>
                            {pct}%
                          </span>
                        </div>
                      );
                    })}
                  </div>

                  <div className="flex flex-wrap items-center justify-center gap-3 pt-3">
                    <button
                      onClick={() => setExamStarted(false)}
                      className="px-6 py-2.5 rounded-2xl bg-indigo-600 text-white font-bold text-xs hover:bg-indigo-500 shadow-md"
                    >
                      Start New Exam
                    </button>
                    <button
                      onClick={() => setMode('practice')}
                      className={`px-6 py-2.5 rounded-2xl border text-xs font-bold ${
                        darkMode ? 'border-slate-700 bg-slate-800 hover:bg-slate-700' : 'border-slate-300 bg-white hover:bg-slate-50'
                      }`}
                    >
                      Return to Practice
                    </button>
                  </div>
                </div>

                {/* Question Review Section */}
                <div className={`p-6 sm:p-8 rounded-3xl border space-y-4 ${
                  darkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'
                }`}>
                  <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
                    <h3 className="text-base font-black flex items-center gap-2">
                      <Award className="w-4 h-4 text-indigo-400" />
                      <span>Exam Answers Review</span>
                    </h3>
                    <div className="flex items-center gap-2">
                      {['all', 'incorrect', 'flagged'].map((rf) => (
                        <button
                          key={rf}
                          onClick={() => setExamReviewFilter(rf)}
                          className={`px-3 py-1 rounded-xl text-xs font-bold border capitalize transition ${
                            examReviewFilter === rf
                              ? 'bg-indigo-600 text-white border-indigo-500'
                              : darkMode
                              ? 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200'
                              : 'bg-slate-100 border-slate-300 text-slate-700'
                          }`}
                        >
                          {rf}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-4">
                    {examReviewQuestions.map((q, idx) => {
                      const userAns = examAnswers[q.id];
                      const isCorrect = userAns === q.correct;
                      return (
                        <div
                          key={q.id}
                          className={`p-5 rounded-2xl border space-y-3 ${
                            isCorrect
                              ? darkMode ? 'bg-emerald-950/20 border-emerald-500/30' : 'bg-emerald-50/60 border-emerald-200'
                              : darkMode ? 'bg-rose-950/20 border-rose-500/30' : 'bg-rose-50/60 border-rose-200'
                          }`}
                        >
                          <div className="flex items-center justify-between gap-2">
                            <span className="text-xs font-black">
                              Q{idx + 1}. {q.category} • [{q.difficulty}]
                            </span>
                            <span className={`text-xs font-black px-2.5 py-0.5 rounded-full ${
                              isCorrect ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                            }`}>
                              {isCorrect ? 'Correct' : userAns !== undefined ? 'Incorrect' : 'Unanswered'}
                            </span>
                          </div>
                          <p className="text-sm font-bold leading-relaxed">{q.question}</p>
                          <div className="text-xs space-y-1">
                            <p className="text-emerald-400 font-bold">
                              ✓ Correct: {['A', 'B', 'C', 'D'][q.correct]} - {q.options[q.correct]}
                            </p>
                            {userAns !== undefined && !isCorrect && (
                              <p className="text-rose-400 font-bold">
                                ✗ Your Answer: {['A', 'B', 'C', 'D'][userAns]} - {q.options[userAns]}
                              </p>
                            )}
                          </div>
                          <p className={`text-xs leading-relaxed pt-2 border-t ${darkMode ? 'border-slate-800 text-slate-300' : 'border-slate-200 text-slate-700'}`}>
                            💡 {q.explanation}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            ) : (
              /* Active Exam Screen */
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                {/* Active Exam Sidebar */}
                <div className="lg:col-span-1 space-y-4">
                  <div className={`p-5 rounded-3xl border text-center space-y-3 ${
                    darkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'
                  }`}>
                    <div className="flex items-center justify-center gap-2">
                      <Clock className="w-5 h-5 text-indigo-400" />
                      <span className={`text-2xl font-black font-mono ${
                        examTimeLeft < 300 ? 'text-rose-400 animate-pulse' : ''
                      }`}>
                        {formatTime(examTimeLeft)}
                      </span>
                    </div>
                    <span className="text-[11px] font-bold text-slate-400 block">
                      Time Remaining
                    </span>
                    <button
                      onClick={() => setShowSubmitModal(true)}
                      className="w-full py-2.5 rounded-2xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs shadow-md shadow-rose-600/30"
                    >
                      End & Submit Exam
                    </button>
                  </div>

                  {/* Exam Question Navigator */}
                  <div className={`p-4 rounded-3xl border space-y-3 ${
                    darkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'
                  }`}>
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-400">Exam Navigator</span>
                      <span className="text-xs font-black">
                        {Object.keys(examAnswers).length} / {examQuestions.length}
                      </span>
                    </div>
                    <div className="max-h-72 overflow-y-auto p-1 grid grid-cols-5 gap-1.5 scrollbar-thin">
                      {examQuestions.map((q, idx) => {
                        const isAnswered = examAnswers[q.id] !== undefined;
                        const isFlagged = markedForReview.has(q.id);
                        const isCurrent = idx === examCurrentIdx;
                        return (
                          <button
                            key={q.id}
                            onClick={() => setExamCurrentIdx(idx)}
                            className={`h-8 rounded-xl text-xs font-bold relative transition ${
                              isCurrent
                                ? 'border-2 border-cyan-400 bg-cyan-950 text-cyan-200 shadow-md'
                                : isAnswered
                                ? 'bg-indigo-600 text-white'
                                : darkMode
                                ? 'bg-slate-950 border border-slate-800 text-slate-400'
                                : 'bg-slate-100 border border-slate-300 text-slate-700'
                            }`}
                          >
                            {idx + 1}
                            {isFlagged && (
                              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-amber-400 rounded-full" />
                            )}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Active Exam Question Card */}
                <div className="lg:col-span-3 space-y-4">
                  {examQuestions[examCurrentIdx] && (
                    <div className={`p-6 sm:p-8 rounded-3xl border space-y-6 ${
                      darkMode ? 'bg-slate-900 border-slate-800 shadow-xl' : 'bg-white border-slate-200 shadow-lg'
                    }`}>
                      <div className="flex items-center justify-between border-b border-slate-800/80 pb-4">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-black px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                            Question {examCurrentIdx + 1} of {examQuestions.length}
                          </span>
                          <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300">
                            {examQuestions[examCurrentIdx].category}
                          </span>
                        </div>
                        <button
                          onClick={() => toggleReviewMark(examQuestions[examCurrentIdx].id)}
                          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold border transition ${
                            markedForReview.has(examQuestions[examCurrentIdx].id)
                              ? 'bg-amber-500/20 border-amber-500/40 text-amber-400'
                              : darkMode
                              ? 'bg-slate-950 border-slate-800 text-slate-400'
                              : 'bg-slate-100 border-slate-300 text-slate-700'
                          }`}
                        >
                          <Flag className="w-3.5 h-3.5" />
                          <span>{markedForReview.has(examQuestions[examCurrentIdx].id) ? 'Flagged' : 'Flag for Review'}</span>
                        </button>
                      </div>

                      <div className="text-base sm:text-lg font-bold leading-relaxed">
                        {examQuestions[examCurrentIdx].question}
                      </div>

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
                                    ? 'border-indigo-500 bg-indigo-950/40 text-indigo-200 ring-2 ring-indigo-500/30'
                                    : 'border-indigo-600 bg-indigo-50 text-indigo-900 ring-2 ring-indigo-500/20 font-bold'
                                  : darkMode
                                  ? 'border-slate-800 bg-slate-950/60 hover:bg-slate-800/80 text-slate-200'
                                  : 'border-slate-300 bg-white hover:bg-slate-50 text-slate-800'
                              }`}
                            >
                              <div className={`w-7 h-7 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 ${
                                isSelected ? 'bg-indigo-600 text-white' : darkMode ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-700'
                              }`}>
                                {['A', 'B', 'C', 'D'][optIdx]}
                              </div>
                              <div className="flex-1 text-sm sm:text-base leading-snug pt-0.5">
                                {opt}
                              </div>
                            </button>
                          );
                        })}
                      </div>

                      <div className="flex items-center justify-between pt-4 border-t border-slate-800/80">
                        <button
                          onClick={() => setExamCurrentIdx((prev) => Math.max(0, prev - 1))}
                          disabled={examCurrentIdx === 0}
                          className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl text-xs font-bold border ${
                            examCurrentIdx === 0 ? 'opacity-30 cursor-not-allowed' : ''
                          }`}
                        >
                          <ChevronLeft className="w-4 h-4" /> Previous
                        </button>
                        <button
                          onClick={() => setExamCurrentIdx((prev) => Math.min(examQuestions.length - 1, prev + 1))}
                          disabled={examCurrentIdx === examQuestions.length - 1}
                          className="flex items-center gap-2 px-6 py-2.5 rounded-2xl text-xs font-bold bg-indigo-600 hover:bg-indigo-500 text-white shadow-md"
                        >
                          Next <ChevronRight className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Submit Confirmation Modal */}
            {showSubmitModal && (
              <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
                <div className={`max-w-md w-full p-6 sm:p-8 rounded-3xl border space-y-4 ${
                  darkMode ? 'bg-slate-900 border-slate-800 text-white' : 'bg-white border-slate-200 text-slate-900'
                }`}>
                  <h3 className="text-lg font-black">Submit Exam?</h3>
                  <p className={`text-xs ${darkMode ? 'text-slate-300' : 'text-slate-600'}`}>
                    You have answered {Object.keys(examAnswers).length} out of {examQuestions.length} questions.
                    {examQuestions.length - Object.keys(examAnswers).length > 0 && (
                      <span className="block mt-1 text-amber-400 font-bold">
                        ⚠️ You still have {examQuestions.length - Object.keys(examAnswers).length} unanswered questions!
                      </span>
                    )}
                  </p>
                  <div className="flex items-center justify-end gap-3 pt-3">
                    <button
                      onClick={() => setShowSubmitModal(false)}
                      className="px-4 py-2 rounded-xl text-xs font-bold border border-slate-700"
                    >
                      Cancel & Return
                    </button>
                    <button
                      onClick={() => {
                        setShowSubmitModal(false);
                        setExamFinished(true);
                      }}
                      className="px-5 py-2 rounded-xl bg-rose-600 text-white text-xs font-bold hover:bg-rose-500"
                    >
                      Confirm Submit
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* =========================================
            MODE 4: FLASHCARDS MODE
            ========================================= */}
        {mode === 'flashcards' && (
          <div className="max-w-3xl mx-auto space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-black">Interactive Flashcards</h2>
                <p className={`text-xs ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                  Card {flashcardIdx + 1} of {QUESTION_BANK.length} • Press Space or Click to Flip
                </p>
              </div>
              <button
                onClick={() => {
                  setFlashcardIdx(Math.floor(Math.random() * QUESTION_BANK.length));
                  setIsFlipped(false);
                }}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold ${
                  darkMode ? 'bg-slate-900 border-slate-800 hover:bg-slate-800' : 'bg-white border-slate-300 hover:bg-slate-50'
                }`}
              >
                <Shuffle className="w-3.5 h-3.5 text-indigo-400" />
                <span>Shuffle</span>
              </button>
            </div>

            {/* Flashcard Card */}
            <div
              onClick={() => setIsFlipped(!isFlipped)}
              className={`min-h-[380px] p-8 rounded-3xl border cursor-pointer select-none transition-all duration-300 flex flex-col justify-between ${
                isFlipped
                  ? darkMode
                    ? 'bg-gradient-to-br from-indigo-950/70 via-slate-900 to-cyan-950/40 border-cyan-500/50 shadow-2xl'
                    : 'bg-gradient-to-br from-indigo-50 via-white to-cyan-50 border-cyan-400 shadow-xl'
                  : darkMode
                  ? 'bg-slate-900/95 border-slate-800 hover:border-slate-700 shadow-xl'
                  : 'bg-white border-slate-200 hover:border-slate-300 shadow-lg'
              }`}
            >
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-black px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    Q{activeFlashcard.num}
                  </span>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">
                    {activeFlashcard.category}
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400">
                    {activeFlashcard.difficulty}
                  </span>
                </div>
                <span className="text-[11px] font-bold text-slate-400">
                  {isFlipped ? 'Answer & Explanation' : 'Question Prompt'}
                </span>
              </div>

              {/* Main Face Content */}
              <div className="py-6 flex-1 flex flex-col justify-center">
                {!isFlipped ? (
                  <div className="space-y-4">
                    <p className="text-lg sm:text-xl font-bold leading-relaxed">
                      {activeFlashcard.question}
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-2">
                      {activeFlashcard.options.map((opt, idx) => (
                        <div key={idx} className={`p-2.5 rounded-xl border text-xs ${
                          darkMode ? 'bg-slate-950/60 border-slate-800 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-700'
                        }`}>
                          <span className="font-bold mr-1.5">{['A', 'B', 'C', 'D'][idx]})</span>
                          {opt}
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4 animate-fadeIn">
                    <div className="p-3 rounded-2xl bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 text-sm font-bold flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                      <span>
                        Correct Answer: Option {['A', 'B', 'C', 'D'][activeFlashcard.correct]} ({activeFlashcard.options[activeFlashcard.correct]})
                      </span>
                    </div>
                    <p className="text-xs sm:text-sm leading-relaxed text-slate-300 font-medium">
                      💡 {activeFlashcard.beginnerConcept}
                    </p>
                    <p className="text-xs leading-relaxed text-slate-400">
                      🎯 {activeFlashcard.explanation}
                    </p>
                  </div>
                )}
              </div>

              <div className="flex items-center justify-between text-xs text-slate-500 pt-3 border-t border-slate-800/80">
                <span>Click to Flip Card (or press Space)</span>
                <span>Use [← / →] to navigate</span>
              </div>
            </div>

            {/* Navigation buttons */}
            <div className="flex items-center justify-between">
              <button
                onClick={() => {
                  setFlashcardIdx((prev) => Math.max(0, prev - 1));
                  setIsFlipped(false);
                }}
                disabled={flashcardIdx === 0}
                className="px-5 py-2.5 rounded-2xl border text-xs font-bold flex items-center gap-2"
              >
                <ChevronLeft className="w-4 h-4" /> Previous Card
              </button>
              <button
                onClick={() => {
                  setFlashcardIdx((prev) => Math.min(QUESTION_BANK.length - 1, prev + 1));
                  setIsFlipped(false);
                }}
                disabled={flashcardIdx === QUESTION_BANK.length - 1}
                className="px-6 py-2.5 rounded-2xl bg-indigo-600 text-white font-bold text-xs flex items-center gap-2"
              >
                Next Card <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* =========================================
            MODE 5: QUICK CHEATSHEET MODE
            ========================================= */}
        {mode === 'cheatsheet' && (
          <div className="space-y-6">
            <div className={`p-6 sm:p-8 rounded-3xl border ${
              darkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'
            }`}>
              <h2 className="text-xl font-black">Pre-Interview Quick Cheatsheet</h2>
              <p className={`text-xs sm:text-sm ${darkMode ? 'text-slate-400' : 'text-slate-600'} mt-1`}>
                High-yield formula summaries, ACID properties, join mechanics, and Kimball dimensional modeling rules.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {CHEAT_SHEET_ITEMS.map((item, idx) => (
                <div
                  key={idx}
                  className={`p-6 rounded-3xl border space-y-3 ${
                    darkMode ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                      {item.tag}
                    </span>
                  </div>
                  <h3 className="text-base font-bold text-slate-100">{item.title}</h3>
                  <div className={`text-xs leading-relaxed whitespace-pre-line ${
                    darkMode ? 'text-slate-300 font-mono' : 'text-slate-700'
                  }`}>
                    {item.content}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* FOOTER */}
      <footer className={`mt-16 border-t ${darkMode ? 'bg-slate-950 border-slate-800/80 text-slate-500' : 'bg-white border-slate-200 text-slate-600'} py-8 px-4 text-center text-xs space-y-2`}>
        <p className="font-bold">
          SQL, Data Warehousing & Databricks Master Practice Hub • 200 Questions Bank
        </p>
        <p className="text-[11px] opacity-80">
          Covering 14 Core Domains • Calibrated Easy/Medium/Hard • Virtual Client Scenarios • Medallion & Kimball Architectures
        </p>
      </footer>
    </div>
  );
}
