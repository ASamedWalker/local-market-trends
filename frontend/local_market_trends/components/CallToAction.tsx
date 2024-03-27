const CallToAction: React.FC = () => {
  return (
    <div className="bg-blue-600 text-white text-center p-8">
      <h2 className="text-2xl font-bold mb-4">Stay Ahead of Market Trends!</h2>
      <p className="mb-4">
        Sign up for our newsletter to get the latest updates.
      </p>
      <button className="bg-white text-blue-600 font-semibold py-2 px-4 rounded hover:bg-gray-100">
        Subscribe Now
      </button>
    </div>
  );
};

export default CallToAction;
