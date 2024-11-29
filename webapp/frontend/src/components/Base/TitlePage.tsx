import React from 'react';

interface TitlePageProps {
    text: string;
}

const TitlePage: React.FC<TitlePageProps> = ({ text }) => {
    return (
        <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl text-center my-10 mx-5">
            {text}
        </h1>
    );
};

export default TitlePage;