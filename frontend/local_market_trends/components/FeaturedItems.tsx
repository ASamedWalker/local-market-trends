"use client";
// components/FeaturedItems.client.tsx
import { useEffect, useState } from "react";
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

  useEffect(() => {
    setFilteredItems(
      items.filter((item) =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [items, searchTerm]);

  useEffect(() => {
    // Fetch prices
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
      }
    };

    // Fetch special offers
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
      }
    };

    fetchPriceRecords();
    fetchSpecialOffers();
  }, []);

  const findPriceForItem = (itemId: string): PriceRecord | undefined => {
    return priceRecords.find((record) => record.grocery_item_id === itemId);
  };
  // New function to find the special offer for an item
  const findSpecialOfferForItem = (
    itemId: string
  ): SpecialOffer | undefined => {
    return specialOffers.find((offer) => offer.grocery_item_id === itemId);
  };

  // Integrate both price records and special offers with items before rendering
  const itemsWithDetails = filteredItems.map((item) => {
    const priceRecord = findPriceForItem(item.id);
    const specialOffer = findSpecialOfferForItem(item.id);
    return { ...item, priceRecord, specialOffer };
  });

  function onItemClick(name: string) {
    throw new Error("Function not implemented.");
  }

  return (
    <div className="container mx-auto my-8">
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
