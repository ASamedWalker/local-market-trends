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

        // Fetch related data
        const fetchPriceRecords = axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/price_records`
        );
        const fetchSpecialOffers = axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/special_offers`
        );
        const fetchMarkets = axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/markets`
        );

        Promise.all([fetchPriceRecords, fetchSpecialOffers, fetchMarkets])
          .then((results) => {
            const [priceRecordsRes, specialOffersRes, marketsRes] = results;

            setPriceRecords(priceRecordsRes.data);
            setSpecialOffers(specialOffersRes.data);
            setMarkets(marketsRes.data);
          })
          .catch((error) => {
            console.error("Error fetching related data:", error);
          });
      } catch (error) {
        console.error("Error fetching product details:", error);
      }
    };

    fetchProductDetails();
  }, [product_name]);

  if (!product) {
    return <div>Loading...</div>;
  }

  const fullImageUrl = `${process.env.NEXT_PUBLIC_API_URL}${product.image_url}`;
  return (
    <div className="container mx-auto">
      {product ? (
        <>
          <div className="max-w-4xl mx-auto py-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <Image
                  src={fullImageUrl}
                  alt={product.name}
                  width={400}
                  height={400}
                  layout="responsive"
                  className="rounded-lg"
                />
              </div>
              <div className="flex flex-col justify-center">
                <h1 className="text-3xl font-semibold mb-4">{product.name}</h1>
                <p className="text-gray-700 mb-4">{product.description}</p>
                {/* Displaying Price Records */}
                {priceRecords && priceRecords.length > 0 && (
                  <div>
                    <h2 className="text-2xl font-semibold">Price Records</h2>
                    {priceRecords.map((record) => (
                      <p key={record.id}>
                        Market: {record.market_id}, Price: ${record.price},
                        Promotional: {record.is_promotional ? "Yes" : "No"}
                      </p>
                    ))}
                  </div>
                )}
                {/* Displaying Special Offers */}
                {specialOffers && specialOffers.length > 0 && (
                  <div className="mt-4">
                    <h2 className="text-2xl font-semibold">Special Offers</h2>
                    {specialOffers.map((offer) => (
                      <p key={offer.id}>
                        {offer.description} (Valid from{" "}
                        {new Date(offer.valid_from).toLocaleDateString()} to{" "}
                        {new Date(offer.valid_to).toLocaleDateString()})
                      </p>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
          {/* Displaying Markets */}
          {markets && markets.length > 0 && (
            <div className="max-w-4xl mx-auto py-8">
              <h2 className="text-2xl font-semibold mb-4">Available At:</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {markets.map((market) => (
                  <div key={market.id} className="border rounded-lg p-4">
                    <h3 className="font-semibold">{market.name}</h3>
                    {/* Additional market details like location can be displayed here */}
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
};

export default ProductPage;
