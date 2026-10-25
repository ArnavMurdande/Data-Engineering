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
  ChevronDown,
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
  Copy,
  Lightbulb,
  Workflow,
  ShieldAlert,
  Compass,
  SlidersHorizontal,
  Terminal,
  Gauge
} from 'lucide-react';

import { QUESTION_BANK } from './data/questions.js';
import { CATEGORIES, DIFFICULTIES } from './data/categories.js';
import { CHEAT_SHEET_ITEMS } from './data/cheatsheet.js';
import { CONCEPTS_DATA } from './data/concepts.js';
import CustomDropdown from './components/CustomDropdown.jsx';

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
  const [showMobilePalette, setShowMobilePalette] = useState(false);
  const [showExamMobilePalette, setShowExamMobilePalette] = useState(false);

  const [darkMode, setDarkMode] = useState(() => {
    try {
      const saved = localStorage.getItem('de_mcq_dark_mode');
      return saved !== null ? JSON.parse(saved) : false; // Default to vibrant Neo-Brutalist Light Mode
    } catch {
      return false;
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
      if (darkMode) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
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

  const questionCardRef = useRef(null);

  // Category counts
  const categoryCountMap = useMemo(() => {
    const counts = { "All Topics": QUESTION_BANK.length };
    QUESTION_BANK.forEach((q) => {
      counts[q.category] = (counts[q.category] || 0) + 1;
    });
    return counts;
  }, []);

  // Formatted dropdown options
  const categoryDropdownOptions = useMemo(() => {
    return CATEGORIES.map((cat) => ({
      value: cat,
      label: cat,
      count: categoryCountMap[cat] || 0
    }));
  }, [categoryCountMap]);

  const difficultyDropdownOptions = useMemo(() => {
    return DIFFICULTIES.map((diff) => ({
      value: diff,
      label: diff
    }));
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

  const scrollToQuestionCard = () => {
    if (questionCardRef.current) {
      const headerOffset = 115;
      const elementPosition = questionCardRef.current.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({
        top: Math.max(0, offsetPosition),
        behavior: 'smooth'
      });
    }
  };

  const handleNext = () => {
    if (currentIndex < filteredQuestions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      scrollToQuestionCard();
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
      scrollToQuestionCard();
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
      if (!catStats[q.category]) catStats[q.category] = { total: 0, correct: 0 };
      catStats[q.category].total += 1;

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
    <div className={`min-h-screen font-sans ${
      darkMode ? 'bg-[#0B0F17] text-slate-100' : 'bg-[#F9F7F2] text-slate-900'
    } transition-colors duration-150`}>
      {/* =========================================
          NEO-BRUTALIST TWO-TIER HEADER NAVBAR
          ========================================= */}
      <header className={`sticky top-0 z-40 border-b-[3px] backdrop-blur-md px-3 sm:px-6 py-2 transition-colors ${
        darkMode 
          ? 'bg-[#0F172A]/95 border-slate-700 shadow-[0_4px_0_0_#1E293B]' 
          : 'bg-white border-black shadow-[0_4px_0_0_#000000]'
      }`}>
        <div className="max-w-7xl mx-auto space-y-2">
          {/* TIER 1: BRAND IDENTITY + STATS + THEME TOGGLE */}
          <div className="flex items-center justify-between gap-2">
            {/* Logo & Neo-Brutalist Title */}
            <div className="flex items-center gap-2.5 min-w-0">
              <div className={`w-9 h-9 sm:w-10 sm:h-10 rounded-xl sm:rounded-2xl flex items-center justify-center font-black shrink-0 transition-all ${
                darkMode
                  ? 'bg-amber-400 text-black border-2 border-slate-700 shadow-[2px_2px_0px_#0284c7]'
                  : 'bg-amber-300 text-black border-[2.5px] border-black shadow-[2.5px_2.5px_0px_#000000]'
              }`}>
                <Database className="w-5 h-5 stroke-[2.5]" />
              </div>
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <h1 className="text-sm sm:text-lg font-black tracking-tight leading-none truncate">
                    SQL & Databricks Master
                  </h1>
                  <span className={`text-[9px] sm:text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full border-2 shrink-0 ${
                    darkMode
                      ? 'bg-cyan-400 text-black border-slate-700 shadow-[1.5px_1.5px_0px_#0284c7]'
                      : 'bg-yellow-300 text-black border-black shadow-[1.5px_1.5px_0px_#000000]'
                  }`}>
                    200 MCQs
                  </span>
                </div>
                <p className={`text-[11px] font-bold ${darkMode ? 'text-slate-400' : 'text-slate-600'} hidden md:block mt-0.5 truncate`}>
                  SQL Mastery • Query Optimization • Medallion Lakehouse • Kimball Modeling • SCD Types 1-6
                </p>
              </div>
            </div>

            {/* Right Controls: Stats Pill & Dark Mode Toggle */}
            <div className="flex items-center gap-2 shrink-0">
              <div className={`flex items-center gap-1.5 px-2.5 py-1 sm:px-3 sm:py-1 rounded-xl sm:rounded-2xl border-2 text-[11px] sm:text-xs font-black shrink-0 ${
                darkMode
                  ? 'bg-slate-900 border-slate-700 text-amber-300 shadow-[2px_2px_0px_#0284c7]'
                  : 'bg-amber-100 border-black text-black shadow-[2px_2px_0px_#000000]'
              }`}>
                <Flame className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-orange-500 fill-current" />
                <span>
                  <span className="sm:hidden">{totalCorrect}/{totalAnswered} ({overallAccuracy}%)</span>
                  <span className="hidden sm:inline">{totalCorrect}/{totalAnswered} Correct ({overallAccuracy}%)</span>
                </span>
              </div>

              <button
                onClick={() => setDarkMode(!darkMode)}
                className={`p-1.5 sm:p-2 rounded-xl sm:rounded-2xl border-2 font-black transition-all neo-btn shrink-0 ${
                  darkMode
                    ? 'bg-slate-900 border-slate-700 text-amber-400 shadow-[2px_2px_0px_#eab308]'
                    : 'bg-white border-black text-black shadow-[2px_2px_0px_#000000] hover:bg-amber-100'
                }`}
                title="Toggle Dark / Light Mode"
                aria-label="Toggle Theme"
              >
                {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* TIER 2: DEDICATED FULL-WIDTH NAVIGATION BAR (ALL 5 TABS GUARANTEED 100% VISIBLE) */}
          <nav 
            aria-label="Primary Modes"
            className={`w-full p-1 sm:p-1.5 rounded-xl sm:rounded-2xl border-2 transition-all ${
              darkMode 
                ? 'bg-slate-900 border-slate-700 shadow-[2.5px_2.5px_0px_#0284c7]' 
                : 'bg-slate-100 border-black shadow-[2.5px_2.5px_0px_#000000]'
            }`}
          >
            <div className="grid grid-cols-5 gap-1 sm:gap-2">
              {/* Tab 1: Practice & Learn */}
              <button
                onClick={() => setMode('practice')}
                className={`flex items-center justify-center gap-1.5 py-1.5 sm:py-2 px-1 sm:px-3 rounded-lg sm:rounded-xl text-[11px] sm:text-xs font-black transition-all border-2 select-none neo-btn ${
                  mode === 'practice'
                    ? darkMode
                      ? 'bg-cyan-400 text-black border-cyan-300 shadow-[2px_2px_0px_#FFF]'
                      : 'bg-amber-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]'
                    : darkMode
                    ? 'border-transparent text-slate-300 hover:text-white hover:bg-slate-800'
                    : 'border-transparent text-slate-700 hover:text-black hover:bg-amber-100'
                }`}
              >
                <BookOpen className="w-3.5 h-3.5 sm:w-4 sm:h-4 stroke-[2.5] shrink-0" />
                <span className="truncate">
                  <span className="md:hidden">Practice</span>
                  <span className="hidden md:inline">Practice & Learn</span>
                </span>
              </button>

              {/* Tab 2: Concept Hub */}
              <button
                onClick={() => setMode('concepts')}
                className={`flex items-center justify-center gap-1.5 py-1.5 sm:py-2 px-1 sm:px-3 rounded-lg sm:rounded-xl text-[11px] sm:text-xs font-black transition-all border-2 select-none neo-btn ${
                  mode === 'concepts'
                    ? darkMode
                      ? 'bg-emerald-400 text-black border-emerald-300 shadow-[2px_2px_0px_#FFF]'
                      : 'bg-emerald-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]'
                    : darkMode
                    ? 'border-transparent text-slate-300 hover:text-white hover:bg-slate-800'
                    : 'border-transparent text-slate-700 hover:text-black hover:bg-amber-100'
                }`}
              >
                <Layers className="w-3.5 h-3.5 sm:w-4 sm:h-4 stroke-[2.5] shrink-0" />
                <span className="truncate">
                  <span className="md:hidden">Concepts</span>
                  <span className="hidden md:inline">Concept Hub</span>
                </span>
                <span className={`hidden sm:inline-block text-[9px] px-1.5 py-0.2 rounded-full font-black border shrink-0 ${
                  darkMode ? 'bg-cyan-400 text-black border-cyan-300' : 'bg-black text-white border-black'
                }`}>NEW</span>
              </button>

              {/* Tab 3: Exam Simulator */}
              <button
                onClick={() => setMode('exam')}
                className={`flex items-center justify-center gap-1.5 py-1.5 sm:py-2 px-1 sm:px-3 rounded-lg sm:rounded-xl text-[11px] sm:text-xs font-black transition-all border-2 select-none neo-btn ${
                  mode === 'exam'
                    ? darkMode
                      ? 'bg-orange-400 text-black border-orange-300 shadow-[2px_2px_0px_#FFF]'
                      : 'bg-orange-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]'
                    : darkMode
                    ? 'border-transparent text-slate-300 hover:text-white hover:bg-slate-800'
                    : 'border-transparent text-slate-700 hover:text-black hover:bg-amber-100'
                }`}
              >
                <Timer className="w-3.5 h-3.5 sm:w-4 sm:h-4 stroke-[2.5] shrink-0" />
                <span className="truncate">
                  <span className="md:hidden">Exam</span>
                  <span className="hidden md:inline">Exam Simulator</span>
                </span>
              </button>

              {/* Tab 4: Flashcards */}
              <button
                onClick={() => setMode('flashcards')}
                className={`flex items-center justify-center gap-1.5 py-1.5 sm:py-2 px-1 sm:px-3 rounded-lg sm:rounded-xl text-[11px] sm:text-xs font-black transition-all border-2 select-none neo-btn ${
                  mode === 'flashcards'
                    ? darkMode
                      ? 'bg-sky-400 text-black border-sky-300 shadow-[2px_2px_0px_#FFF]'
                      : 'bg-sky-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]'
                    : darkMode
                    ? 'border-transparent text-slate-300 hover:text-white hover:bg-slate-800'
                    : 'border-transparent text-slate-700 hover:text-black hover:bg-amber-100'
                }`}
              >
                <RotateCcw className="w-3.5 h-3.5 sm:w-4 sm:h-4 stroke-[2.5] shrink-0" />
                <span className="truncate">
                  <span className="sm:hidden">Cards</span>
                  <span className="hidden sm:inline">Flashcards</span>
                </span>
              </button>

              {/* Tab 5: Cheatsheet */}
              <button
                onClick={() => setMode('cheatsheet')}
                className={`flex items-center justify-center gap-1.5 py-1.5 sm:py-2 px-1 sm:px-3 rounded-lg sm:rounded-xl text-[11px] sm:text-xs font-black transition-all border-2 select-none neo-btn ${
                  mode === 'cheatsheet'
                    ? darkMode
                      ? 'bg-yellow-400 text-black border-yellow-300 shadow-[2px_2px_0px_#FFF]'
                      : 'bg-lime-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]'
                    : darkMode
                    ? 'border-transparent text-slate-300 hover:text-white hover:bg-slate-800'
                    : 'border-transparent text-slate-700 hover:text-black hover:bg-amber-100'
                }`}
              >
                <FileText className="w-3.5 h-3.5 sm:w-4 sm:h-4 stroke-[2.5] shrink-0" />
                <span className="truncate">
                  <span className="sm:hidden">Cheat</span>
                  <span className="hidden sm:inline">Cheatsheet</span>
                </span>
              </button>
            </div>
          </nav>
        </div>
      </header>

      {/* =========================================
          MAIN CONTAINER
          ========================================= */}
      <main className="max-w-7xl mx-auto p-4 sm:p-6 space-y-6">

        {/* =========================================
            MODE 1: PRACTICE & LEARN MODE
            ========================================= */}
        {mode === 'practice' && (
          <div className="space-y-4 lg:space-y-0">
            {/* Mobile-only Quick Status & Palette Toggle Bar */}
            <div className={`lg:hidden p-3.5 rounded-2xl border-2 flex items-center justify-between gap-2.5 transition-all mb-4 ${
              darkMode
                ? 'bg-slate-900 border-slate-700 text-slate-100 shadow-[3px_3px_0px_#0284c7]'
                : 'bg-white border-black text-slate-900 shadow-[3px_3px_0px_#000000]'
            }`}>
              <div className="flex items-center gap-2 truncate">
                <span className={`text-xs font-black px-2.5 py-0.5 rounded-xl border-2 shrink-0 ${
                  darkMode ? 'bg-cyan-400 text-black border-slate-700' : 'bg-yellow-300 text-black border-black shadow-[1.5px_1.5px_0px_#000]'
                }`}>
                  Q{currentQ ? currentQ.num : 1}/200
                </span>
                <span className="text-xs font-black truncate">
                  {currentQ?.category || "Practice"}
                </span>
              </div>

              <button
                onClick={() => setShowMobilePalette(!showMobilePalette)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-black border-2 shrink-0 transition-all neo-btn ${
                  showMobilePalette
                    ? 'bg-amber-300 text-black border-black shadow-[2px_2px_0px_#000]'
                    : darkMode
                    ? 'bg-slate-950 border-slate-700 text-cyan-300 hover:text-white'
                    : 'bg-amber-100 border-black text-black shadow-[2px_2px_0px_#000]'
                }`}
              >
                <ListFilter className="w-3.5 h-3.5" />
                <span>{showMobilePalette ? 'Close' : 'Palette (200)'}</span>
                <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-200 ${showMobilePalette ? 'rotate-180' : ''}`} />
              </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              {/* Left Sidebar: Filters & Question Palette (Permanent on laptop lg:block, toggled on mobile) */}
              <div className={`${showMobilePalette ? 'block' : 'hidden lg:block'} lg:col-span-1 space-y-5 order-2 lg:order-1`}>
              {/* Filter Card */}
              <div className={`p-5 rounded-3xl border-[2.5px] space-y-4 ${
                darkMode ? 'bg-slate-900 border-slate-700 shadow-[4px_4px_0px_#0284c7]' : 'bg-white border-black shadow-[4px_4px_0px_#000000]'
              }`}>
                <div className="flex items-center justify-between pb-2 border-b-2 border-black/10 dark:border-slate-800">
                  <h3 className="text-xs font-black uppercase tracking-wider flex items-center gap-2">
                    <Filter className="w-4 h-4 text-amber-500" /> Filters & Navigation
                  </h3>
                  <span className={`text-[11px] font-black px-2.5 py-0.5 rounded-full border-2 ${
                    darkMode
                      ? 'bg-cyan-950 text-cyan-300 border-cyan-400'
                      : 'bg-yellow-300 text-black border-black shadow-[1.5px_1.5px_0px_#000]'
                  }`}>
                    {filteredQuestions.length} / 200
                  </span>
                </div>

                {/* Search Box */}
                <div className="relative">
                  <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Search keywords, topics..."
                    value={searchQuery}
                    onChange={(e) => {
                      setSearchQuery(e.target.value);
                      setCurrentIndex(0);
                    }}
                    className={`w-full pl-10 pr-3 py-2.5 text-xs font-bold rounded-2xl border-2 transition focus:outline-none ${
                      darkMode
                        ? 'bg-slate-950 border-slate-700 text-slate-100 focus:border-cyan-400 shadow-[2px_2px_0px_#0284c7]'
                        : 'bg-white border-black text-black placeholder:text-slate-400 focus:border-black focus:ring-2 focus:ring-amber-300 shadow-[2.5px_2.5px_0px_#000]'
                    }`}
                  />
                </div>

                {/* Rounded Custom Category Dropdown */}
                <CustomDropdown
                  label="Filter by Domain:"
                  value={selectedCategory}
                  options={categoryDropdownOptions}
                  onChange={(val) => {
                    setSelectedCategory(val);
                    setCurrentIndex(0);
                  }}
                  icon={Layers}
                  darkMode={darkMode}
                  accentColor="yellow"
                />

                {/* Rounded Custom Difficulty Dropdown */}
                <CustomDropdown
                  label="Filter by Difficulty:"
                  value={selectedDifficulty}
                  options={difficultyDropdownOptions}
                  onChange={(val) => {
                    setSelectedDifficulty(val);
                    setCurrentIndex(0);
                  }}
                  icon={Gauge}
                  darkMode={darkMode}
                  accentColor="emerald"
                />

                {/* Difficulty Quick Select Pills */}
                <div>
                  <div className="grid grid-cols-4 gap-1.5 pt-1">
                    {DIFFICULTIES.map((diff) => {
                      const isSelected = selectedDifficulty === diff;
                      let activeStyle = darkMode
                        ? 'bg-cyan-400 text-black border-slate-700 shadow-[2px_2px_0px_#FFF]'
                        : 'bg-amber-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]';

                      if (diff === 'Easy' && isSelected) {
                        activeStyle = darkMode ? 'bg-emerald-400 text-black border-slate-700' : 'bg-emerald-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]';
                      } else if (diff === 'Medium' && isSelected) {
                        activeStyle = darkMode ? 'bg-amber-400 text-black border-slate-700' : 'bg-yellow-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]';
                      } else if (diff === 'Hard' && isSelected) {
                        activeStyle = darkMode ? 'bg-rose-400 text-black border-slate-700' : 'bg-rose-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]';
                      }

                      return (
                        <button
                          key={diff}
                          onClick={() => {
                            setSelectedDifficulty(diff);
                            setCurrentIndex(0);
                          }}
                          className={`py-1.5 text-[10px] rounded-xl font-black transition-all text-center border-2 neo-btn ${
                            isSelected
                              ? activeStyle
                              : darkMode
                              ? 'bg-slate-950 border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800'
                              : 'bg-white border-black text-slate-700 hover:bg-amber-50 shadow-[1.5px_1.5px_0px_#000]'
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
                  className={`w-full py-2.5 px-3 rounded-2xl text-xs font-black flex items-center justify-between border-2 transition-all neo-btn ${
                    showOnlyScenarios
                      ? darkMode
                        ? 'bg-amber-400 text-black border-amber-300 shadow-[3px_3px_0px_#FFF]'
                        : 'bg-amber-300 text-black border-black shadow-[3px_3px_0px_#000000]'
                      : darkMode
                      ? 'bg-slate-950 border-slate-700 text-slate-300 hover:bg-slate-800'
                      : 'bg-white border-black text-slate-900 hover:bg-amber-50 shadow-[2px_2px_0px_#000]'
                  }`}
                >
                  <span className="flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-amber-600 fill-current" />
                    <span>Client Virtual Scenarios</span>
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-black text-white font-black">
                    20
                  </span>
                </button>

                {/* Starred & Missed Buttons */}
                <div className="grid grid-cols-2 gap-2 pt-2 border-t border-black/10 dark:border-slate-800">
                  <button
                    onClick={() => {
                      setShowOnlyBookmarks(!showOnlyBookmarks);
                      setCurrentIndex(0);
                    }}
                    className={`py-2 px-2.5 rounded-2xl text-xs font-black flex items-center justify-center gap-1.5 border-2 transition-all neo-btn ${
                      showOnlyBookmarks
                        ? 'bg-amber-300 text-black border-black shadow-[2px_2px_0px_#000]'
                        : darkMode
                        ? 'bg-slate-950 border-slate-700 text-slate-300 hover:bg-slate-800'
                        : 'bg-white border-black text-slate-800 hover:bg-amber-50 shadow-[2px_2px_0px_#000]'
                    }`}
                  >
                    <Bookmark className={`w-3.5 h-3.5 ${showOnlyBookmarks ? 'fill-current text-black' : ''}`} />
                    <span>Starred ({bookmarkedIds.size})</span>
                  </button>

                  <button
                    onClick={() => {
                      setShowOnlyMissed(!showOnlyMissed);
                      setCurrentIndex(0);
                    }}
                    className={`py-2 px-2.5 rounded-2xl text-xs font-black flex items-center justify-center gap-1.5 border-2 transition-all neo-btn ${
                      showOnlyMissed
                        ? 'bg-rose-300 text-black border-black shadow-[2px_2px_0px_#000]'
                        : darkMode
                        ? 'bg-slate-950 border-slate-700 text-slate-300 hover:bg-slate-800'
                        : 'bg-white border-black text-slate-800 hover:bg-rose-50 shadow-[2px_2px_0px_#000]'
                    }`}
                  >
                    <XCircle className="w-3.5 h-3.5 text-rose-500" />
                    <span>Missed ({totalIncorrect})</span>
                  </button>
                </div>
              </div>

              {/* Question Navigator Grid */}
              <div className={`p-5 rounded-3xl border-[2.5px] space-y-3 ${
                darkMode ? 'bg-slate-900 border-slate-700 shadow-[4px_4px_0px_#0284c7]' : 'bg-white border-black shadow-[4px_4px_0px_#000000]'
              }`}>
                <div className="flex items-center justify-between pb-1 border-b border-black/10 dark:border-slate-800">
                  <h4 className="text-xs font-black uppercase tracking-wider">
                    Question Palette
                  </h4>
                  <span className="text-[10px] font-bold text-slate-400">
                    200 Questions
                  </span>
                </div>

                {/* Status Legend */}
                <div className="flex flex-wrap items-center gap-2 text-[10px] font-black text-slate-500 pb-1">
                  <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-md bg-emerald-400 border border-black inline-block"></span> Pass</span>
                  <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-md bg-rose-400 border border-black inline-block"></span> Miss</span>
                  <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-md bg-amber-300 border border-black inline-block"></span> Star</span>
                </div>

                {/* Grid */}
                <div className="max-h-72 overflow-y-auto p-1 pr-2 grid grid-cols-5 gap-1.5 scrollbar-thin">
                  {filteredQuestions.map((q, idx) => {
                    const isAnswered = userAnswers[q.id] !== undefined;
                    const isCorrect = userAnswers[q.id] === q.correct;
                    const isCurrent = idx === currentIndex;
                    const isStarred = bookmarkedIds.has(q.id);

                    let btnClass = darkMode
                      ? 'bg-slate-950 text-slate-400 border-2 border-slate-800 hover:border-slate-600'
                      : 'bg-white text-slate-800 border-2 border-black hover:bg-amber-100 shadow-[2px_2px_0px_#000]';

                    if (isAnswered) {
                      btnClass = isCorrect
                        ? 'bg-emerald-400 text-black font-black border-2 border-black shadow-[2px_2px_0px_#000]'
                        : 'bg-rose-400 text-black font-black border-2 border-black shadow-[2px_2px_0px_#000]';
                    }

                    if (isCurrent) {
                      btnClass = darkMode
                        ? 'bg-cyan-400 text-black font-black border-2 border-white shadow-[3px_3px_0px_#FFF]'
                        : 'bg-amber-300 text-black font-black border-[2.5px] border-black shadow-[3px_3px_0px_#000] ring-2 ring-black';
                    }

                    return (
                      <button
                        key={q.id}
                        onClick={() => {
                          setCurrentIndex(idx);
                          setShowMobilePalette(false);
                          scrollToQuestionCard();
                        }}
                        className={`h-9 rounded-xl text-xs font-black flex items-center justify-center relative transition-all neo-btn ${btnClass}`}
                        title={`Q${q.num} [${q.difficulty}]: ${q.topic}`}
                      >
                        {q.num}
                        {isStarred && (
                          <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-amber-400 border border-black rounded-full" />
                        )}
                        <span className={`absolute bottom-0.5 right-1 w-1.5 h-1.5 rounded-full ${
                          q.difficulty === 'Easy' ? 'bg-emerald-500' : q.difficulty === 'Hard' ? 'bg-rose-500' : 'bg-amber-500'
                        }`} />
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Active Question Main Card */}
            <div className="lg:col-span-3 space-y-4 order-1 lg:order-2 scroll-mt-36" ref={questionCardRef}>
              {filteredQuestions.length === 0 ? (
                <div className={`p-12 text-center rounded-3xl border-[2.5px] space-y-4 ${
                  darkMode ? 'bg-slate-900 border-slate-700' : 'bg-white border-black shadow-[4px_4px_0px_#000]'
                }`}>
                  <AlertCircle className="w-12 h-12 text-amber-500 mx-auto" />
                  <h3 className="text-xl font-black">No Questions Match Active Filter</h3>
                  <p className="text-xs text-slate-500 max-w-md mx-auto">
                    Try clearing difficulty or scenario filters to explore all 200 questions.
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
                    className="px-6 py-2.5 rounded-2xl bg-amber-300 text-black font-black border-2 border-black shadow-[3px_3px_0px_#000] neo-btn"
                  >
                    Reset All Filters
                  </button>
                </div>
              ) : currentQ ? (
                <div className={`p-6 sm:p-8 rounded-3xl border-[2.5px] space-y-6 ${
                  darkMode
                    ? 'bg-slate-900 border-slate-700 shadow-[5px_5px_0px_#0284c7]'
                    : 'bg-white border-black shadow-[5px_5px_0px_#000000]'
                }`}>
                  {/* Badges & Header Bar */}
                  <div className="flex flex-wrap items-center justify-between gap-2.5 pb-4 border-b-2 border-black/10 dark:border-slate-800">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`px-3 py-1 rounded-xl text-xs font-black border-2 ${
                        darkMode ? 'bg-cyan-400 text-black border-slate-700' : 'bg-yellow-300 text-black border-black shadow-[2px_2px_0px_#000]'
                      }`}>
                        Question {currentQ.num} of 200
                      </span>

                      <span className={`px-3 py-1 rounded-xl text-xs font-black border-2 ${
                        darkMode ? 'bg-slate-800 text-slate-200 border-slate-700' : 'bg-slate-100 text-black border-black shadow-[1.5px_1.5px_0px_#000]'
                      }`}>
                        {currentQ.category}
                      </span>

                      {/* Difficulty Badge */}
                      <span className={`px-2.5 py-1 rounded-xl text-xs font-black border-2 ${
                        currentQ.difficulty === 'Easy'
                          ? 'bg-emerald-300 text-black border-black shadow-[2px_2px_0px_#000]'
                          : currentQ.difficulty === 'Hard'
                          ? 'bg-rose-300 text-black border-black shadow-[2px_2px_0px_#000]'
                          : 'bg-amber-300 text-black border-black shadow-[2px_2px_0px_#000]'
                      }`}>
                        {currentQ.difficulty}
                      </span>

                      {/* Scenario Badge */}
                      {currentQ.isScenario && (
                        <span className="px-2.5 py-1 rounded-xl text-xs font-black border-2 bg-amber-300 text-black border-black shadow-[2px_2px_0px_#000] flex items-center gap-1">
                          <Sparkles className="w-3.5 h-3.5 text-amber-700 fill-current" />
                          <span>{currentQ.scenarioTitle || "Client Scenario"}</span>
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => toggleBookmark(currentQ.id)}
                        className={`p-2.5 rounded-xl border-2 font-black transition-all neo-btn ${
                          bookmarkedIds.has(currentQ.id)
                            ? 'bg-amber-300 text-black border-black shadow-[2.5px_2.5px_0px_#000]'
                            : darkMode
                            ? 'bg-slate-950 border-slate-700 text-slate-400'
                            : 'bg-white border-black text-black shadow-[2px_2px_0px_#000]'
                        }`}
                        title="Bookmark / Star"
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
                        className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-black border-2 transition-all neo-btn ${
                          showExplanation[currentQ.id]
                            ? 'bg-black text-white border-black shadow-[2px_2px_0px_#000]'
                            : darkMode
                            ? 'bg-slate-800 border-slate-700 text-slate-200'
                            : 'bg-amber-200 border-black text-black shadow-[2px_2px_0px_#000]'
                        }`}
                      >
                        <HelpCircle className="w-3.5 h-3.5" />
                        <span>{showExplanation[currentQ.id] ? 'Hide Solution' : 'Reveal Solution'}</span>
                      </button>
                    </div>
                  </div>

                  {/* Question Stem */}
                  <div className={`text-base sm:text-lg font-black leading-relaxed tracking-tight ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                    {currentQ.question}
                  </div>

                  {/* Options List with Tactile Cards */}
                  <div className="space-y-3">
                    {currentQ.options.map((option, idx) => {
                      const isSelected = userAnswers[currentQ.id] === idx;
                      const hasAnswered = userAnswers[currentQ.id] !== undefined;
                      const isCorrect = idx === currentQ.correct;

                      let optClass = darkMode
                        ? 'border-2 border-slate-700 bg-slate-950/80 text-slate-200 hover:border-slate-500 shadow-[3px_3px_0px_#0284c7]'
                        : 'border-[2.5px] border-black bg-white text-black hover:bg-amber-50 shadow-[3px_3px_0px_#000000]';

                      if (hasAnswered) {
                        if (isCorrect) {
                          optClass = darkMode
                            ? 'border-2 border-emerald-400 bg-emerald-950/80 text-emerald-200 shadow-[4px_4px_0px_#10B981]'
                            : 'border-[2.5px] border-black bg-emerald-300 text-black font-black shadow-[4px_4px_0px_#000]';
                        } else if (isSelected && !isCorrect) {
                          optClass = darkMode
                            ? 'border-2 border-rose-400 bg-rose-950/80 text-rose-200 shadow-[4px_4px_0px_#F43F5E]'
                            : 'border-[2.5px] border-black bg-rose-300 text-black font-black shadow-[4px_4px_0px_#000]';
                        }
                      }

                      return (
                        <button
                          key={idx}
                          onClick={() => handleSelectOption(currentQ.id, idx)}
                          className={`w-full text-left p-4 rounded-2xl transition-all duration-150 flex items-start gap-3.5 neo-btn ${optClass}`}
                        >
                          <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-black shrink-0 mt-0.5 border-2 ${
                            hasAnswered && isCorrect
                              ? 'bg-black text-white border-black'
                              : hasAnswered && isSelected && !isCorrect
                              ? 'bg-black text-white border-black'
                              : darkMode
                              ? 'bg-slate-800 border-slate-600 text-white'
                              : 'bg-yellow-300 border-black text-black'
                          }`}>
                            {hasAnswered && isCorrect ? (
                              <Check className="w-4 h-4 stroke-[3]" />
                            ) : hasAnswered && isSelected && !isCorrect ? (
                              <X className="w-4 h-4 stroke-[3]" />
                            ) : (
                              ['A', 'B', 'C', 'D'][idx]
                            )}
                          </div>
                          <div className="flex-1 text-sm sm:text-base font-extrabold leading-snug pt-1">
                            {option}
                          </div>
                        </button>
                      );
                    })}
                  </div>

                  {/* Multi-Tab Solution & Architecture Blueprint */}
                  {(showExplanation[currentQ.id] || userAnswers[currentQ.id] !== undefined) && (
                    <div className={`p-6 rounded-3xl border-[2.5px] space-y-4 ${
                      darkMode ? 'bg-slate-950 border-slate-700 shadow-[5px_5px_0px_#0284c7]' : 'bg-[#FFFBEB] border-black shadow-[5px_5px_0px_#000000]'
                    }`}>
                      {/* Solution Tabs */}
                      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b-2 border-black/10 dark:border-slate-800">
                        <div className="flex items-center gap-2">
                          <span className="w-3 h-3 rounded-full bg-amber-400 border border-black inline-block" />
                          <span className="text-xs font-black uppercase tracking-wider">
                            Comprehensive Solution & Visuals
                          </span>
                        </div>

                        {/* Tabs */}
                        <div className="grid grid-cols-2 sm:flex items-center gap-1.5 p-1 rounded-2xl border-2 border-black bg-white dark:bg-slate-900 dark:border-slate-700">
                          <button
                            onClick={() => setActiveSolutionTab('intuition')}
                            className={`px-3 py-1.5 text-xs font-black rounded-xl transition ${
                              activeSolutionTab === 'intuition' ? 'bg-amber-300 text-black border border-black shadow-[1.5px_1.5px_0px_#000]' : 'text-slate-600 dark:text-slate-400'
                            }`}
                          >
                            💡 Intuition
                          </button>
                          <button
                            onClick={() => setActiveSolutionTab('visual')}
                            className={`px-3 py-1.5 text-xs font-black rounded-xl transition ${
                              activeSolutionTab === 'visual' ? 'bg-sky-300 text-black border border-black shadow-[1.5px_1.5px_0px_#000]' : 'text-slate-600 dark:text-slate-400'
                            }`}
                          >
                            📐 Blueprint
                          </button>
                          <button
                            onClick={() => setActiveSolutionTab('technical')}
                            className={`px-3 py-1.5 text-xs font-black rounded-xl transition ${
                              activeSolutionTab === 'technical' ? 'bg-emerald-300 text-black border border-black shadow-[1.5px_1.5px_0px_#000]' : 'text-slate-600 dark:text-slate-400'
                            }`}
                          >
                            🎯 Technical
                          </button>
                          <button
                            onClick={() => setActiveSolutionTab('tip')}
                            className={`px-3 py-1.5 text-xs font-black rounded-xl transition ${
                              activeSolutionTab === 'tip' ? 'bg-orange-300 text-black border border-black shadow-[1.5px_1.5px_0px_#000]' : 'text-slate-600 dark:text-slate-400'
                            }`}
                          >
                            💼 Client Tip
                          </button>
                        </div>
                      </div>

                      {/* Correct Answer Header */}
                      <div className={`p-3.5 rounded-2xl border-2 flex items-center justify-between ${
                        darkMode ? 'bg-emerald-950/60 border-emerald-400 text-emerald-200' : 'bg-emerald-300 border-black text-black font-black shadow-[2px_2px_0px_#000]'
                      }`}>
                        <div className="flex items-center gap-2 font-black text-sm">
                          <CheckCircle2 className="w-5 h-5 shrink-0 stroke-[2.5]" />
                          <span>Correct Answer: Option {['A', 'B', 'C', 'D'][currentQ.correct]}</span>
                        </div>
                        <span className="text-xs font-bold truncate max-w-sm hidden sm:inline">
                          "{currentQ.options[currentQ.correct]}"
                        </span>
                      </div>

                      {/* Tab 1: Intuition */}
                      {activeSolutionTab === 'intuition' && (
                        <div className="space-y-2">
                          <span className={`text-xs font-black uppercase flex items-center gap-1.5 ${darkMode ? 'text-amber-400' : 'text-amber-700'}`}>
                            <Lightbulb className="w-4 h-4 text-amber-500" /> Beginner Mental Model
                          </span>
                          <p className={`text-xs sm:text-sm font-semibold leading-relaxed ${darkMode ? 'text-amber-100' : 'text-slate-800'}`}>
                            {currentQ.beginnerConcept}
                          </p>
                        </div>
                      )}

                      {/* Tab 2: Visual Diagram */}
                      {activeSolutionTab === 'visual' && (
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className={`text-xs font-black uppercase flex items-center gap-1.5 ${darkMode ? 'text-cyan-400' : 'text-sky-700'}`}>
                              <Workflow className="w-4 h-4" /> Execution Architecture & Data Flow
                            </span>
                            <button
                              onClick={() => handleCopyCode(currentQ.visualDiagram, currentQ.id)}
                              className={`text-[11px] px-2.5 py-1 rounded-xl border-2 font-black neo-btn ${
                                darkMode ? 'border-slate-700 bg-slate-800 text-cyan-300' : 'border-black bg-white text-black shadow-[1.5px_1.5px_0px_#000]'
                              }`}
                            >
                              {copiedCodeId === currentQ.id ? 'Copied!' : 'Copy Blueprint'}
                            </button>
                          </div>
                          <pre className={`p-4 rounded-2xl text-[10.5px] sm:text-xs font-mono border-2 overflow-x-auto no-scrollbar touch-pan-x leading-relaxed ${
                            darkMode ? 'bg-black border-slate-700 text-cyan-300' : 'bg-slate-900 border-black text-cyan-200 shadow-[3px_3px_0px_#000]'
                          }`}>
                            {currentQ.visualDiagram}
                          </pre>
                          <span className="text-[10px] font-bold text-slate-400 dark:text-slate-500 block sm:hidden">
                            👉 Swipe diagram horizontally to explore full architecture
                          </span>
                        </div>
                      )}

                      {/* Tab 3: Technical Explanation */}
                      {activeSolutionTab === 'technical' && (
                        <div className="space-y-2">
                          <span className={`text-xs font-black uppercase flex items-center gap-1.5 ${darkMode ? 'text-emerald-400' : 'text-emerald-800'}`}>
                            <Cpu className="w-4 h-4 text-emerald-500" /> Deep Technical Rationale
                          </span>
                          <p className={`text-xs sm:text-sm font-medium leading-relaxed ${darkMode ? 'text-slate-200' : 'text-slate-800'}`}>
                            {currentQ.explanation}
                          </p>
                        </div>
                      )}

                      {/* Tab 4: Client Pro-Tip */}
                      {activeSolutionTab === 'tip' && (
                        <div className="space-y-2">
                          <span className={`text-xs font-black uppercase flex items-center gap-1.5 ${darkMode ? 'text-orange-400' : 'text-orange-700'}`}>
                            <Award className="w-4 h-4 text-orange-500" /> Client Round Strategy
                          </span>
                          <p className={`text-xs sm:text-sm font-medium leading-relaxed ${darkMode ? 'text-orange-100' : 'text-slate-800'}`}>
                            {currentQ.interviewTip}
                          </p>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Navigation Bar */}
                  <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t-2 border-black/10 dark:border-slate-800">
                    <div className="grid grid-cols-2 gap-3 w-full sm:w-auto">
                      <button
                        onClick={handlePrev}
                        disabled={currentIndex === 0}
                        className={`flex items-center justify-center gap-2 px-5 py-2.5 rounded-2xl text-xs font-black border-2 transition-all select-none ${
                          currentIndex === 0
                            ? darkMode
                              ? 'bg-slate-900 border-slate-800 text-slate-500 cursor-not-allowed opacity-50 shadow-none'
                              : 'bg-slate-100 border-slate-300 text-slate-400 cursor-not-allowed opacity-50 shadow-none'
                            : darkMode
                            ? 'bg-slate-800 border-slate-700 text-slate-100 shadow-[2.5px_2.5px_0px_#0284c7] hover:bg-slate-700 hover:border-slate-500 neo-btn'
                            : 'bg-white border-black text-black shadow-[3px_3px_0px_#000000] hover:bg-amber-50 neo-btn'
                        }`}
                        title={currentIndex === 0 ? "You are on the first question" : "Previous Question (Arrow Left)"}
                      >
                        <ChevronLeft className="w-4 h-4 stroke-[2.5]" />
                        <span>Previous</span>
                      </button>

                      <button
                        onClick={handleNext}
                        disabled={currentIndex === filteredQuestions.length - 1}
                        className={`flex items-center justify-center gap-2 px-6 py-2.5 rounded-2xl text-xs font-black border-2 transition-all select-none ${
                          currentIndex === filteredQuestions.length - 1
                            ? darkMode
                              ? 'bg-slate-900 border-slate-800 text-slate-500 cursor-not-allowed opacity-50 shadow-none'
                              : 'bg-slate-100 border-slate-300 text-slate-400 cursor-not-allowed opacity-50 shadow-none'
                            : darkMode
                            ? 'bg-amber-400 text-black border-slate-700 shadow-[3px_3px_0px_#FFF] neo-btn hover:bg-amber-300'
                            : 'bg-amber-300 text-black border-black shadow-[3px_3px_0px_#000000] neo-btn hover:bg-amber-400'
                        }`}
                        title="Next Question (Arrow Right)"
                      >
                        <span>Next</span>
                        <ChevronRight className="w-4 h-4 stroke-[2.5]" />
                      </button>
                    </div>

                    <span className="text-xs font-bold text-slate-500 dark:text-slate-400 hidden lg:inline">
                      Shortcuts: [1-4] Select • [←/→] Navigate • [S] Star • [E] Solution
                    </span>
                  </div>

                  {/* Mobile Quick Link to open palette if collapsed */}
                  {!showMobilePalette && (
                    <div className="lg:hidden pt-2 text-center">
                      <button
                        onClick={() => {
                          setShowMobilePalette(true);
                          window.scrollTo({ top: 0, behavior: 'smooth' });
                        }}
                        className={`text-xs font-black px-4 py-2.5 rounded-2xl border-2 transition-all neo-btn inline-flex items-center gap-2 ${
                          darkMode ? 'bg-slate-900 border-slate-700 text-cyan-300 shadow-[2px_2px_0px_#0284c7]' : 'bg-slate-100 border-black text-black shadow-[2px_2px_0px_#000]'
                        }`}
                      >
                        <ListFilter className="w-3.5 h-3.5" />
                        <span>Open 200 Questions Palette & Filters</span>
                      </button>
                    </div>
                  )}
                </div>
              ) : null}
            </div>
          </div>
        </div>
        )}

        {/* =========================================
            MODE 2: CONCEPT & VISUALIZATION HUB
            ========================================= */}
        {mode === 'concepts' && (
          <div className="space-y-6">
            {/* Banner */}
            <div className={`p-6 sm:p-8 rounded-3xl border-[2.5px] ${
              darkMode ? 'bg-slate-900 border-slate-700 text-slate-100 shadow-[5px_5px_0px_#0284c7]' : 'bg-emerald-100 border-black text-black shadow-[5px_5px_0px_#000000]'
            }`}>
              <div className="max-w-3xl space-y-2">
                <span className="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider bg-black text-white border border-black">
                  Core Architecture Blueprints
                </span>
                <h2 className={`text-2xl sm:text-3xl font-black tracking-tight ${darkMode ? 'text-white' : 'text-black'}`}>
                  Concept Explanation & Visualization Hub
                </h2>
                <p className={`text-xs sm:text-sm font-bold leading-relaxed ${darkMode ? 'text-slate-200' : 'text-slate-800'}`}>
                  Clear, zero-jargon mental models paired with complete ASCII execution blueprints covering Medallion architecture, Kimball dimensional modeling, SCD Types 1-6, and Delta Lake internals.
                </p>
              </div>

              {/* Search */}
              <div className="mt-5 max-w-md relative">
                <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search architecture concepts..."
                  value={conceptSearch}
                  onChange={(e) => setConceptSearch(e.target.value)}
                  className={`w-full pl-10 pr-3 py-2.5 text-xs font-bold rounded-2xl border-2 transition focus:outline-none ${
                    darkMode
                      ? 'bg-slate-950 border-slate-700 text-slate-100 placeholder:text-slate-400 shadow-[3px_3px_0px_#0284c7] focus:border-cyan-400'
                      : 'border-2 border-black bg-white text-black shadow-[3px_3px_0px_#000] placeholder:text-slate-400'
                  }`}
                />
              </div>
            </div>

            {/* Concepts List */}
            <div className="grid grid-cols-1 gap-6">
              {filteredConcepts.map((concept) => {
                const isExpanded = expandedConceptId === concept.id;
                return (
                  <div
                    key={concept.id}
                    className={`rounded-3xl border-[2.5px] transition-all overflow-hidden ${
                      isExpanded
                        ? darkMode
                          ? 'bg-slate-900 border-cyan-400 text-slate-100 shadow-[6px_6px_0px_#0284c7]'
                          : 'bg-white border-black text-slate-900 shadow-[6px_6px_0px_#000000]'
                        : darkMode
                        ? 'bg-slate-900 border-slate-700 text-slate-100 shadow-[3px_3px_0px_#0284c7] hover:border-slate-500'
                        : 'bg-white border-black text-slate-900 shadow-[3px_3px_0px_#000000] hover:-translate-x-0.5 hover:-translate-y-0.5'
                    }`}
                  >
                    <div
                      onClick={() => setExpandedConceptId(isExpanded ? null : concept.id)}
                      className="p-5 sm:p-6 flex items-center justify-between gap-4 cursor-pointer select-none"
                    >
                      <div className="space-y-1.5 flex-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase bg-amber-300 text-black border border-black shadow-[1.5px_1.5px_0px_#000]">
                            {concept.badge}
                          </span>
                          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-black border border-black">
                            {concept.domain}
                          </span>
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-black bg-lime-300 text-black border border-black">
                            {concept.difficulty}
                          </span>
                        </div>
                        <h3 className={`text-base sm:text-xl font-black ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                          {concept.title}
                        </h3>
                        <p className={`text-xs font-medium leading-relaxed ${darkMode ? 'text-slate-300' : 'text-slate-600'}`}>
                          {concept.summary}
                        </p>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        <span className={`text-xs font-black hidden sm:inline ${darkMode ? 'text-cyan-300' : 'text-black'}`}>
                          {isExpanded ? 'Collapse' : 'Explore'}
                        </span>
                        <div className="w-8 h-8 rounded-xl bg-amber-300 border-2 border-black flex items-center justify-center text-black">
                          <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`} />
                        </div>
                      </div>
                    </div>

                    {isExpanded && (
                      <div className={`p-6 pt-0 space-y-6 border-t-2 ${darkMode ? 'border-slate-800' : 'border-black/10'}`}>
                        {/* 1. Beginner Intuition */}
                        <div className={`p-4 rounded-2xl border-2 space-y-1.5 shadow-[3px_3px_0px_#000] ${
                          darkMode ? 'bg-amber-950/60 border-amber-400 text-amber-100' : 'bg-amber-100 border-black text-black'
                        }`}>
                          <div className={`flex items-center gap-2 font-black text-xs uppercase ${darkMode ? 'text-amber-300' : 'text-amber-700'}`}>
                            <Lightbulb className="w-4 h-4 text-amber-500" />
                            <span>Beginner Mental Model (Plain-English Analogy)</span>
                          </div>
                          <p className={`text-xs sm:text-sm font-semibold leading-relaxed ${darkMode ? 'text-amber-100' : 'text-slate-900'}`}>
                            {concept.beginnerAnalogy}
                          </p>
                        </div>

                        {/* 2. Visual Blueprint */}
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className={`text-xs font-black uppercase flex items-center gap-1.5 ${darkMode ? 'text-cyan-400' : 'text-sky-700'}`}>
                              <Workflow className="w-4 h-4" /> Architectural Blueprint & Data Flow
                            </span>
                            <button
                              onClick={() => handleCopyCode(concept.visualDiagram, concept.id)}
                              className={`text-[11px] px-3 py-1 rounded-xl border-2 font-black neo-btn ${
                                darkMode ? 'border-slate-700 bg-slate-800 text-cyan-300' : 'border-black bg-white text-black'
                              }`}
                            >
                              {copiedCodeId === concept.id ? 'Copied!' : 'Copy Blueprint'}
                            </button>
                          </div>
                          <pre className="p-5 rounded-2xl text-[11px] sm:text-xs font-mono border-2 border-black bg-slate-950 text-cyan-200 overflow-x-auto shadow-[4px_4px_0px_#000]">
                            {concept.visualDiagram}
                          </pre>
                        </div>

                        {/* 3. Key Rules */}
                        <div className="space-y-2">
                          <h4 className={`text-xs font-black uppercase ${darkMode ? 'text-slate-200' : 'text-slate-900'}`}>
                            Key Rules to Memorize
                          </h4>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                            {concept.keyRules.map((rule, idx) => (
                              <div
                                key={idx}
                                className={`p-3.5 rounded-2xl border-2 text-xs font-bold flex items-start gap-2 shadow-[2px_2px_0px_#000] ${
                                  darkMode ? 'border-slate-700 bg-slate-950 text-slate-100' : 'border-black bg-slate-50 text-slate-900'
                                }`}
                              >
                                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                                <span className="leading-relaxed">{rule}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* 4. Interview Trap & Code */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                          <div className={`p-4 rounded-2xl border-2 space-y-1.5 shadow-[3px_3px_0px_#000] ${
                            darkMode ? 'bg-rose-950/60 border-rose-500 text-rose-100' : 'bg-rose-100 border-black text-black'
                          }`}>
                            <div className={`flex items-center gap-2 font-black text-xs uppercase ${darkMode ? 'text-rose-300' : 'text-rose-700'}`}>
                              <ShieldAlert className="w-4 h-4 text-rose-500" />
                              <span>Client Interview Trap / Anti-Pattern</span>
                            </div>
                            <p className={`text-xs sm:text-sm font-semibold leading-relaxed ${darkMode ? 'text-rose-100' : 'text-slate-900'}`}>
                              {concept.interviewGotchas}
                            </p>
                          </div>

                          <div className={`p-4 rounded-2xl border-2 border-black bg-slate-950 text-white space-y-2 shadow-[3px_3px_0px_#000]`}>
                            <div className="flex items-center justify-between">
                              <span className="text-xs font-black text-slate-400">Implementation Reference</span>
                              <button
                                onClick={() => handleCopyCode(concept.codeExample, `code-${concept.id}`)}
                                className="text-[10px] font-black text-cyan-400 hover:text-cyan-300"
                              >
                                {copiedCodeId === `code-${concept.id}` ? 'Copied' : 'Copy SQL'}
                              </button>
                            </div>
                            <pre className="text-[11px] font-mono text-cyan-300 overflow-x-auto leading-relaxed">
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
              /* Exam Config Screen with Custom Rounded Dropdowns */
              <div className={`max-w-2xl mx-auto p-6 sm:p-10 rounded-3xl border-[2.5px] text-center space-y-6 ${
                darkMode ? 'bg-slate-900 border-slate-700 shadow-[6px_6px_0px_#0284c7]' : 'bg-white border-black shadow-[6px_6px_0px_#000000]'
              }`}>
                <div className="w-16 h-16 rounded-2xl bg-amber-300 border-2 border-black flex items-center justify-center mx-auto shadow-[3px_3px_0px_#000]">
                  <Timer className="w-8 h-8 text-black stroke-[2.5]" />
                </div>
                <div>
                  <h2 className="text-2xl font-black">
                    Databricks & SQL Client Mock Exam
                  </h2>
                  <p className="text-xs text-slate-500 font-bold mt-1">
                    Timed exam simulation with randomized questions, flagged review, and difficulty analytics.
                  </p>
                </div>

                {/* Custom Rounded Dropdowns for Exam Configuration (No more ugly rectangular select!) */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left">
                  <CustomDropdown
                    label="Filter by Domain:"
                    value={examCategoryFilter}
                    options={categoryDropdownOptions}
                    onChange={(val) => setExamCategoryFilter(val)}
                    icon={Layers}
                    darkMode={darkMode}
                    accentColor="yellow"
                  />

                  <CustomDropdown
                    label="Filter by Difficulty:"
                    value={examDifficultyFilter}
                    options={difficultyDropdownOptions}
                    onChange={(val) => setExamDifficultyFilter(val)}
                    icon={Gauge}
                    darkMode={darkMode}
                    accentColor="emerald"
                  />
                </div>

                {/* Tactile Question Count Selection */}
                <div className="space-y-3 pt-2">
                  <span className="text-xs font-black uppercase tracking-wider block">
                    Choose Number of Questions:
                  </span>
                  <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
                    {[
                      { count: 10, time: '10 Mins', color: 'bg-amber-300' },
                      { count: 25, time: '25 Mins', color: 'bg-emerald-300' },
                      { count: 50, time: '50 Mins', color: 'bg-sky-300' },
                      { count: 100, time: '100 Mins', color: 'bg-orange-300' },
                      { count: 200, time: '200 Mins', color: 'bg-yellow-300' }
                    ].map((item) => (
                      <button
                        key={item.count}
                        onClick={() => startExam(item.count)}
                        className={`py-4 px-3 rounded-2xl text-xs font-black border-[2.5px] border-black ${item.color} text-black shadow-[4px_4px_0px_#000000] hover:shadow-[5px_5px_0px_#000000] hover:-translate-x-0.5 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-[1px_1px_0px_#000] neo-btn flex flex-col items-center justify-center gap-1 cursor-pointer`}
                      >
                        <span className="text-xl sm:text-2xl font-black font-heading leading-none">{item.count}</span>
                        <span className="text-[11px] font-extrabold uppercase tracking-wide opacity-90">{item.time}</span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : examFinished ? (
              /* Score Report */
              <div className="max-w-4xl mx-auto space-y-6">
                <div className={`p-8 rounded-3xl border-[2.5px] text-center space-y-4 ${
                  darkMode ? 'bg-slate-900 border-slate-700 shadow-[6px_6px_0px_#0284c7]' : 'bg-white border-black shadow-[6px_6px_0px_#000]'
                }`}>
                  <div className={`w-24 h-24 rounded-3xl mx-auto flex items-center justify-center text-3xl font-black border-[3px] border-black shadow-[4px_4px_0px_#000] ${
                    examScore.percentage >= 70 ? 'bg-emerald-300 text-black' : 'bg-rose-300 text-black'
                  }`}>
                    {examScore.percentage}%
                  </div>

                  <h2 className="text-2xl font-black">
                    {examScore.percentage >= 70 ? '🎉 Passed! Client Ready!' : '📚 Review Needed - Keep Practicing!'}
                  </h2>
                  <p className="text-xs font-bold text-slate-500">
                    Answered {examScore.correct} of {examScore.total} questions correctly. Passing threshold is 70%.
                  </p>

                  {/* Difficulty Breakdown */}
                  <div className="grid grid-cols-3 gap-3 max-w-lg mx-auto pt-2">
                    {['Easy', 'Medium', 'Hard'].map((diff) => {
                      const stat = examScore.difficultyStats[diff] || { total: 0, correct: 0 };
                      const pct = stat.total > 0 ? Math.round((stat.correct / stat.total) * 100) : 0;
                      return (
                        <div key={diff} className="p-3 rounded-2xl border-2 border-black bg-slate-50 dark:bg-slate-950 text-center shadow-[2px_2px_0px_#000]">
                          <span className="text-[10px] font-black uppercase text-slate-400 block">{diff}</span>
                          <span className="text-lg font-black block">{stat.correct}/{stat.total}</span>
                          <span className="text-[10px] font-black text-amber-500">{pct}%</span>
                        </div>
                      );
                    })}
                  </div>

                  <div className="flex flex-wrap items-center justify-center gap-3 pt-3">
                    <button
                      onClick={() => setExamStarted(false)}
                      className="px-6 py-2.5 rounded-2xl bg-amber-300 text-black font-black border-2 border-black shadow-[3px_3px_0px_#000] neo-btn"
                    >
                      Start New Exam
                    </button>
                    <button
                      onClick={() => setMode('practice')}
                      className="px-6 py-2.5 rounded-2xl bg-white text-black font-black border-2 border-black shadow-[3px_3px_0px_#000] neo-btn"
                    >
                      Return to Practice
                    </button>
                  </div>
                </div>

                {/* Review Answers */}
                <div className={`p-6 sm:p-8 rounded-3xl border-[2.5px] space-y-4 ${
                  darkMode ? 'bg-slate-900 border-slate-700' : 'bg-white border-black shadow-[4px_4px_0px_#000]'
                }`}>
                  <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-black/10 dark:border-slate-800 pb-3">
                    <h3 className="text-base font-black flex items-center gap-2">
                      <Award className="w-5 h-5 text-amber-500" />
                      <span>Exam Answers Review</span>
                    </h3>
                    <div className="flex items-center gap-1.5">
                      {['all', 'incorrect', 'flagged'].map((rf) => (
                        <button
                          key={rf}
                          onClick={() => setExamReviewFilter(rf)}
                          className={`px-3 py-1 rounded-xl text-xs font-black border-2 capitalize neo-btn ${
                            examReviewFilter === rf
                              ? 'bg-amber-300 text-black border-black shadow-[2px_2px_0px_#000]'
                              : 'bg-white dark:bg-slate-950 border-black text-slate-700 dark:text-slate-300'
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
                          className={`p-5 rounded-2xl border-2 space-y-3 ${
                            isCorrect
                              ? 'bg-emerald-50 dark:bg-emerald-950/40 border-black shadow-[3px_3px_0px_#000]'
                              : 'bg-rose-50 dark:bg-rose-950/40 border-black shadow-[3px_3px_0px_#000]'
                          }`}
                        >
                          <div className="flex items-center justify-between gap-2">
                            <span className="text-xs font-black">
                              Q{idx + 1}. {q.category} • [{q.difficulty}]
                            </span>
                            <span className={`text-xs font-black px-2.5 py-0.5 rounded-full border border-black ${
                              isCorrect ? 'bg-emerald-300 text-black' : 'bg-rose-300 text-black'
                            }`}>
                              {isCorrect ? 'Correct' : userAns !== undefined ? 'Incorrect' : 'Unanswered'}
                            </span>
                          </div>
                          <p className="text-sm font-black leading-relaxed">{q.question}</p>
                          <div className="text-xs space-y-1 font-bold">
                            <p className="text-emerald-700 dark:text-emerald-300">
                              ✓ Correct: {['A', 'B', 'C', 'D'][q.correct]} - {q.options[q.correct]}
                            </p>
                            {userAns !== undefined && !isCorrect && (
                              <p className="text-rose-700 dark:text-rose-300">
                                ✗ Your Answer: {['A', 'B', 'C', 'D'][userAns]} - {q.options[userAns]}
                              </p>
                            )}
                          </div>
                          <p className="text-xs font-medium leading-relaxed pt-2 border-t border-black/10 dark:border-slate-800">
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
                <div className="lg:col-span-1 space-y-4 order-2 lg:order-1">
                  <div className={`p-5 rounded-3xl border-[2.5px] text-center space-y-3 ${
                    darkMode ? 'bg-slate-900 border-slate-700 shadow-[4px_4px_0px_#0284c7]' : 'bg-white border-black shadow-[4px_4px_0px_#000]'
                  }`}>
                    <div className="flex items-center justify-center gap-2">
                      <Clock className="w-5 h-5 text-amber-500" />
                      <span className="text-2xl font-black font-mono">
                        {formatTime(examTimeLeft)}
                      </span>
                    </div>
                    <span className="text-[11px] font-black text-slate-400 block uppercase">
                      Time Remaining
                    </span>
                    <button
                      onClick={() => setShowSubmitModal(true)}
                      className="w-full py-2.5 rounded-2xl bg-rose-400 text-black font-black text-xs border-2 border-black shadow-[3px_3px_0px_#000] neo-btn"
                    >
                      End & Submit Exam
                    </button>
                  </div>

                  {/* Palette */}
                  <div className={`p-4 rounded-3xl border-[2.5px] space-y-3 ${
                    darkMode ? 'bg-slate-900 border-slate-700 shadow-[4px_4px_0px_#0284c7]' : 'bg-white border-black shadow-[4px_4px_0px_#000]'
                  }`}>
                    <div className="flex items-center justify-between pb-1 border-b border-black/10 dark:border-slate-800">
                      <span className="text-xs font-black">Exam Navigator</span>
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
                            className={`h-8 rounded-xl text-xs font-black relative border-2 neo-btn ${
                              isCurrent
                                ? 'bg-amber-300 text-black border-black ring-2 ring-black shadow-[2px_2px_0px_#000]'
                                : isAnswered
                                ? 'bg-emerald-300 text-black border-black shadow-[1.5px_1.5px_0px_#000]'
                                : 'bg-white text-slate-800 border-black'
                            }`}
                          >
                            {idx + 1}
                            {isFlagged && (
                              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-orange-400 border border-black rounded-full" />
                            )}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Question */}
                <div className="lg:col-span-3 space-y-4 order-1 lg:order-2">
                  {/* Mobile Compact Timer Bar on top of question */}
                  <div className={`lg:hidden p-3.5 rounded-2xl border-2 flex items-center justify-between gap-3 ${
                    darkMode ? 'bg-slate-900 border-slate-700 text-slate-100 shadow-[3px_3px_0px_#0284c7]' : 'bg-white border-black text-black shadow-[3px_3px_0px_#000]'
                  }`}>
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-amber-500" />
                      <span className="text-base font-black font-mono">
                        {formatTime(examTimeLeft)}
                      </span>
                    </div>
                    <span className="text-xs font-black">
                      {Object.keys(examAnswers).length} / {examQuestions.length} answered
                    </span>
                    <button
                      onClick={() => setShowSubmitModal(true)}
                      className="px-3 py-1 rounded-xl bg-rose-400 text-black font-black text-xs border border-black shadow-[1.5px_1.5px_0px_#000] neo-btn"
                    >
                      Submit
                    </button>
                  </div>

                  {examQuestions[examCurrentIdx] && (
                    <div className={`p-6 sm:p-8 rounded-3xl border-[2.5px] space-y-6 ${
                      darkMode ? 'bg-slate-900 border-slate-700 shadow-[5px_5px_0px_#0284c7]' : 'bg-white border-black shadow-[5px_5px_0px_#000]'
                    }`}>
                      <div className="flex items-center justify-between border-b-2 border-black/10 dark:border-slate-800 pb-4">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-black px-3 py-1 rounded-xl bg-amber-300 text-black border-2 border-black shadow-[2px_2px_0px_#000]">
                            Question {examCurrentIdx + 1} of {examQuestions.length}
                          </span>
                          <span className="text-xs font-black px-2.5 py-1 rounded-xl bg-slate-100 text-black border-2 border-black">
                            {examQuestions[examCurrentIdx].category}
                          </span>
                        </div>
                        <button
                          onClick={() => toggleReviewMark(examQuestions[examCurrentIdx].id)}
                          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-black border-2 neo-btn ${
                            markedForReview.has(examQuestions[examCurrentIdx].id)
                              ? 'bg-orange-300 text-black border-black shadow-[2px_2px_0px_#000]'
                              : 'bg-white text-black border-black'
                          }`}
                        >
                          <Flag className="w-3.5 h-3.5" />
                          <span>{markedForReview.has(examQuestions[examCurrentIdx].id) ? 'Flagged' : 'Flag'}</span>
                        </button>
                      </div>

                      <div className={`text-base sm:text-lg font-black leading-relaxed ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                        {examQuestions[examCurrentIdx].question}
                      </div>

                      <div className="space-y-3">
                        {examQuestions[examCurrentIdx].options.map((opt, optIdx) => {
                          const isSelected = examAnswers[examQuestions[examCurrentIdx].id] === optIdx;
                          return (
                            <button
                              key={optIdx}
                              onClick={() => handleExamSelect(examQuestions[examCurrentIdx].id, optIdx)}
                              className={`w-full text-left p-4 rounded-2xl border-[2.5px] transition-all flex items-start gap-3.5 neo-btn ${
                                isSelected
                                  ? 'bg-amber-200 border-black text-black font-black shadow-[4px_4px_0px_#000]'
                                  : darkMode
                                  ? 'bg-slate-950 border-slate-700 text-slate-100 hover:border-slate-500 shadow-[3px_3px_0px_#0284c7]'
                                  : 'bg-white border-black text-black shadow-[2.5px_2.5px_0px_#000]'
                              }`}
                            >
                              <div className={`w-7 h-7 rounded-xl flex items-center justify-center text-xs font-black shrink-0 border-2 border-black ${
                                isSelected ? 'bg-black text-white' : 'bg-yellow-300 text-black'
                              }`}>
                                {['A', 'B', 'C', 'D'][optIdx]}
                              </div>
                              <div className="flex-1 text-sm sm:text-base font-extrabold leading-snug pt-0.5">
                                {opt}
                              </div>
                            </button>
                          );
                        })}
                      </div>

                      <div className="flex items-center justify-between pt-4 border-t-2 border-black/10 dark:border-slate-800">
                        <button
                          onClick={() => setExamCurrentIdx((prev) => Math.max(0, prev - 1))}
                          disabled={examCurrentIdx === 0}
                          className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl text-xs font-black border-2 transition-all select-none ${
                            examCurrentIdx === 0
                              ? darkMode
                                ? 'bg-slate-900 border-slate-800 text-slate-500 cursor-not-allowed opacity-50 shadow-none'
                                : 'bg-slate-100 border-slate-300 text-slate-400 cursor-not-allowed opacity-50 shadow-none'
                              : darkMode
                              ? 'bg-slate-800 border-slate-700 text-slate-100 shadow-[2.5px_2.5px_0px_#0284c7] hover:bg-slate-700 neo-btn'
                              : 'bg-white border-black text-black shadow-[2.5px_2.5px_0px_#000] hover:bg-amber-50 neo-btn'
                          }`}
                        >
                          <ChevronLeft className="w-4 h-4 stroke-[2.5]" /> Previous
                        </button>
                        <button
                          onClick={() => setExamCurrentIdx((prev) => Math.min(examQuestions.length - 1, prev + 1))}
                          disabled={examCurrentIdx === examQuestions.length - 1}
                          className={`flex items-center gap-2 px-6 py-2.5 rounded-2xl text-xs font-black border-2 transition-all select-none ${
                            examCurrentIdx === examQuestions.length - 1
                              ? darkMode
                                ? 'bg-slate-900 border-slate-800 text-slate-500 cursor-not-allowed opacity-50 shadow-none'
                                : 'bg-slate-100 border-slate-300 text-slate-400 cursor-not-allowed opacity-50 shadow-none'
                              : 'bg-amber-300 text-black border-2 border-black shadow-[3px_3px_0px_#000] neo-btn hover:bg-amber-400'
                          }`}
                        >
                          Next <ChevronRight className="w-4 h-4 stroke-[2.5]" />
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Submit Confirmation Modal */}
            {showSubmitModal && (
              <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fadeIn">
                <div className="max-w-md w-full p-6 sm:p-8 rounded-3xl border-[3px] border-black bg-white text-black shadow-[8px_8px_0px_#000000] space-y-4">
                  <h3 className="text-xl font-black">Submit Exam?</h3>
                  <p className="text-xs font-bold text-slate-700">
                    You have answered {Object.keys(examAnswers).length} out of {examQuestions.length} questions.
                    {examQuestions.length - Object.keys(examAnswers).length > 0 && (
                      <span className="block mt-2 p-2 rounded-xl bg-amber-100 border-2 border-black text-black font-black">
                        ⚠️ You still have {examQuestions.length - Object.keys(examAnswers).length} unanswered questions!
                      </span>
                    )}
                  </p>
                  <div className="flex items-center justify-end gap-3 pt-3">
                    <button
                      onClick={() => setShowSubmitModal(false)}
                      className="px-4 py-2 rounded-xl text-xs font-black border-2 border-black bg-white text-black neo-btn"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => {
                        setShowSubmitModal(false);
                        setExamFinished(true);
                      }}
                      className="px-5 py-2 rounded-xl bg-rose-400 text-black border-2 border-black font-black shadow-[3px_3px_0px_#000] neo-btn"
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
                <h2 className="text-xl font-black">Interactive 3D Flashcards</h2>
                <p className="text-xs text-slate-500 font-bold">
                  Card {flashcardIdx + 1} of {QUESTION_BANK.length} • Press Space or Click to Flip
                </p>
              </div>
              <button
                onClick={() => {
                  setFlashcardIdx(Math.floor(Math.random() * QUESTION_BANK.length));
                  setIsFlipped(false);
                }}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-2xl border-2 border-black bg-white text-black font-black shadow-[3px_3px_0px_#000] neo-btn text-xs"
              >
                <Shuffle className="w-4 h-4" />
                <span>Shuffle</span>
              </button>
            </div>

            {/* Flashcard Card */}
            <div
              onClick={() => setIsFlipped(!isFlipped)}
              className={`min-h-[380px] p-8 rounded-3xl border-[3px] cursor-pointer select-none transition-all duration-200 flex flex-col justify-between ${
                isFlipped
                  ? darkMode
                    ? 'bg-emerald-950/80 border-emerald-400 text-emerald-100 shadow-[8px_8px_0px_#10B981]'
                    : 'bg-emerald-100 border-black text-black shadow-[8px_8px_0px_#000000]'
                  : darkMode
                  ? 'bg-slate-900 border-slate-700 text-slate-100 shadow-[8px_8px_0px_#0284c7] hover:border-slate-500'
                  : 'bg-white border-black text-slate-900 shadow-[8px_8px_0px_#000000] hover:-translate-x-1 hover:-translate-y-1'
              }`}
            >
              <div className={`flex items-center justify-between border-b-2 pb-3 ${darkMode ? 'border-slate-800' : 'border-black/10'}`}>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-black px-2.5 py-0.5 rounded-xl bg-amber-300 text-black border border-black shadow-[1.5px_1.5px_0px_#000]">
                    Q{activeFlashcard.num}
                  </span>
                  <span className={`text-xs font-black px-2 py-0.5 rounded-xl border ${
                    darkMode ? 'bg-slate-800 text-slate-200 border-slate-700' : 'bg-slate-100 text-black border-black'
                  }`}>
                    {activeFlashcard.category}
                  </span>
                  <span className="text-[10px] font-black px-2 py-0.5 rounded-xl bg-lime-300 text-black border border-black">
                    {activeFlashcard.difficulty}
                  </span>
                </div>
                <span className={`text-[11px] font-black uppercase ${darkMode ? 'text-slate-400' : 'text-slate-500'}`}>
                  {isFlipped ? 'Answer & Mental Model' : 'Question Prompt'}
                </span>
              </div>

              {/* Main Content */}
              <div className="py-6 flex-1 flex flex-col justify-center">
                {!isFlipped ? (
                  <div className="space-y-4">
                    <p className={`text-lg sm:text-xl font-black leading-relaxed ${darkMode ? 'text-white' : 'text-slate-900'}`}>
                      {activeFlashcard.question}
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-2">
                      {activeFlashcard.options.map((opt, idx) => (
                        <div
                          key={idx}
                          className={`p-2.5 rounded-xl border-2 text-xs font-bold shadow-[2px_2px_0px_#000] ${
                            darkMode ? 'border-slate-700 bg-slate-950 text-slate-100' : 'border-black bg-slate-50 text-black'
                          }`}
                        >
                          <span className="font-black mr-1.5">{['A', 'B', 'C', 'D'][idx]})</span>
                          {opt}
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="p-3.5 rounded-2xl bg-black text-white border-2 border-black text-sm font-black flex items-center gap-2 shadow-[3px_3px_0px_#000]">
                      <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                      <span>
                        Answer: Option {['A', 'B', 'C', 'D'][activeFlashcard.correct]} ({activeFlashcard.options[activeFlashcard.correct]})
                      </span>
                    </div>
                    <p className={`text-xs sm:text-sm font-bold leading-relaxed ${darkMode ? 'text-amber-200' : 'text-slate-800'}`}>
                      💡 {activeFlashcard.beginnerConcept}
                    </p>
                    <p className={`text-xs font-medium leading-relaxed ${darkMode ? 'text-slate-200' : 'text-slate-700'}`}>
                      🎯 {activeFlashcard.explanation}
                    </p>
                  </div>
                )}
              </div>

              <div className={`flex items-center justify-between text-xs font-black pt-3 border-t-2 ${darkMode ? 'border-slate-800 text-slate-400' : 'border-black/10 text-slate-500'}`}>
                <span>Space / Enter to Flip</span>
                <span>[← / →] Navigate</span>
              </div>
            </div>

            {/* Navigation */}
            <div className="flex items-center justify-between gap-3">
              <button
                onClick={() => {
                  setFlashcardIdx((prev) => Math.max(0, prev - 1));
                  setIsFlipped(false);
                }}
                disabled={flashcardIdx === 0}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl border-2 font-black text-xs transition-all select-none ${
                  flashcardIdx === 0
                    ? darkMode
                      ? 'bg-slate-900 border-slate-800 text-slate-500 cursor-not-allowed opacity-50 shadow-none'
                      : 'bg-slate-100 border-slate-300 text-slate-400 cursor-not-allowed opacity-50 shadow-none'
                    : darkMode
                    ? 'border-slate-700 bg-slate-800 text-slate-100 shadow-[2.5px_2.5px_0px_#0284c7] hover:bg-slate-700 neo-btn'
                    : 'border-black bg-white text-black shadow-[3px_3px_0px_#000] hover:bg-amber-50 neo-btn'
                }`}
              >
                <ChevronLeft className="w-4 h-4 stroke-[2.5]" /> Previous
              </button>
              <button
                onClick={() => {
                  setFlashcardIdx((prev) => Math.min(QUESTION_BANK.length - 1, prev + 1));
                  setIsFlipped(false);
                }}
                disabled={flashcardIdx === QUESTION_BANK.length - 1}
                className={`flex items-center gap-2 px-6 py-2.5 rounded-2xl border-2 font-black text-xs transition-all select-none ${
                  flashcardIdx === QUESTION_BANK.length - 1
                    ? darkMode
                      ? 'bg-slate-900 border-slate-800 text-slate-500 cursor-not-allowed opacity-50 shadow-none'
                      : 'bg-slate-100 border-slate-300 text-slate-400 cursor-not-allowed opacity-50 shadow-none'
                    : 'bg-amber-300 text-black border-black shadow-[3px_3px_0px_#000] neo-btn hover:bg-amber-400'
                }`}
              >
                Next <ChevronRight className="w-4 h-4 stroke-[2.5]" />
              </button>
            </div>
          </div>
        )}

        {/* =========================================
            MODE 5: QUICK CHEATSHEET MODE
            ========================================= */}
        {mode === 'cheatsheet' && (
          <div className="space-y-6">
            <div className={`p-6 sm:p-8 rounded-3xl border-[2.5px] ${
              darkMode ? 'bg-slate-900 border-slate-700 text-slate-100 shadow-[5px_5px_0px_#0284c7]' : 'bg-yellow-100 border-black text-black shadow-[5px_5px_0px_#000]'
            }`}>
              <h2 className={`text-2xl font-black ${darkMode ? 'text-white' : 'text-black'}`}>Pre-Interview Quick Cheatsheet</h2>
              <p className={`text-xs sm:text-sm font-bold mt-1 ${darkMode ? 'text-slate-200' : 'text-slate-700'}`}>
                High-yield formula summaries, ACID properties, join mechanics, and Kimball dimensional modeling rules.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {CHEAT_SHEET_ITEMS.map((item, idx) => (
                <div
                  key={idx}
                  className={`p-6 rounded-3xl border-[2.5px] space-y-3 ${
                    darkMode ? 'bg-slate-900 border-slate-700 text-slate-100 shadow-[4px_4px_0px_#0284c7]' : 'bg-white border-black text-black shadow-[4px_4px_0px_#000]'
                  }`}
                >
                  <span className="text-[10px] font-black uppercase px-2.5 py-0.5 rounded-full bg-amber-300 text-black border border-black shadow-[1.5px_1.5px_0px_#000] inline-block">
                    {item.tag}
                  </span>
                  <h3 className={`text-base font-black ${darkMode ? 'text-white' : 'text-black'}`}>{item.title}</h3>
                  <div className={`text-xs leading-relaxed font-mono whitespace-pre-line ${darkMode ? 'text-slate-200' : 'text-slate-800'}`}>
                    {item.content}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

      </main>

      {/* FOOTER */}
      <footer className={`mt-16 border-t-[3px] py-8 px-4 text-center text-xs font-bold space-y-1.5 ${
        darkMode ? 'bg-[#0F172A] border-slate-700 text-slate-400' : 'bg-white border-black text-slate-800'
      }`}>
        <p className="font-black text-sm">
          SQL, Data Warehousing & Databricks Master Practice Hub • 200 Questions Bank
        </p>
        <p className="text-[11px] opacity-80">
          Soft Neo-Brutalist Architecture • 14 Core Domains • Virtual Client Scenarios • Medallion & Kimball Blueprints
        </p>
      </footer>
    </div>
  );
}
