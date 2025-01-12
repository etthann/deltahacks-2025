import NavBar from "@/components/NavBar";
import Footer from "@/components/Footer";
import Link from 'next/link';
import '../styles/globals.css';
import PricingCard from "@/components/PricingCard";
import Contact from "@/components/Contact";

const Home: React.FC = () => {
    return (
        <div className="m-0 p-0 min-h-screen flex flex-col justify-between bg-blue-500">
            <div className="min-h-screen flex flex-col justify-between">
                <NavBar />

                <div className="flex flex-col items-center justify-center text-center text-white p-8 mt-2">
                    <h1 className="text-5xl font-bold mb-4">Skin Disease Identifier</h1>
                    <p className="text-xl mb-13">Using AI to help you identify skin diseases</p>
                </div>

                <div className="flex flex-col items-center justify-center text-center text-white p-8 mt-5">
                    {/* About Me Section */}
                    <div className="bg-blue-900 text-white p-10 mt-5 rounded-lg shadow-lg mb-12" style={{ marginTop: '-30px' }}>
                        <div className="max-w-5xl mx-auto text-center">
                            <p className="text-lg mb-4">
                                Welcome to the Skin Disease Identifier! Our mission is to leverage the power of artificial intelligence to help you identify skin diseases quickly and accurately. Our team is dedicated to providing you with the best tools and resources to take care of your skin health.
                            </p>
                            <p className="text-lg">
                                Whether you are a healthcare professional or someone looking to understand more about your skin condition, our platform is designed to assist you with ease and precision. Thank you for trusting us with your skin health journey.
                            </p>
                        </div>
                    </div>

                    <Link href="/login" legacyBehavior>
                        <a className="bg-blue-700 hover:bg-blue-900 text-white max-w-xs w-full font-bold py-3 text-2x1 px-4 rounded mt-8">Login</a>
                    </Link>
                </div>
            </div>

            {/* Pricing Page Plan */}

            <div id="pricing" className="flex flex-col justify-between mt-12">
                <h1 className="text-4xl font-bold mt-12 text-white text-center">Pricing Plans</h1>
                <br /><br />
                <div className="flex flex-row items-center justify-center space-x-6 mt-12 mb-12 w-full">
                    <PricingCard planType="Free" features={["Checking History", "Unlimited Uses", "Treatments"]} strikeThrough={[false, true, true]} />
                    <PricingCard planType="Paid" features={["Checking History", "Unlimited Uses", "Treatments"]} strikeThrough={[false, false, false]} />

                </div>
            </div>

            {/* Contact Page */}
            <div id="contact" className="flex flex-col justify-between mt-12">
                <h1 className="text-4xl font-bold mt-12 text-white text-center">Contact Us</h1>
                <br /><br />
                <Contact />
            </div>

            <br/>
            <br/>

            <Footer />
        </div>
    )
}

export default Home;