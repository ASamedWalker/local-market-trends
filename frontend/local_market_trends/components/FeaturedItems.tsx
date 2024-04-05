import { useEffect, useState, useMemo } from "react";
import { AiOutlineSearch } from "react-icons/ai";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import ItemCard from "./ItemCard";
import {
  Item,
  PriceRecord,
  SpecialOffer,
  FeaturedItemsProps,
} from "@/types/Item";

const FeaturedItems = ({ items }: FeaturedItemsProps) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredItems, setFilteredItems] = useState<Item[]>([]);
  const [priceRecords, setPriceRecords] = useState<PriceRecord[]>([]);
  const [specialOffers, setSpecialOffers] = useState<SpecialOffer[]>([]);
  const [loading, setLoading] = useState(true);
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

    fetchPriceRecords();
    fetchSpecialOffers();
    setLoading(false);
  }, []);

  const itemsWithDetails = useMemo(() => {
    return filteredItems.map((item) => {
      const priceRecord = priceRecords.find(
        (record) => record.grocery_item_id === item.id
      );
      const specialOffer = specialOffers.find(
        (offer) => offer.grocery_item_id === item.id
      );
      return { ...item, priceRecord, specialOffer };
    });
  }, [filteredItems, priceRecords, specialOffers]);

  useEffect(() => {
    if (Array.isArray(items)) {
      setFilteredItems(
        items.filter((item) =>
          item.name.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }
  }, [items, searchTerm]);

  function onItemClick(name: string) {
    // Implement your own logic here
  }

  if (loading) {
    return <AiOutlineLoading3Quarters className="animate-spin text-4xl" />;
  }

  if (error) {
    return <p>Error: {error.message}</p>;
  }

  return (
    <div className="container mx-auto my-8 p-4 bg-white max-w-7xl">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {itemsWithDetails.map((item) => (
          <ItemCard
            key={item.id}
            {...item}
            image_url={item.image_url}
            onItemClick={() => onItemClick(item.name)}
          />
        ))}
      </div>
    </div>
  );
};

export default FeaturedItems;
