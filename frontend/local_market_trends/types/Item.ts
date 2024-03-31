// frontend/local_market_trends/types/Item.ts

export interface Item {
  id: string;
  name: string;
  image_url: string;
  description: string;
  category: string;
}

export interface PriceRecord {
  id: string;
  grocery_item_id: string;
  market_id: string;
  price: number;
  is_promotional: boolean;
  date_recorded: string;
  promotional_details?: string;
}

export interface SpecialOffer {
  id: string;
  grocery_item_id: string;
  valid_from: string;
  valid_to: string;
  image_url: string;
  description: string;
}

export interface ItemCardProps {
  id: string;
  name: string;
  image_url: string;
  description: string;
  category: string;
  priceRecord?: PriceRecord;
  specialOffer?: SpecialOffer;
  onItemClick: () => void;
}

export interface FeaturedItemsProps {
  items: Item[];
  onItemClick: (productName: string) => void;
}

export interface Market {
  id: string;
  name: string;
  location_description: string;
  latitude: number;
  longitude: number;
}