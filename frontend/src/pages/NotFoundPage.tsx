import React from 'react';
import { Button } from '../components/ui/button.tsx';
import {Link} from "react-router";

const NotFoundPage: React.FC = () => {
    return (
        <div className={"m-5"}>
            <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-10 text-center">
                Страница не найдена
            </h1>

            <Button asChild>
                <Link to="/meetings">Назад</Link>
            </Button>
        </div>
    );
};

export default NotFoundPage;