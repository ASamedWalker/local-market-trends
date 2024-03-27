import Link from "next/link";

const Navbar = () => {
  return (
    <nav className="bg-blue-500 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="font-semibold text-xl">Local Market Trends</div>
        <div>
          <Link href="/" className="px-4 hover:underline">
            Home
          </Link>
          <Link href="/markets" className="px-4 hover:underline">
            Markets
          </Link>
          <Link href="/about" className="px-4 hover:underline">
            About
          </Link>
        </div>
      </div>
    </nav>
  );
};


export default Navbar;