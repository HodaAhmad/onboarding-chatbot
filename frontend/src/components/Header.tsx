import Image from 'next/image';

export function Header() {
  return (
    <header className="flex items-center justify-between p-4 bg-white shadow">
      <div className="flex items-center space-x-2">
        <Image src="/logo.png" alt="TUM Logo" width={120} height={40} />
        <span className="text-xl font-semibold">TUM Chatbot</span>
      </div>
      <nav className="space-x-4">
        <a href="#" className="text-blue-600 hover:underline">Contact Support</a>
        <a href="#" className="text-blue-600 hover:underline">Report a Problem</a>
      </nav>
    </header>
  );
}
