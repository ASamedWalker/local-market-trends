"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSearch } from "@/components/SearchContext";
import axios from "axios";
import { AiOutlineLoading3Quarters, AiOutlineSearch } from 'react-icons/ai';

const Navbar = () => {
  const router = useRouter();
  const { searchTerm, setSearchTerm, setSearchResults } =
    useSearch();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchTerm.trim() === "") {
        fetchItems();
      } else {
        fetchSearchResults();
      }
    }, 500); // 500ms delay
    return () => clearTimeout(timeoutId);
  }, [searchTerm]);

  const fetchItems = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/products/`);
      setSearchResults(response.data);
    } catch (error) {
      console.error("Error fetching items:", error);
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSearchResults = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/products/search/${encodeURIComponent(searchTerm)}`);
      setSearchResults(response.data);
    } catch (error) {
      console.error("Error fetching search results:", error);
      setError(error);
    } finally {
      setLoading(false);
    }
  };


  const handleSearch = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!searchTerm.trim()) return;
    router.push(`/search?q=${encodeURIComponent(searchTerm)}`);
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  return (
    <nav className="text-white shadow-lg">
      <div className="container mx-auto flex justify-between items-center py-4 px-6 md:px-12">
        <span className="font-bold text-xl tracking-tight">Local Market Trends</span>
        <form className="flex flex-grow ml-4 relative" onSubmit={handleSearch}>
          <AiOutlineSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="search"
            value={searchTerm}
            onChange={handleChange}
            placeholder="Search for groceries..."
            className="w-full pl-10 pr-4 py-2 rounded-l-md text-gray-700 bg-white border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          />
          {loading && <AiOutlineLoading3Quarters className="absolute right-3 top-1/2 transform -translate-y-1/2 animate-spin text-gray-500" />}
          <button type="submit" className="bg-blue-600 px-4 rounded-r-md hover:bg-blue-700 transition-colors">Search</button>
        </form>
        {error && <p className="text-red-500">{error.message}</p>}
      </div>
    </nav>
  );
};

export default Navbar;
