'use client';

import { useState } from 'react';
import { Header } from '@/components/Header';
import { ChatBox } from '@/components/ChatBox';
import { Message } from '@/types/chat';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: [...messages, userMessage] }),
      });

      const data = await response.json();
      console.log("Response from backend:", data);
      console.log("🔁 Response from backend:", data);
      console.log("📨 Reply Content:", data.content);
      console.log("📬 Email Content:", data.email);


      let replyContent = data.content || 'Sorry, I couldn’t generate a reply.';;

      if (data.email_draft) {
        replyContent += `\n\n📩 Here's a suggested email you can send:\n\n${data.email_draft}`;
      }

      const botMessage: Message = {
        id: Date.now().toString(),
        content: replyContent,
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
        console.error("Error sending message:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header />
      <main className="flex-1 overflow-auto p-4 px-24">
        <ChatBox
          messages={messages}
          input={input}
          setInput={setInput}
          handleSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </main>
    </div>
  );
}
