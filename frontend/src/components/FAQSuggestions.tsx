// components/FAQSuggestions.tsx

export interface FAQCategory {
  title: string;
  questions: string[];
}

export interface Props {
  categories: FAQCategory[];
  onSelect: (question: string) => void;
}

export function FAQSuggestions({ categories, onSelect }: Props) {
  return (
    <div className="flex flex-row justify-center gap-4 mt-8">
      {categories.map((cat) => (
        <div key={cat.title} className="bg-blue-100 p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">{cat.title}</h2>
          <div className="flex flex-wrap gap-3 min-w-[400px] items-center justify-center">
            {cat.questions.map((q) => (
              <button
                key={q}
                onClick={() => onSelect(q)}
                className="bg-white cursor-pointer text-blue-900 px-4 py-2 rounded-full hover:bg-blue-500 hover:text-white transition text-sm"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
