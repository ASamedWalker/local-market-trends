"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSearch } from "@/components/SearchContext";
import axios from "axios";

const Navbar = () => {
  const router = useRouter();
  const { searchTerm, setSearchTerm, setSearchResults, searchResults } =
    useSearch();

  const handleSearch = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!searchTerm.trim()) return; // Prevent navigation on empty search term
    // Programmatically navigate to the search results page with the search term as a query parameter
    router.push(`/search?q=${encodeURIComponent(searchTerm)}`);
  };

  const handleChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.target;
    setSearchTerm(value);
    if (value.trim() === "") {
      try {
        const response = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/products/`
        );
        setSearchResults(response.data);
        return;
      } catch (error) {
        console.error("Error fetching items:", error);
      }
    }
    try {
      const response = await axios.get(
        `${
          process.env.NEXT_PUBLIC_API_URL
        }/products/search/${encodeURIComponent(value)}`
      );
      setSearchResults(response.data);
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };
  return (
    <nav className=" text-white shadow-lg">
      <div className="container mx-auto flex justify-between items-center py-4 px-6 md:px-12">
        <span className="font-bold text-xl tracking-tight">
          Local Market Trends
        </span>
        <form className="flex flex-grow ml-4" onSubmit={handleSearch}>
          <input
            type="search"
            value={searchTerm}
            onChange={handleChange}
            placeholder="Search for groceries..."
            className="w-full px-4 py-2 rounded-l-md text-gray-700 bg-white border border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
          />
          <button
            type="submit"
            className="bg-blue-600 px-4 rounded-r-md hover:bg-blue-700 transition-colors"
          >
            Search
          </button>
        </form>
      </div>
    </nav>
  );
};

export default Navbar;
