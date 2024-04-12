// HomePage.tsx
"use client";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { FiChevronLeft, FiChevronRight } from "react-icons/fi";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import FeaturedItems from "@/components/FeaturedItems";
import { useSearch } from "@/components/SearchContext"; // Import your useSearch hook

const HomePage = () => {
  const searchParams = useSearchParams();
  const { searchResults, setSearchResults } = useSearch();
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const searchQuery = searchParams.get("q");

  const fetchItems = async () => {
    setLoading(true);
    setError(null); // Reset error state before fetching
    let url = `${process.env.NEXT_PUBLIC_API_URL}/products?page=${currentPage}`;
    if (searchQuery) {
      url += `&q=${encodeURIComponent(searchQuery.toString())}`;
    }

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("Failed to fetch items");
      }
      const { items, total_pages } = await response.json();
      setSearchResults(items);
      setTotalPages(total_pages);
    } catch (error) {
      console.error("Failed to fetch items:", error);
      setError("Failed to load items, please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, [searchQuery, currentPage, setSearchResults]);

  return (
    <>
      {loading ? (
        <div className="flex justify-center items-center min-h-screen">
          <AiOutlineLoading3Quarters className="animate-spin text-4xl" />
        </div>
      ) : error ? (
        <div className="text-red-500 text-center my-2">
          {error}{" "}
          <button onClick={fetchItems} className="btn-primary">
            Retry
          </button>
        </div>
      ) : (
        <>
          <FeaturedItems items={searchResults} shouldFetchData={false} />
          <div className="flex items-center justify-center my-4">
            {searchResults.length > 0 && (
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
      )}
    </>
  );
};

export default HomePage;
