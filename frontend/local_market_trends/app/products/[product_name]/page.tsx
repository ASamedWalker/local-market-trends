"use client";
import { useParams, useSearchParams, useRouter } from "next/navigation";
import axios from "axios";
import Image from "next/image";
import { useEffect, useState } from "react";
import {
  Item,
  ItemCardProps,
  PriceRecord,
  SpecialOffer,
  Market,
} from "@/types/Item";

const ProductPage = () => {
  const { product_name } = useParams<{ product_name: string }>();
  const [product, setProduct] = useState<Item | null>(null);
  const [priceRecords, setPriceRecords] = useState<PriceRecord[]>([]);
  const [specialOffers, setSpecialOffers] = useState<SpecialOffer[]>([]);
  const [markets, setMarkets] = useState<Market[]>([]);

  useEffect(() => {
    const fetchProductDetails = async () => {
      if (!product_name) return;

      try {
        // Fetch product details
        const productRes = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/products/${product_name}`
        );
        const productData = productRes.data;
        setProduct(productData);

        // Fetch all price records and special offers
        const [priceRecordsResponse, specialOffersResponse, marketsResponse] =
          await Promise.all([
            axios.get(`${process.env.NEXT_PUBLIC_API_URL}/price_records`),
            axios.get(`${process.env.NEXT_PUBLIC_API_URL}/special_offers`),
            axios.get(`${process.env.NEXT_PUBLIC_API_URL}/markets`),
          ]);

        // Filter price records and special offers for this product
        const relatedPriceRecords = priceRecordsResponse.data.filter(
          (record) => record.grocery_item_id === productData.id
        );
        const relatedSpecialOffers = specialOffersResponse.data.filter(
          (offer) => offer.grocery_item_id === productData.id
        );
        const relatedMarkets = relatedPriceRecords
          .map((record) => {
            return marketsResponse.data.find(
              (market) => market.id === record.market_id
            );
          })
          .filter((market): market is Market => market !== undefined);

        setPriceRecords(relatedPriceRecords);
        setSpecialOffers(relatedSpecialOffers);
        setMarkets(relatedMarkets);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchProductDetails();
  }, [product_name]);

  if (!product) {
    return <div>Loading...</div>;
  }

  const fullImageUrl = `${process.env.NEXT_PUBLIC_API_URL}${product.image_url}`;
  return (
    <div className="container mx-auto my-8 p-4 bg-white">
      {product ? (
        <>
          {/* Product Details Section */}
          <div className="flex flex-col md:flex-row md:items-center border-b pb-4">
            <div className="md:flex-1">
              <Image
                src={`${process.env.NEXT_PUBLIC_API_URL}${product.image_url}`}
                alt={product.name}
                width={200}
                height={200}
                layout="responsive"
                className="rounded-lg"
              />
            </div>

            <div className="md:flex-1 md:pl-6">
              <h1 className="text-2xl font-bold">{product.name}</h1>
              <p className="text-gray-600">{product.description}</p>
              {/* Display the first category if available */}
              <div className="flex items-center mt-2">
                <a
                  href="#reviews"
                  className="flex items-center text-blue-500 hover:text-blue-600"
                >
                  {/* Dynamically render star icons based on rating, example rating: 4.5 */}
                  {[...Array(5)].map((_, i) => (
                    <span
                      key={i}
                      className="fa fa-star"
                    ></span>
                  ))}
                  <span className="ml-4">(0 reviews)</span>
                </a>
              </div>
              {/* Assuming priceRecords holds the most recent price */}
              <div className="text-lg font-semibold mt-2">
                $
                {priceRecords.length > 0 ? priceRecords[0].price : "Loading..."}
              </div>
              {/* Display the first special offer if available */}
              {specialOffers.length > 0 && (
                <div className="mt-2 p-2 text-sm bg-yellow-100 border border-yellow-200 rounded">
                  Special offer: {specialOffers[0].description}
                </div>
              )}
            </div>
          </div>

          {/* Availability and Store Pickup Section */}
          <div className="my-4">
            <h2 className="text-xl font-semibold mb-2">Availability</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {markets.map((market) => (
                <div
                  key={market.id}
                  className="p-4 border rounded flex justify-between items-center"
                >
                  <span>{market.name}</span>
                  <span className="text-green-600">In stock</span>{" "}
                  {/* Dynamically show stock status based on your data */}
                </div>
              ))}
            </div>
          </div>

          {/* Add to Cart Section */}
          <div className="flex justify-end mt-4">
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Add to Cart
            </button>
          </div>

          {/* Reviews Section */}
        <div id="reviews" className="my-8">
          <h2 className="text-xl font-semibold mb-4">Customer Reviews</h2>
          {/* Customer reviews will go here */}
        </div>

        {/* ... Rest of the Reviews Section display */}
        </>
      ) : (
        <div>Loading product...</div>
      )}
    </div>
  );
};

export default ProductPage;
