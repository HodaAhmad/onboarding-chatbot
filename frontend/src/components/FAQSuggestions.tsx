'use client';
import React from 'react';

type FAQSuggestionsProps = {
  questions: string[];
  onSelect: (question: string) => void;
};

export const FAQSuggestions: React.FC<FAQSuggestionsProps> = ({ questions, onSelect }) => {
  return (
    <div className="mt-6 animate-fade-in-down">
      <h4 className="text-gray-700 font-semibold mb-2">Try one of these:</h4>
      <div className="flex flex-wrap gap-3 ">
        {questions.map((q, i) => (
          <button
            key={q}
            onClick={() => onSelect(q)}
            className="cursor-pointer bg-white shadow-md px-4 py-2 rounded-2xl text-sm text-gray-700 border hover:bg-gray-100 transition-all duration-200"
            style={{ animationDelay: `${i * 100}ms` }}
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
};
