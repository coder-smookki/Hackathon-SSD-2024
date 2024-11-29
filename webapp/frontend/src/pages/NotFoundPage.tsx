import React from 'react';
import { Button } from '../components/ui/button.tsx';
import {Link} from "react-router";
import TitlePage from "@/components/Base/TitlePage.tsx";

const NotFoundPage: React.FC = () => {
    return (
        <div className={"m-5"}>
            <TitlePage text="Страница не найдена"/>

            <Button asChild>
                <Link to="/meetings">Назад</Link>
            </Button>
        </div>
    );
};

export default NotFoundPage;