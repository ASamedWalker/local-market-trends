// components/FeaturedItems.tsx
import Image from "next/image";
import ItemCard from "./ItemCard";

const items = [
  {
    id: 1,
    name: "Apples",
    price: "$1.99 /lb",
    imageUrl: "/images/fruits/apples.jpg",
    offer: "20% off",
  },
  {
    id: 2,
    name: "Oranges",
    price: "$0.99 /lb",
    imageUrl: "/images/fruits/oranges.jpg",
    offer: null,
  },
  {
    id: 3,
    name: "Bananas",
    price: "$0.59 /lb",
    imageUrl: "/images/fruits/bananas.jpg",
    offer: "Buy 1, Get 1 Free",
  },
  {
    id: 4,
    name: "Grapes",
    price: "$2.50 /lb",
    imageUrl: "/images/fruits/grapes.jpg",
    offer: null,
  },
  {
    id: 5,
    name: "Tomatoes",
    price: "$1.20 /lb",
    imageUrl: "/images/fruits/tomatoes.jpg",
    offer: "10% off",
  },
  {
    id: 6,
    name: "Lettuce",
    price: "$0.99 each",
    imageUrl: "/images/fruits/lettuce.jpg",
    offer: null,
  },
  // Add more items as needed
];

const FeaturedItems = () => {
  return (
    <div className="container mx-auto my-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {items.map((item) => (
          <ItemCard key={item.id} {...item} />
        ))}
      </div>
    </div>
  );
};

export default FeaturedItems;
