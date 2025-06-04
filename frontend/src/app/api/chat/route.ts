import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { messages } = await req.json();

  // Get the last message content
  const lastMessage = messages[messages.length - 1].content;

  // Connect to FastAPI backend
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const response = await fetch(`${backendUrl}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ messages }),
  });

  const data = await response.json();

  return NextResponse.json(data);
}
