import Link from "next/link";
import { useRouter } from "next/router";

const NavBar: React.FC = () => {
    const router = useRouter();

    const scrollToPricing = (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => {
        e.preventDefault();
        const pricingSection = document.getElementById("pricing");
        if (pricingSection) {
            pricingSection.scrollIntoView({ behavior: "smooth" });
        }
    };

    return (
        <nav className="bg-white border-gray-200 dark:bg-gray-900 h-16">
            <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
                <Link href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
                    <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Skin Disease Identifier</span>
                </Link>
                <div className="hidden w-full md:block md:w-auto" id="navbar-default">
                    <ul className="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
                        <li>
                            <Link href="/" className={`block py-2 px-3 rounded md:p-0 ${router.pathname === '/' ? 'text-blue-700 dark:text-blue-500' : 'text-gray-900 hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent'}`} aria-current="page">Home</Link>
                        </li>
                        <li>
                            <a href="#pricing" onClick={scrollToPricing} className="block py-2 px-3 rounded md:p-0 text-gray-900 hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Pricing</a>
                        </li>
                        <li>
                            <Link href="/login" className={`block py-2 px-3 rounded md:p-0 ${router.pathname === '/login' ? 'text-blue-700 dark:text-blue-500' : 'text-gray-900 hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent'}`}>Login</Link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default NavBar;