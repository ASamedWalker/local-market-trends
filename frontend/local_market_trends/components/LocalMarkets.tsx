// components/LocalMarkets.tsx
const markets = [
  {
    id: 1,
    name: "Downtown Market",
    description: "Fresh local produce and artisan foods.",
  },
  // Add more markets as needed
];

const LocalMarkets = () => {
  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-4">Local Grocery Markets</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {markets.map((market) => (
          <div
            key={market.id}
            className="border rounded-lg p-4 hover:shadow-md transition-shadow duration-300"
          >
            <h3 className="text-lg font-semibold">{market.name}</h3>
            <p>{market.description}</p>
            <button className="mt-2 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-700 transition-colors duration-200">
              View Details
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LocalMarkets;
