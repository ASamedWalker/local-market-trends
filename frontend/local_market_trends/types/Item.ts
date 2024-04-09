// frontend/local_market_trends/types/Item.ts

export interface Item {
  id: string;
  name: string;
  image_url: string;
  description: string;
  category: string;
  unit: string;
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

export interface Review {
  id: string;
  grocery_item_id: string;
  rating: number;
  comment: string;
  created_at: string;
}

export interface ItemCardProps {
  id: string;
  name: string;
  image_url: string;
  description: string;
  unit: string;
  category: string;
  priceRecord?: PriceRecord;
  specialOffer?: SpecialOffer;
  reviews?: Review[];
}

export interface FeaturedItemsProps {
  items: Item[];
  shouldFetchData: boolean;
}

export interface Market {
  id: string;
  name: string;
  location_description: string;
  image_url: string;
  opening_hours: string;
  rating: number;
}