import React, { ReactNode } from 'react';

interface FormProps {
    children: ReactNode;
}

const Form: React.FC<FormProps> = ({ children }) => {
    return (
        <form>
            <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                    Password
                </label>
                <input
                    id="password"
                    name="password"
                    type="password"
                    required
                    className="mt-1 block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-black focus:outline-none focus:ring-black sm:text-sm"
                />
            </div>
            {children}
        </form>
    );
};

export default Form;