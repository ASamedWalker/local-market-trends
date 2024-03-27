import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Navbar from "@/components/Navbar";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Local Market Trends",
  description: "Stay updated with the latest market trends and prices",
};

interface LayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: LayoutProps) {
  return (
    <html lang="en">
      <body className={(inter.className, "flex flex-col min-h-screen")}>
        <header className="bg-blue-500 text-white p-4">
          <Navbar />
        </header>
        <main className="container mx-auto my-8">{children}</main>
        <footer className="bg-gray-800 text-white text-center p-4">
          [Footer]
        </footer>
      </body>
    </html>
  );
}
