interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
}

export function MessageBubble({ role, content }: MessageBubbleProps) {
  const isUser = role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-2`}>
      <div
      style={{ whiteSpace: 'pre-line' }}
        className={`px-4 py-2 rounded-lg whitespace-pre-wrap break-words shadow-sm
        ${isUser 
          ? 'bg-blue-500 text-white max-w-[75%] md:max-w-[60%] lg:max-w-[50%]' 
          : 'bg-gray-200 text-black max-w-[75%] md:max-w-[60%] lg:max-w-[50%]'
        }`}
      >
        {content}
      </div>
    </div>
  );
}
