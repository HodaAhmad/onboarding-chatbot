import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const { messages, program } = await req.json(); //get program and messages from request body

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
      body: JSON.stringify({
       messages: [
          {
            role: "user",
            content: lastMessage  // e.g. "how many credits do I need?"
          }
        ],
        program,
      }),
    });

    if (!res.ok) {
      const err = await res.text();
      console.error("Backend Error:", err);
      return NextResponse.json({ error: "Backend error", detail: err }, { status: 500 });
    }

    const data = await res.json();

    // Build the assistant's message
    let botMessageContent = data.reply;
    if (data.email_draft) {
      botMessageContent += `\n\n📩 Suggested Email:\n${data.email_draft}`;
    }

    const botMessage = {
      id: Date.now().toString(),
      content: botMessageContent,
      role: 'assistant',
      timestamp: new Date(),
    };

    return NextResponse.json(botMessage);


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
