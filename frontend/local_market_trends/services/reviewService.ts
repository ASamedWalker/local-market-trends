import axios from "axios";

export const handleNewReviewSubmission = async (
  reviewText: string,
  rating: number,
  productId: string
) => {
  const reviewData = {
    grocery_item_id: productId, // Make sure this matches the field name expected by your backend
    rating: rating,
    comment: reviewText, // This field is optional in your model
  };

  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_API_URL}/reviews`,
      reviewData
    );
    console.log(response.data);
  } catch (error) {
    console.error("Error submitting review:", error);
  }
};
