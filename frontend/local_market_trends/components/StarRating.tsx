export const StarRating = ({ rating, setRating }) => {
  return (
    <div className="flex justify-center my-2">
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          onClick={() => setRating(star)}
          className={`hover:text-yellow-500 ${
            rating >= star ? "text-yellow-500" : "text-gray-400"
          }`}
          aria-label={`Rate this ${star} stars out of 5`}
        >
          &#9733;
        </button>
      ))}
    </div>
  );
};
