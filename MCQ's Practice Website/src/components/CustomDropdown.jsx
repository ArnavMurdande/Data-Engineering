import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';

/**
 * Neo-Brutalist Custom Dropdown Component
 * Features:
 * - Generously rounded corners (rounded-2xl container, rounded-xl items)
 * - Solid 2.5px borders with zero-blur offset shadows
 * - Smooth rotating chevron in tactile action badge
 * - Fully accessible keyboard escape & outside click dismissal
 * - Smooth scroll with clipped inner container to prevent edge bleeding
 */
export default function CustomDropdown({
  label,
  value,
  options = [],
  onChange,
  icon: Icon,
  darkMode = false,
  placeholder = "Select an option",
  accentColor = "yellow", // 'yellow' | 'emerald' | 'cyan' | 'orange'
  className = ""
}) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  // Close dropdown on click outside or Escape key
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  // Determine active option label
  const selectedOption = options.find((opt) => {
    const optValue = typeof opt === 'object' && opt !== null ? opt.value : opt;
    return optValue === value;
  });

  const displayLabel = selectedOption
    ? typeof selectedOption === 'object'
      ? selectedOption.label
      : selectedOption
    : value || placeholder;

  // Accent styling for button badge
  const badgeColor = {
    yellow: darkMode ? 'bg-amber-400 text-black' : 'bg-amber-300 text-black',
    emerald: darkMode ? 'bg-emerald-400 text-black' : 'bg-emerald-300 text-black',
    cyan: darkMode ? 'bg-cyan-400 text-black' : 'bg-sky-300 text-black',
    orange: darkMode ? 'bg-orange-400 text-black' : 'bg-orange-300 text-black',
  }[accentColor] || (darkMode ? 'bg-amber-400 text-black' : 'bg-amber-300 text-black');

  return (
    <div className={`relative ${className}`} ref={containerRef}>
      {label && (
        <label className={`block text-xs font-black uppercase tracking-wider mb-1.5 ${
          darkMode ? 'text-slate-300' : 'text-slate-900 font-extrabold'
        }`}>
          {label}
        </label>
      )}

      {/* Dropdown Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        className={`w-full flex items-center justify-between p-3 text-xs sm:text-sm font-bold rounded-2xl transition-all duration-150 select-none border-[2.5px] ${
          darkMode
            ? 'bg-slate-900 text-slate-100 border-slate-700 hover:border-slate-500 shadow-[3px_3px_0px_#0284c7]'
            : 'bg-white text-slate-900 border-black shadow-[3.5px_3.5px_0px_#000000] hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-[5px_5px_0px_#000000]'
        } ${
          isOpen
            ? darkMode
              ? 'border-cyan-400 ring-2 ring-cyan-400/30'
              : '-translate-x-0.5 -translate-y-0.5 shadow-[5px_5px_0px_#000000] ring-2 ring-black/20'
            : ''
        }`}
      >
        <div className="flex items-center gap-2.5 truncate min-w-0">
          {Icon && (
            <div className={`w-7 h-7 rounded-xl flex items-center justify-center shrink-0 border-2 border-black ${badgeColor}`}>
              <Icon className="w-3.5 h-3.5 stroke-[2.5]" />
            </div>
          )}
          <span className="truncate font-black text-xs sm:text-sm">{displayLabel}</span>
        </div>

        <div className="flex items-center gap-2 shrink-0 ml-2">
          <div
            className={`w-7 h-7 rounded-xl flex items-center justify-center transition-transform duration-200 border-2 border-black ${badgeColor} ${
              isOpen ? 'transform rotate-180' : ''
            }`}
          >
            <ChevronDown className="w-4 h-4 stroke-[3]" />
          </div>
        </div>
      </button>

      {/* Dropdown Popup Menu with Rounded Corners & Neo-Brutalist Shadow */}
      {isOpen && (
        <div
          role="listbox"
          className={`absolute left-0 right-0 z-50 mt-2 rounded-2xl border-[2.5px] overflow-hidden transition-all duration-150 animate-fadeIn ${
            darkMode
              ? 'bg-slate-900 border-slate-700 text-slate-100 shadow-[6px_6px_0px_#0284c7]'
              : 'bg-white border-black text-slate-900 shadow-[6px_6px_0px_#000000]'
          }`}
        >
          {/* Inner scroll container with padding and rounded scrollbar */}
          <div className="max-h-72 overflow-y-auto p-2 scrollbar-thin space-y-1">
            {options.map((opt, idx) => {
              const optValue = typeof opt === 'object' && opt !== null ? opt.value : opt;
              const optLabel = typeof opt === 'object' && opt !== null ? opt.label : opt;
              const optCount = typeof opt === 'object' && opt !== null ? opt.count : undefined;
              const isSelected = optValue === value;

              return (
                <button
                  key={idx}
                  type="button"
                  role="option"
                  aria-selected={isSelected}
                  onClick={() => {
                    onChange(optValue);
                    setIsOpen(false);
                  }}
                  className={`w-full flex items-center justify-between px-3.5 py-2.5 text-xs sm:text-sm font-bold rounded-xl transition-all duration-100 ${
                    isSelected
                      ? darkMode
                        ? 'bg-cyan-950/80 text-cyan-300 border-2 border-cyan-400 font-black shadow-[2px_2px_0px_#0284c7]'
                        : `${badgeColor} text-black border-2 border-black font-black shadow-[2.5px_2.5px_0px_#000000]`
                      : darkMode
                      ? 'hover:bg-slate-800 text-slate-300 hover:text-white border-2 border-transparent hover:border-slate-600'
                      : 'hover:bg-amber-100 text-slate-800 hover:text-black border-2 border-transparent hover:border-black'
                  }`}
                >
                  <div className="flex items-center gap-2.5 truncate min-w-0">
                    <div
                      className={`w-5 h-5 rounded-lg flex items-center justify-center shrink-0 border-2 ${
                        isSelected
                          ? darkMode
                            ? 'bg-cyan-400 text-black border-cyan-300'
                            : 'bg-black text-white border-black'
                          : 'border-transparent'
                      }`}
                    >
                      {isSelected ? <Check className="w-3.5 h-3.5 stroke-[3]" /> : null}
                    </div>
                    <span className="truncate font-extrabold">{optLabel}</span>
                  </div>

                  {optCount !== undefined && (
                    <span
                      className={`text-[10px] px-2.5 py-0.5 rounded-full font-black ml-2 shrink-0 border-2 ${
                        isSelected
                          ? darkMode
                            ? 'bg-cyan-400/20 text-cyan-200 border-cyan-400/40'
                            : 'bg-black text-white border-black'
                          : darkMode
                          ? 'bg-slate-800 text-slate-400 border-slate-700'
                          : 'bg-slate-100 text-slate-800 border-black/30'
                      }`}
                    >
                      {optCount}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
