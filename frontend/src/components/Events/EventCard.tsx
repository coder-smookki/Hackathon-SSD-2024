import React from "react";
import {Card, CardContent, CardHeader, CardTitle} from "../ui/card.tsx";

interface EventCardProps {
    name: string;
    startedAt: string;
    endedAt: string;
}

const EventCard: React.FC<EventCardProps> = ({ name, startedAt, endedAt }) => (
    <Card>
        <CardHeader>
            <CardTitle>{name}</CardTitle>
        </CardHeader>
        <CardContent>
            <p>Начало: {new Date(startedAt).toLocaleString()}</p>
            <p>Окончание: {new Date(endedAt).toLocaleString()}</p>
        </CardContent>
    </Card>
);

export default EventCard;
