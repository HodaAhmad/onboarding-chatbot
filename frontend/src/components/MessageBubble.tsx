import ReactMarkdown from 'react-markdown';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
}

export function MessageBubble({ role, content }: MessageBubbleProps) {
  const isUser = role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-2`}>
      <div
        className={`px-4 py-2 rounded-xl shadow-sm whitespace-pre-wrap break-words
        ${isUser 
          ? 'bg-blue-500 text-white max-w-[75%] md:max-w-[60%] lg:max-w-[50%]' 
          : 'bg-gray-200 text-black max-w-[75%] md:max-w-[60%] lg:max-w-[50%]'
        }`}
      >
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="my-2">{children}</p>,
              ul: ({ children }) => <ul className="list-disc list-inside pl-4 my-2">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal list-inside pl-4 my-2">{children}</ol>,
              li: ({ children }) => <li className="my-1">{children}</li>,
              strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
              em: ({ children }) => <em className="italic">{children}</em>,
              br: () => <br />,
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
