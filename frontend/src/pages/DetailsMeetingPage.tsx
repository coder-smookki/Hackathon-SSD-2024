import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router";
import { GetMeetingResponse } from "@/types/Meetings.ts";
import SidebarLayout from "@/layout.tsx";
import MeetingService from "@/services/MeetingService.ts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card.tsx";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table.tsx";
import { Button } from "@/components/ui/button.tsx";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const MeetingDetails: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [meeting, setMeeting] = useState<GetMeetingResponse | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchMeeting = async () => {
            try {
                const response = await MeetingService.fetchOneMeeting(Number(id));
                setMeeting(response.data);
            } catch (err) {
                setError("Ошибка при загрузке данных о встрече.");
            } finally {
                setLoading(false);
            }
        };
        fetchMeeting();
    }, [id]);
    console.log(meeting)
    return (
        <SidebarLayout>
            <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl text-center my-10 mx-3">
                Детали мероприятия
            </h1>

            {loading ? (
                <div className="flex justify-center">
                    <Card className="w-[93vw] max-w-2xl mx-auto my-8 p-6">
                        <Skeleton className="h-8 w-3/4 mb-4" />
                        <Skeleton className="h-6 w-1/2 mb-2" />
                        <Skeleton className="h-6 w-2/3 mb-2" />
                        <Skeleton className="h-6 w-1/4 mb-2" />
                        <Skeleton className="h-10 w-full mt-4" />
                    </Card>
                </div>
            ) : error ? (
                <div className="flex justify-center">
                    <Alert variant="destructive" className="w-[93vw] max-w-2xl mx-auto my-8">
                        <AlertTitle>Ошибка</AlertTitle>
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                </div>
            ) : meeting ? (
                <Card className="w-[93vw] max-w-2xl mx-auto my-8">
                    <CardHeader>
                        <CardTitle className="text-center text-3xl font-extrabold tracking-tight lg:text-5xl">
                            {meeting.name}
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <p>
                                <strong>Начало:</strong> {new Date(meeting.startedAt).toLocaleString()}
                            </p>
                            {meeting.endedAt && (
                                <p>
                                    <strong>Окончание:</strong> {new Date(meeting.endedAt).toLocaleString()}
                                </p>
                            )}
                            <p>
                                <strong>Длительность:</strong>{" "}
                                {Math.round(
                                    (new Date(meeting.endedAt).getTime() -
                                        new Date(meeting.startedAt).getTime()) /
                                    60000
                                )}{" "}
                                мин.
                            </p>
                            <p>
                                <strong>Количество участников:</strong> {meeting.participantsCount}
                            </p>
                            <p>
                                <strong>Платформа:</strong> {meeting.backend}
                            </p>
                            {/*<hr className={"border-dashed"}/>*/}
                            {/*<h2 className="text-xl font-semibold">Организатор:</h2>*/}
                            {/*<p>*/}
                            {/*    <strong>ФИО:</strong> {meeting?.organizedUser?.firstName} {meeting?.organizedUser?.middleName} {meeting?.organizedUser?.lastName}*/}
                            {/*    <br/>*/}
                            {/*    <strong>Email:</strong> {meeting?.organizedUser?.email}*/}
                            {/*</p>*/}
                            <hr className={"border-dashed"}/>
                            <h2 className="text-xl font-semibold">Участники:</h2>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>ФИО</TableHead>
                                        <TableHead>Email</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {meeting.participants.map((participant) => (
                                        <TableRow key={participant.id}>
                                            <TableCell>
                                                {participant.firstName} {participant.middleName}{" "}
                                                {participant.lastName}
                                            </TableCell>
                                            <TableCell>{participant.email}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                            <hr/>
                            <h2 className="text-xl font-semibold">Дополнительные детали:</h2>
                            <p>
                                <strong>ID встречи:</strong> {meeting.id}
                            </p>
                            <p>
                                <strong>ID комнаты:</strong>{" "}
                                {meeting.roomId ? meeting.roomId : "Не указано"}
                            </p>
                            <p>
                                <strong>Организовано пользователем ID:</strong> {meeting.organizedBy ? meeting.organizedBy : "Не указано"}
                            </p>
                        </div>
                    </CardContent>
                </Card>
            ) : (
                <p className="text-center">Встреча не найдена.</p>
            )}

            <div className="flex justify-center my-8">
                <Button onClick={() => navigate(-1)}>Вернуться</Button>
            </div>
        </SidebarLayout>
    );
};

export default MeetingDetails;
