import React from "react";
import {Card, CardContent, CardHeader, CardTitle} from "../ui/card.tsx";
import {IMeeting} from "@/types/meetings/Meetings.ts";
import {useNavigate} from "react-router";

interface MeetingCardProps {
    meeting: IMeeting;
}

const MeetingCard: React.FC<MeetingCardProps> = ({meeting}) => {
    const navigate = useNavigate();

    const handleCardClick = () => {
        navigate(`/meetings/${meeting.id}`);
    };

    return (
        <Card onClick={handleCardClick} style={{cursor: "pointer"}}>
            <CardHeader>
                <CardTitle>{meeting.name}</CardTitle>
            </CardHeader>
            <CardContent>
                <p>
                    <strong>Начало:</strong> {meeting.startedAt ? new Date(meeting.startedAt).toLocaleString() : "Не указано"}
                </p>
                <p>
                    <strong>Окончание:</strong> {meeting.endedAt ? new Date(meeting.endedAt).toLocaleString() : "Не указано"}
                </p>
                <p><strong>Длительность:</strong> {meeting.duration ? `${meeting.duration} мин.` : "Не указано"}</p>
                <strong>Статус:</strong>{" "}
                {{
                    ended: "Окончено",
                    booked: "Забронировано",
                    started: "Начато",
                    cancelled: "Отменено",
                }[meeting.state] || "Не указано"}
            </CardContent>
        </Card>
    );
};

export default MeetingCard;
