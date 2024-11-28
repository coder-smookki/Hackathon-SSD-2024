import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent } from "@/components/ui/card";
import SidebarLayout from "@/layout";
import {MeetingFormValues} from "@/types/Meetings.ts";
import MeetingService from "@/services/MeetingService.ts";
import {toast} from "sonner";

const CreateApplicationPage: React.FC = () => {
    const {
        register,
        formState: { errors },
        handleSubmit,
        reset,
    } = useForm<MeetingFormValues>({
        defaultValues: {
            isMicrophoneOn: true,
            isVideoOn: true,
            isWaitingRoomEnabled: true,
            needVideoRecording: false,
            isNotifyAccepted: false,
        },
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    const onSubmit = async (data: MeetingFormValues) => {
        setLoading(true);
        setError(null);
        setSuccess(null);

        try {
            const response = await MeetingService.createMeeting(data);
            console.log("Response:", response);
            setSuccess("Мероприятие успешно создано!");
            toast("Мероприятие успешно создано!", {
                description: 'Вы можете посмотреть свои мероприятия в разделе "Мои мероприятия".',
                action: {
                    label: "Понятно",
                    onClick: () => console.log("Понятно"),
                },
            })
            reset(); // Очистка полей формы
        } catch (err) {
            console.error(err);
            setError("Не удалось создать мероприятие. Перепроверьте все даты.");
            toast("Не удалось создать мероприятие!", {
                description: 'Проверьте, указали ли Вы все необходимые поля для создания заявки.',
                action: {
                    label: "Понятно",
                    onClick: () => console.log("Понятно"),
                },
            })
        } finally {
            setLoading(false);
        }
    };


    return (
        <SidebarLayout>
            <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl text-center my-10 mx-5">
                Создание мероприятия
            </h1>
            <Card className="w-[93vw] max-w-2xl mx-auto mb-5">
                <CardContent>
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                        {/* Поле name */}
                        <div className="mt-5">
                            <Label htmlFor="name">
                                Название <span className="text-red-500">*</span>
                            </Label>
                            <Input
                                id="name"
                                type="text"
                                {...register("name", {
                                    required: "Это поле обязательно",
                                    minLength: { value: 3, message: "Минимальная длина 3 символа" },
                                    maxLength: { value: 100, message: "Максимальная длина 100 символов" },
                                })}
                            />
                            {errors.name && (
                                <p className="text-sm text-red-500">{errors.name.message}</p>
                            )}
                        </div>

                        {/* Поле startedAt */}
                        <div>
                            <Label htmlFor="startedAt">Начало мероприятия <span className="text-red-500">*</span></Label>
                            <Input
                                id="startedAt"
                                type="datetime-local"
                                {...register("startedAt", { required: "Это поле обязательно" })}
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
                                {...register("endedAt")}
                            />
                            {errors.endedAt && (
                                <p className="text-sm text-red-500">{errors.endedAt.message}</p>
                            )}
                        </div>

                        {/* Поле duration */}
                        <div>
                            <Label htmlFor="duration">Продолжительность (минуты) <span className="text-red-500">*</span></Label>
                            <Input
                                id="duration"
                                type="number"
                                {...register("duration", {
                                    required: "Это поле обязательно",
                                    min: { value: 5, message: "Длительность минимум 5 минут" }
                                })}
                            />
                            {errors.duration && (
                                <p className="text-sm text-red-500">{errors.duration.message}</p>
                            )}
                        </div>

                        {/* Поле participantsCount */}
                        <div>
                            <Label htmlFor="participantsCount">Количество участников <span className="text-red-500">*</span></Label>
                            <Input
                                id="participantsCount"
                                type="number"
                                {...register("participantsCount", {
                                    required: "Это поле обязательно",
                                    min: { value: 1, message: "Минимум 1 участник" }
                                })}
                            />
                            {errors.participantsCount && (
                                <p className="text-sm text-red-500">{errors.participantsCount.message}</p>
                            )}
                        </div>

                        {/* Поле sendNotificationsAt */}
                        <div>
                            <Label htmlFor="sendNotificationsAt">Время уведомлений <span
                                className="text-red-500">*</span></Label>
                            <Input
                                id="sendNotificationsAt"
                                type="datetime-local"
                                {...register("sendNotificationsAt", {required: "Это поле обязательно"})}
                            />
                            <p className="text-sm text-gray-300 mt-1 ml-2">Должно быть раньше времени начала мероприятия</p>
                            {errors.sendNotificationsAt && (
                                <p className="text-sm text-red-500">{errors.sendNotificationsAt.message}</p>
                            )}
                        </div>

                        {/* Поле isMicrophoneOn */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="isMicrophoneOn"
                                {...register("isMicrophoneOn", { required: "Это поле обязательно" })}
                            />
                            <Label htmlFor="isMicrophoneOn">Микрофон включен <span className="text-red-500">*</span></Label>
                        </div>

                        {/* Поле isVideoOn */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="isVideoOn"
                                {...register("isVideoOn", { required: "Это поле обязательно" })}
                            />
                            <Label htmlFor="isVideoOn">Видео включено <span className="text-red-500">*</span></Label>
                        </div>

                        {/* Поле isWaitingRoomEnabled */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="isWaitingRoomEnabled"
                                {...register("isWaitingRoomEnabled", { required: "Это поле обязательно"})}
                            />
                            <Label htmlFor="isWaitingRoomEnabled">Комната ожидания включена <span className="text-red-500">*</span></Label>
                        </div>

                        {/* Поле needVideoRecording */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="needVideoRecording"
                                {...register("needVideoRecording")}
                            />
                            <Label htmlFor="needVideoRecording">Необходима видеозапись ВКС</Label>
                        </div>

                        {/* Поле roomId */}
                        <div>
                            <Label htmlFor="roomId">ID комнаты</Label>
                            <Input
                                id="roomId"
                                type="number"
                                {...register("roomId")}
                            />
                            {errors.roomId && (
                                <p className="text-sm text-red-500">{errors.roomId.message}</p>
                            )}
                        </div>

                        {/* Поле comment */}
                        <div>
                            <Label htmlFor="comment">Комментарий</Label>
                            <Input
                                id="comment"
                                type="text"
                                {...register("comment", {
                                    maxLength: { value: 1000, message: "Максимальная длина 1000 символов" }
                                })}
                            />
                            {errors.comment && (
                                <p className="text-sm text-red-500">{errors.comment.message}</p>
                            )}
                        </div>

                        {/* Поле isNotifyAccepted */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="isNotifyAccepted"
                                {...register("isNotifyAccepted")}
                            />
                            <Label htmlFor="isNotifyAccepted">Уведомления о принявших приглашение</Label>
                        </div>

                        <Button type="submit" variant="default" className="w-full" disabled={loading}>
                            {loading ? "Создание..." : "Создать"}
                        </Button>

                        {error && (
                            <div className="text-red-500 text-center mt-10">{error}</div>
                        )}
                        {success && (
                            <div className="text-green-500 text-center mt-10">{success}</div>
                        )}
                    </form>
                </CardContent>
            </Card>
        </SidebarLayout>
    );
};

export default CreateApplicationPage;
