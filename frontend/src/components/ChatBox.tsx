import { MessageBubble } from './MessageBubble';
import { Message } from '@/types/chat';

interface ChatBoxProps {
  messages: Message[];
  input: string;
  setInput: (value: string) => void;
  handleSendMessage: (e: React.FormEvent) => void;
  isLoading: boolean;
  suggestedQuestions?: string[];
  onSelectFAQ?: (question: string) => void;
}

export function ChatBox({
  messages,
  input,
  setInput,
  handleSendMessage,
  isLoading,
  suggestedQuestions,
  onSelectFAQ,
}: ChatBoxProps) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto space-y-2">
        {messages.length === 0 && !input.trim() && suggestedQuestions && onSelectFAQ && (
          <div
            className={`faq-container transition-opacity duration-500 ease-in-out ${
              input.trim() ? 'opacity-0 pointer-events-none translate-y-2' : 'opacity-100 translate-y-0'
            } flex flex-wrap gap-4 mb-4 justify-end-safe`}
          >
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => onSelectFAQ(question)}
                className="cursor-pointer faq-bubble bg-blue-100 text-blue-800 px-4 py-2 rounded-xl shadow-sm hover:bg-blue-200 transition text-sm"
              >
                {question}
              </button>
            ))}
          </div>
        )}


        {messages.map((msg) => (
          <MessageBubble key={msg.id} role={msg.role} content={msg.content} />
        ))}

        {isLoading && <MessageBubble role="assistant" content="Typing..." />}
      </div>

      <form onSubmit={handleSendMessage} className="mt-4 flex space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 border rounded"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
