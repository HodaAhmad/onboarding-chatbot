# Onboarding Chatbot – Fullstack Setup (Next.js + FastAPI)

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app), connected to a [FastAPI](https://fastapi.tiangolo.com) backend that handles chat functionality using OpenAI GPT-4.

---

## 📦 Prerequisites

Before running the project, install the following tools:

### ✅ For All Users
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js + npm](https://nodejs.org/) (includes npm)

---

## 💻 Installing Node.js + npm

### On macOS
Using Homebrew:
```bash
brew install node
```

### On Windows
Download and install from:
[https://nodejs.org](https://nodejs.org)

---

## 🚀 Getting Started (Frontend)

First, go to the frontend directory: 

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

---

## 🧠 Getting Started (Backend – FastAPI)

From the root directory:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the backend folder with your OpenAI key:

```env
OPENAI_API_KEY=your-openai-key-here
```

```RAG
python rag_preprocess.py
```

Start the backend server:

```bash
uvicorn main:app --reload
```

This will run at [http://localhost:8000](http://localhost:8000)

---

## 🔗 Connecting Frontend to Backend

In the `frontend` folder, create a file called `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Now your frontend will forward requests to the FastAPI backend.

---

## 🔍 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [OpenAI API Docs](https://platform.openai.com/docs/)

---

## ☁️ Deploy

You can deploy the frontend with [Vercel](https://vercel.com), and the backend with services like [Render](https://render.com), [Railway](https://railway.app), or [Heroku](https://www.heroku.com/).

---

Feel free to customize or extend this fullstack chatbot!