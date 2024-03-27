// components/ItemCard.tsx
import Image from "next/image";
import Link from "next/link";

interface ItemCardProps {
  name: string;
  price: string;
  imageUrl: string;
  offer?: string | null;
}

const ItemCard = ({ name, price, imageUrl, offer }: ItemCardProps) => {
  return (
    <Link href={`/products/${name.toLowerCase().replace(/ /g, "-")}`} passHref>
      <div className="max-w-sm flex flex-col h-full rounded overflow-hidden shadow-lg transition duration-300 ease-in-out transform hover:scale-105">
        <Image
          src={imageUrl}
          alt={name}
          layout="responsive"
          width={300}
          height={200}
          objectFit="cover"
        />

        <div className="px-6 py-4">
          <div className="font-bold text-xl mb-2">{name}</div>
          <p className="text-gray-700 text-base flex-grow">{price}</p>
          {offer && (
            <span className="bg-red-100 text-red-800 text-sm font-semibold mr-2 px-2.5 py-0.5 rounded dark:bg-red-200 dark:text-red-900">
              {offer}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
};

export default ItemCard;
