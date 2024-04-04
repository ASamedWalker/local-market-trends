import React from 'react';
import { format } from 'date-fns'; // Ensure you have 'date-fns' installed for date formatting
import { renderStars } from "@/utils/renderStars";

const ReviewCard = ({ review }) => {
  const reviewDate = review.date ? format(new Date(review.date), "MMM dd, yyyy") : "Unknown date";

  return (
    <div className="border p-4 my-2 shadow-lg rounded-lg">
      <div className="flex justify-between items-center mb-2">
        <div className="font-bold text-lg">{review.author}</div>
        <div className="flex items-center">
          {renderStars(review.rating)}
          <span className="ml-2 text-sm text-gray-600">{reviewDate}</span>
        </div>
      </div>
      <p className="mb-2">{review.text}</p>
      {review.verified && (
        <span className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
          Verified Purchase
        </span>
      )}
      {/* Response to Review */}
      {review.response && (
        <div className="mt-4 pt-4 border-t">
          <div className="font-semibold">Response from Seller:</div>
          <p className="text-sm">{review.response}</p>
        </div>
      )}
    </div>
  );
};

export default ReviewCard;
