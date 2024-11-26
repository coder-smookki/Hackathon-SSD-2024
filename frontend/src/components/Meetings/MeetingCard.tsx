import React from "react";
import {Card, CardContent, CardHeader, CardTitle} from "../ui/card.tsx";
import {IMeeting} from "@/types/Meetings.ts";

interface MeetingCardProps {
    meeting: IMeeting;
}

const MeetingCard: React.FC<MeetingCardProps> = ({ meeting }) => (
    <Card>
        <CardHeader>
            <CardTitle>{meeting.name}</CardTitle>
        </CardHeader>
        <CardContent>
            <p><strong>Начало:</strong> {meeting.startedAt ? new Date(meeting.startedAt).toLocaleString() : "Не указано"}</p>
            <p><strong>Окончание:</strong> {meeting.endedAt ? new Date(meeting.endedAt).toLocaleString() : "Не указано"}</p>
            <p><strong>Длительность:</strong> {meeting.duration ? `${meeting.duration} мин.` : "Не указано"}</p>
            <p><strong>Статус:</strong> {meeting.state ? (meeting.state == "ended" ? "Окончено" : "Забронировано") : "Не указано"}</p>
        </CardContent>
    </Card>
);

export default MeetingCard;
