import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    // Check messages validity
    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return NextResponse.json({ error: "No messages provided." }, { status: 400 });
    }

    const lastMessage = messages[messages.length - 1].content;
    console.log("Received from UI:", lastMessage);

    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    const res = await fetch(`${backendUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ messages }),
    });

    if (!res.ok) {
      const err = await res.text();
      console.error("Backend Error:", err);
      return NextResponse.json({ error: "Backend error", detail: err }, { status: 500 });
    }

    const data = await res.json();
    return NextResponse.json(data);

  } catch (error: unknown) {
    console.error("Route handler error:", error);

    const errorMessage =
      error instanceof Error ? error.message : "Unknown error";

    return NextResponse.json(
      { error: "Internal Server Error", detail: errorMessage },
      { status: 500 }
    );
  }

}
