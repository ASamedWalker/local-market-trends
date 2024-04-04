// AddReviewForm.js or within the same file
import { useState } from "react";
import { StarRating } from "@/components/starRating";

const AddReviewForm = ({ onSubmit }) => {
  const [reviewText, setReviewText] = useState("");
  const [rating, setRating] = useState(0);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (rating > 0 && reviewText.trim()) {
      onSubmit({ reviewText, rating });
      setReviewText("");
      setRating(0);
    } else {
      // Implement more user-friendly feedback
      alert("Please add a review and select a rating.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="my-4">
      <StarRating rating={rating} setRating={setRating} />
      <label htmlFor="reviewText" className="sr-only">
        Review Text
      </label>
      <textarea
        id="reviewText"
        value={reviewText}
        onChange={(e) => setReviewText(e.target.value)}
        className="border p-2 w-full"
        placeholder="Write your review..."
        required
      />
      <button
        type="submit"
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2"
      >
        Submit Review
      </button>
    </form>
  );
};

export default AddReviewForm;
