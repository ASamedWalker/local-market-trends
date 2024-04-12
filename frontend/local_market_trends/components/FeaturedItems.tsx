import { useEffect, useState, useMemo } from "react";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import ItemCard from "./ItemCard";
import {
  Item,
  PriceRecord,
  SpecialOffer,
  FeaturedItemsProps,
} from "@/types/Item";

const FeaturedItems = ({
  items = [],
  shouldFetchData = true,
}: FeaturedItemsProps) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredItems, setFilteredItems] = useState<Item[]>([]);
  const [priceRecords, setPriceRecords] = useState<PriceRecord[]>([]);
  const [specialOffers, setSpecialOffers] = useState<SpecialOffer[]>([]);
  const [loading, setLoading] = useState(shouldFetchData);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPriceRecords = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/price_records`
        );
        if (!res.ok) throw new Error("Failed to fetch price records");
        const data = await res.json();
        setPriceRecords(data);
      } catch (error) {
        console.error("Error fetching price records:", error);
        setError(error);
      }
    };

    const fetchSpecialOffers = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/special_offers`
        );
        if (!res.ok) throw new Error("Failed to fetch special offers");
        const data = await res.json();
        setSpecialOffers(data);
      } catch (error) {
        console.error("Error fetching special offers:", error);
        setError(error);
      }
    };

    Promise.all([fetchPriceRecords(), fetchSpecialOffers()]).finally(() => {
      setLoading(false);
    });
  }, []);

  const itemsWithDetails = useMemo(
    () =>
      filteredItems.map((item) => ({
        ...item,
        priceRecord: priceRecords.find(
          (record) => record.grocery_item_id === item.id
        ),
        specialOffer: specialOffers.find(
          (offer) => offer.grocery_item_id === item.id
        ),
      })),
    [filteredItems, priceRecords, specialOffers]
  );

  useEffect(() => {
    if (Array.isArray(items) && items.length > 0) {
      setFilteredItems(
        items.filter((item) =>
          item.name.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }
  }, [items, searchTerm]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <AiOutlineLoading3Quarters className="animate-spin text-4xl" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-center">Error: {error.message}</div>
    );
  }

  return (
    <div className="container mx-auto my-8 p-4 bg-white max-w-7xl">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {itemsWithDetails.map((item) => (
          <ItemCard key={item.id} {...item} image_url={item.image_url} />
        ))}
      </div>
    </div>
  );
};

export default FeaturedItems;
