// components/ItemCard.tsx
import { useState, useEffect, useMemo } from "react";
import Image from "next/image";
import Link from "next/link";
import { PriceRecord, SpecialOffer, ItemCardProps } from "@/types/Item";
import { renderStars } from "@/utils/renderStars";

const ItemCard = ({
  name,
  description,
  category,
  image_url,
  unit,
  priceRecord,
  specialOffer,
  id,
}: ItemCardProps) => {
  const fullImageUrl = `${process.env.NEXT_PUBLIC_API_URL}${image_url}`;
  const discountImageUrl = specialOffer
    ? `${process.env.NEXT_PUBLIC_API_URL}${specialOffer.image_url}`
    : null;


  return (
    <Link href={`/products/${name.toLowerCase().replace(/ /g, "-")}`} passHref>
      <div className="max-w-sm flex flex-col h-full rounded overflow-hidden shadow-lg transition duration-300 ease-in-out transform hover:scale-105">
        <div className="relative h-48">
          <Image
            src={fullImageUrl}
            alt={name}
            layout="fill"
            objectFit="cover"
          />
          {discountImageUrl && (
            <div className="absolute right-2 top-2 w-1/4">
              <Image
                src={discountImageUrl}
                alt="Discount"
                layout="responsive"
                width={100}
                height={100}
                objectFit="contain"
              />
            </div>
          )}
        </div>

        <div className="px-6 py-4 flex-grow">
          <div className="space-y-2">
            <h3 className="font-bold text-xl mb-2">{name}</h3>
            <p className="text-gray-700 text-base">{description}</p>
            <div className="flex items-center justify-between">
              {priceRecord && (
                <p className="text-lg font-semibold text-gray-800">
                  ${priceRecord.price} {unit && `${unit}`}
                </p>
              )}
              {category && (
                <span className="inline-block bg-red-600 text-xs font-semibold mr-2 px-3 py-1 rounded-full text-white dark:bg-red-200 dark:text-red-900">
                  {category}
                </span>
              )}
            </div>
            {specialOffer && (
              <div className="mt-2">
                <p className="text-sm text-red-500">
                  {specialOffer.description} - Valid until{" "}
                  {new Date(specialOffer.valid_to).toLocaleDateString()}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
};

export default ItemCard;
