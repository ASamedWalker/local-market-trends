// HomePage.tsx
"use client";
import { useEffect, useContext, useState } from "react";
import { useSearchParams } from "next/navigation";
import { FiChevronLeft, FiChevronRight } from "react-icons/fi";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import FeaturedItems from "@/components/FeaturedItems";
import { useSearch } from "@/components/SearchContext"; // Import your useSearch hook
import LocalMarkets from "@/components/LocalMarkets";
import CallToAction from "@/components/CallToAction";

const HomePage = () => {
  const searchParams = useSearchParams();
  const { searchResults, setSearchResults } = useSearch();
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const searchQuery = searchParams.get("q");

  useEffect(() => {
    const fetchItems = async () => {
      setLoading(true);
      let url = `${process.env.NEXT_PUBLIC_API_URL}/products?page=${currentPage}`;
      if (searchQuery) {
        url += `&q=${encodeURIComponent(searchQuery.toString())}`;
      }

      try {
        const response = await fetch(url);
        const { items, total_pages } = await response.json();
        setSearchResults(items);
        setTotalPages(total_pages);
      } catch (error) {
        console.error("Failed to fetch items:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchItems();
  }, [searchQuery, currentPage, setSearchResults]);

  return (
    <>
      <FeaturedItems items={searchResults} shouldFetchData={false} />
      <div className="flex items-center justify-center">
        {loading ? (
          <AiOutlineLoading3Quarters className="animate-spin text-4xl" />
        ) : (
          <>
            <button
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={currentPage === 1}
              className="inline-flex items-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed"
            >
              <FiChevronLeft className="mr-2" />
              Previous
            </button>
            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="inline-flex items-center px-7 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed ml-4"
            >
              Next
              <FiChevronRight className="ml-2" />
            </button>
          </>
        )}
      </div>
    </>
  );
};
export default HomePage;
