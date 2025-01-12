import React from 'react';
import ItemList from './ItemList';

interface PricingCardProps {
    features: string[];
    strikeThrough: boolean[];
    planType: string;
}

const PricingCard: React.FC<PricingCardProps> = ({ features, strikeThrough, planType }) => {
    return (
        <div className="max-w-md h-auto w-full bg-blue-900 border border-blue-800 rounded-lg shadow dark:bg-darkblue-900 dark:border-blue-700 p-12">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">{planType} Plan</h3>
            <ul role="list" className="space-y-5 my-7">
                {features.map((feature, index) => (
                    <ItemList key={index} text={feature} isStrikethrough={strikeThrough[index]} />
                ))}
            </ul>
            <button
                onClick={() => (window.location.href = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')}
                className="w-full px-5 py-3 text-lg font-medium text-center text-white bg-blue-800 rounded-lg hover:bg-blue-900 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-700 dark:hover:bg-blue-800 dark:focus:ring-blue-900"
            >
                Get started
            </button>
        </div>
    );
};

export default PricingCard;