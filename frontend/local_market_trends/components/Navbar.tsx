import Search from "@/components/Search";

const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto flex justify-between items-center py-4 px-6 md:px-12">
        <span className="font-bold text-2xl tracking-tight">
          Local Market Trends
        </span>
        <Search />
      </div>
    </nav>
  );
};

export default Navbar;
