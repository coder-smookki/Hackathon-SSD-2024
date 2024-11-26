import React from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent } from "@/components/ui/card";
import SidebarLayout from "@/layout";

interface ApplicationFormValues {
    isOfflineMeeting: boolean;
    roomId: number;
    name: string;
    startedAt: string;
    endedAt: string;
    duration: number;
}

const CreateMeetingPage: React.FC = () => {
    const {
        register,
        formState: { errors },
        handleSubmit,
    } = useForm<ApplicationFormValues>();

    const onSubmit = (data: ApplicationFormValues) => {
        console.log("Form Data:", data);
        // Здесь можно отправить данные на сервер
    };

    return (
        <SidebarLayout>
            <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-10 text-center mt-10">
                Создание заявки
            </h1>
            <Card className="w-[93vw] max-w-2xl mx-auto">
                <CardContent>
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                        {/* Поле roomId */}
                        <div className="mt-5">
                            <Label htmlFor="roomId">ID комнаты</Label>
                            <Input
                                id="roomId"
                                type="number"
                                {...register("roomId", {
                                    required: "Это поле обязательно",
                                    valueAsNumber: true,
                                })}
                            />
                            {errors.roomId && (
                                <p className="text-sm text-red-500">{errors.roomId.message}</p>
                            )}
                        </div>

                        {/* Поле name */}
                        <div>
                            <Label htmlFor="name">Название</Label>
                            <Input
                                id="name"
                                type="text"
                                {...register("name", {
                                    required: "Это поле обязательно"
                                })}
                            />
                            {errors.name && (
                                <p className="text-sm text-red-500">{errors.name.message}</p>
                            )}
                        </div>

                        {/* Поле startedAt */}
                        <div>
                            <Label htmlFor="startedAt">Начало мероприятия</Label>
                            <Input
                                id="startedAt"
                                type="datetime-local"
                                {...register("startedAt", {
                                    required: "Это поле обязательно",
                                })}
                            />
                            {errors.startedAt && (
                                <p className="text-sm text-red-500">{errors.startedAt.message}</p>
                            )}
                        </div>

                        {/* Поле endedAt */}
                        <div>
                            <Label htmlFor="endedAt">Конец мероприятия</Label>
                            <Input
                                id="endedAt"
                                type="datetime-local"
                                {...register("endedAt", {
                                    required: "Это поле обязательно",
                                })}
                            />
                            {errors.endedAt && (
                                <p className="text-sm text-red-500">{errors.endedAt.message}</p>
                            )}
                        </div>

                        {/* Поле duration */}
                        <div>
                            <Label htmlFor="duration">Продолжительность (минуты)</Label>
                            <Input
                                id="duration"
                                type="number"
                                {...register("duration", {
                                    required: "Это поле обязательно",
                                    valueAsNumber: true,
                                })}
                            />
                            {errors.duration && (
                                <p className="text-sm text-red-500">{errors.duration.message}</p>
                            )}
                        </div>

                        {/* Поле isOfflineMeeting */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="isOfflineMeeting"
                                {...register("isOfflineMeeting")}
                            />
                            <Label htmlFor="isOfflineMeeting">Офлайн мероприятие</Label>
                        </div>

                        {/* Кнопка отправки */}
                        <Button type="submit" variant="default" className="w-full">
                            Создать
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </SidebarLayout>
    );
};

export default CreateMeetingPage;
