import Image from 'next/image';

export function Header() {
  return (
    <header className="flex items-center justify-between px-8 py-2 bg-white shadow">
      <div className="flex items-center space-x-2">
        <Image src="/logo.png" alt="TUM Logo" width={150} height={40} />
        <span className="text-xl font-semibold"></span>
      </div>
      <nav className="space-x-4">
        <a href="https://tumde-my.sharepoint.com/:b:/g/personal/hoda_bahaaaldeen_tum_de/ERWeVmYFPB9NnHlqQpqWSrIBEGIovDgdSBebsoTnXILO-w" target='_blank' className="text-blue-600 hover:underline">User Guide</a>
        <a href="mailto:hoda.bahaaaldeen@tum.de" className="text-blue-600 hover:underline">Report a Problem</a>
      </nav>
    </header>
  );
}
