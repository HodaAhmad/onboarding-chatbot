'use client';

import { useState } from 'react';
import { Header } from '@/components/Header';
import { ChatBox } from '@/components/ChatBox';
import { Message } from '@/types/chat';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [pendingFAQ, setPendingFAQ] = useState<string | null>(null);
  const [program, setProgram] = useState<string | null>(null); //for handling program selection

  const suggestedQuestions = [
    {
      title: "Onboarding",
      questions: ["Campus Card", "Program Contacts", "Student Clubs in Campus"]
    },
    {
      title: "Semester",
      questions: ["Total Credits Needed", "Semester Schedule", "Semester Exams"]
    },
  ];


  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    const detected = detectProgram(trimmed);

    // If user is just confirming their program (like "MIE")
    if (detected && !pendingFAQ && !trimmed.match(/\w{3,}/g)) {
      setProgram(detected);
      
      setMessages((prev) => [...prev, userMessage]);
      setInput('');
      return;
    }

    const userMessage: Message = {
      id: crypto.randomUUID(),
      content: trimmed,
      role: 'user',
      timestamp: new Date(),
    };

    const newProgram = detected || program;

    if (!newProgram) {
      // Ask for program if still unknown
      setPendingFAQ(trimmed);
      const botMessage: Message = {
        id: crypto.randomUUID(),
        content: `Hello 👋 Before we continue, can you let me know which Masters program you're in?\n\n• Master in Management (MIM)\n• Management in Digital Technology (MMDT)\n• Information Engineering (MIE)`,
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMessage, botMessage]);
      setInput('');
      return;
    }

    if (detected && pendingFAQ) {
      // User just gave us their program, and there's a pending question
      setProgram(detected);
      setPendingFAQ(null);

      setMessages((prev) => [...prev, userMessage]);
      setInput('');
      setIsLoading(true);
      await sendToBackend(pendingFAQ, detected);
      setIsLoading(false);
      return;
    }

    // Normal question handling
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    await sendToBackend(trimmed, newProgram);
    setIsLoading(false);
  };


  // Function to detect the program based on user input
  function detectProgram(message: string): string | null {
    const msg = message.toLowerCase();

    if (msg.includes("mim") || msg.includes("master in management")) return "MIM";
    if (msg.includes("mmdt") || msg.includes("digital technology") || msg.includes("management in digital")) return "MMDT";
    if (msg.includes("mie") || msg.includes("information engineering")) return "MIE";

    return null;
  }


  const sendFAQMessage = async (question: string) => {
    if (!program) {
      setPendingFAQ(question);

      const botMessage: Message = {
        id: crypto.randomUUID(),
        content: `Before I can help, can you let me know which Masters program you're in?\n\n• Master in Management (MIM)\n• Management in Digital Technology (MMDT)\n• Information Engineering (MIE)`,
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
      return;
    }

    // If program is known, send the FAQ using shared logic
    setIsLoading(true);
    await sendToBackend(question, program);
    setIsLoading(false);
  };


  const sendToBackend = async (question: string, programParam: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      content: question,
      role: 'user',
      timestamp: new Date(),
    };

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: [...messages, userMessage], program: programParam }),
      });

      const data = await response.json();

      let replyContent = data.content || 'Sorry, I couldn’t generate a reply.';
      if (data.email_draft) {
        replyContent += `\n\n📩 Suggested Email:\n${data.email_draft}`;
      }

      const botMessage: Message = {
        id: crypto.randomUUID(),
        content: replyContent,
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };



  /*const sendFAQMessage = async (question: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content: question,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: [...messages, userMessage], program }),  
      });

      const data = await response.json();

      let replyContent = data.content || 'Sorry, I couldn’t generate a reply.';
      if (data.email_draft) {
        replyContent += `\n\n📩 Suggested Email:\n${data.email_draft}`;
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
  };*/


return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header />
      <main className="flex-1 overflow-auto p-4 px-18">
        <ChatBox
          messages={messages}
          input={input}
          setInput={setInput}
          handleSendMessage={handleSendMessage}
          isLoading={isLoading}
          suggestedQuestions={suggestedQuestions}
          onSelectFAQ={sendFAQMessage}
        />
      </main>
    </div>
  );

}
