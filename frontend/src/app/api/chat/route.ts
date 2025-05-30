import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { messages } = await req.json();

  // Mock response for demonstration
  const reply = `Echo: ${messages[messages.length - 1].content}`;

  return NextResponse.json({ reply });
}
