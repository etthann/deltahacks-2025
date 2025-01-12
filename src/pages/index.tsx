import NavBar from "@/components/NavBar";
import Footer from "@/components/Footer";
import Link from 'next/link';
import '../styles/globals.css';

const Home: React.FC = () => {
    return (
        <div className="m-0 p-0 min-h-screen flex flex-col justify-between">
            <div className="min-h-screen bg-cover bg-center bg-no-repeat bg-[url('/rocket_background.jpg')] flex flex-col justify-between">
                <NavBar />
                <div className="flex flex-col items-center justify-center text-center text-white p-8">
                    <h1 className="text-5xl font-bold mb-4">Skin Disease Identifier</h1>
                    <p className="text-xl mb-8">Using AI to help you identify skin diseases</p>
                    <Link href="/upload" legacyBehavior>
                        <a className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Try Me</a>
                    </Link>
                </div>
            </div>
            <Footer />
        </div>
    )
}

export default Home;