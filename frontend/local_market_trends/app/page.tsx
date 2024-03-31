// HomePage.tsx
"use client";
import { useEffect, useContext } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import FeaturedItems from "@/components/FeaturedItems";
import { useSearch } from "@/components/SearchContext"; // Import your useSearch hook
import LocalMarkets from "@/components/LocalMarkets";
import CallToAction from "@/components/CallToAction";
import { Item } from "@/types/Item";

const HomePage = () => {
  const router = useRouter(); // Use the useRouter hook
  const searchParams = useSearchParams();
  const { searchResults, setSearchResults } = useSearch(); // Use your useSearch hook

  const searchQuery = searchParams.get("q");

  // Define function to handle navigation to product page
  const navigateToProductPage = (productName: string) => {
    router.push(`/products/${encodeURIComponent(productName)}`);
  };

  useEffect(() => {
    const fetchItems = async () => {
      let url = `${process.env.NEXT_PUBLIC_API_URL}/products/`;
      if (searchQuery) {
        url += `?q=${encodeURIComponent(searchQuery.toString())}`;
      }

      try {
        const response = await fetch(url);
        const data: Item[] = await response.json();
        setSearchResults(data); // Update the search results in the SearchContext
      } catch (error) {
        console.error("Failed to fetch items:", error);
      }
    };

    fetchItems();
  }, [searchQuery, setSearchResults]);

  return (
    <>
      <FeaturedItems
        items={searchResults}
        onItemClick={(productName) => navigateToProductPage(productName)}
      />{" "}
      {/* Use the search results from the SearchContext */}
      {/* <LocalMarkets /> */}
    </>
  );
};

export default HomePage;
