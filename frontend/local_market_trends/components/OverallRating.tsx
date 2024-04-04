import React from "react";
import { renderStars } from "@/utils/renderStars";

const OverallRating = ({ reviews }) => {
  const totalReviews = reviews.length;
  const averageRating =
    totalReviews > 0
      ? reviews.reduce((acc, review) => acc + review.rating, 0) / totalReviews
      : 0;
  const ratingCounts = Array(5).fill(0);

  reviews.forEach((review) => {
    if (review.rating) {
      // Ensure there is a rating before trying to access it
      ratingCounts[review.rating - 1]++;
    }
  });

  return (
    <div>
      {totalReviews > 0 ? (
        <>
          <div className="flex items-center">
            <div className="text-xl font-bold">{averageRating.toFixed(1)}</div>
            <div className="flex ml-2">{renderStars(averageRating)}</div>
            <div className="ml-2">({totalReviews} reviews)</div>
          </div>
          <div>
            {ratingCounts.map((count, index) => (
              <div key={index}>
                {5 - index} stars: {count}
              </div>
            ))}
          </div>
        </>
      ) : (
        <div>No reviews yet.</div>
      )}
    </div>
  );
};

export default OverallRating;
