import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Navbar from "@/components/Navbar";
import { SearchProvider } from "@/components/SearchContext";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Local Market Trends",
  description: "Stay updated with the latest market trends and prices",
};

interface LayoutProps {
  children: React.ReactNode;
  onSearch?: (searchTerm: string) => void;
}

export default function RootLayout({ children, onSearch }: LayoutProps) {
  const bodyClasses = `flex flex-col min-h-screen ${inter?.className || ""}`;
  return (
    <SearchProvider>
      <html lang="en">
        <body className={bodyClasses}>
          <header className="bg-teal-500 text-white p-4">
            <Navbar/>
          </header>
          <main className="flex-grow container mx-auto my-8">{children}</main>
          <footer className="bg-gray-800 text-white text-center p-4">
            [Footer]
          </footer>
        </body>
      </html>
    </SearchProvider>
  );
}
