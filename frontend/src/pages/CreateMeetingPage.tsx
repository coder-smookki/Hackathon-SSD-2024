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
import BuildingsList from "@/components/Filter/BuildingsList.tsx";
import UserService from "@/services/UserService.ts";

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
    const [selectedBuilding, setSelectedBuilding] = useState<number | null>(null);
    const [selectedRoom, setSelectedRoom] = useState<number | null>(null);
    const [participants, setParticipants] = useState<string[]>([""]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    const addParticipant = () => {
        setParticipants([...participants, ""]);
    };

    const removeParticipant = (index: number) => {
        setParticipants(participants.filter((_, i) => i !== index));
    };

    const onParticipantChange = (value: string, index: number) => {
        const updatedParticipants = [...participants];
        updatedParticipants[index] = value;
        setParticipants(updatedParticipants);
    };

    const onSubmit = async (data: MeetingFormValues) => {
        setLoading(true);
        setError(null);
        setSuccess(null);

        try {
            if (selectedBuilding && !selectedRoom) {
                setError("Выберите комнату для выбранного строения.");
                toast("Ошибка при создании мероприятия!", {
                    description: "Пожалуйста, выберите комнату для выбранного строения.",
                    action: {
                        label: "Понятно",
                        onClick: () => console.log("Понятно"),
                    },
                });
                return;
            } else if (participants.length === 0) {
                setError("Необходимо добавить хотя бы одного участника!");
                toast("Ошибка при создании мероприятия!", {
                    description: "Пожалуйста, добавьте участников.",
                    action: {
                        label: "Понятно",
                        onClick: () => console.log("Понятно"),
                    },
                });
                return;
            }

            if (selectedRoom) {
                data.roomId = selectedRoom;
            }

            if (!Array.isArray(data.participants)) {
                data.participants = [];
            }

            for (const email of participants) {
                if (!email.trim()) {
                    toast("Ошибка при создании мероприятия!", {
                        description: "Email не может быть пустым!.",
                        action: {
                            label: "Понятно",
                            onClick: () => console.log("Понятно"),
                        },
                    });
                    return;
                }

                const userResponse = await UserService.checkParticipant(email);

                if (userResponse) {
                    const user = userResponse;
                    console.log(user, user.id, user.email)
                    data.participants.push(user);
                } else {
                    toast("Ошибка при создании мероприятия!", {
                        description: `Участник с email ${email} не найден!`,
                        action: {
                            label: "Понятно",
                            onClick: () => console.log("Понятно"),
                        },
                    });
                    return;
                }
            }

            const response = await MeetingService.createMeeting(data);
            console.log("ВКС:", response);
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
                                    minLength: {value: 3, message: "Минимальная длина 3 символа"},
                                    maxLength: {value: 100, message: "Максимальная длина 100 символов"},
                                })}
                            />
                            {errors.name && (
                                <p className="text-sm text-red-500">{errors.name.message}</p>
                            )}
                        </div>

                        {/* Поле startedAt */}
                        <div>
                            <Label htmlFor="startedAt">Начало мероприятия <span
                                className="text-red-500">*</span></Label>
                            <Input
                                id="startedAt"
                                type="datetime-local"
                                {...register("startedAt", {required: "Это поле обязательно"})}
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
                                    min: {value: 5, message: "Длительность минимум 5 минут"}
                                })}
                            />
                            {errors.duration && (
                                <p className="text-sm text-red-500">{errors.duration.message}</p>
                            )}
                        </div>

                        {/* Поле participantsCount */}
                        <div>
                            <Label htmlFor="participantsCount">Максимальное количество участников <span
                                className="text-red-500">*</span></Label>
                            <Input
                                id="participantsCount"
                                type="number"
                                {...register("participantsCount", {
                                    required: "Это поле обязательно",
                                    min: {value: 1, message: "Минимум 1 участник"}
                                })}
                            />
                            {errors.participantsCount && (
                                <p className="text-sm text-red-500">{errors.participantsCount.message}</p>
                            )}
                        </div>

                        {/* Поле participants */}
                        <div className="flex flex-col">
                            <Label>Участники</Label>
                            {participants.map((participant, index) => (
                                <div key={index} className="flex items-center gap-2 mt-2">
                                    <Input
                                        type="text"
                                        placeholder={`Участник ${index + 1}`}
                                        value={participant}
                                        onChange={(e) => onParticipantChange(e.target.value, index)}
                                    />
                                    <Button
                                        type="button"
                                        variant="ghost"
                                        onClick={() => removeParticipant(index)}
                                    >
                                        Удалить
                                    </Button>
                                </div>
                            ))}
                            <Button
                                type="button"
                                variant="outline"
                                className="mt-2"
                                onClick={addParticipant}
                            >
                                + Добавить участника
                            </Button>
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
                            <p className="text-sm text-gray-300 mt-1 ml-2">Должно быть раньше времени начала
                                мероприятия</p>
                            {errors.sendNotificationsAt && (
                                <p className="text-sm text-red-500">{errors.sendNotificationsAt.message}</p>
                            )}
                        </div>

                        {/* Поле buildings */}
                        <BuildingsList
                            selectedBuildingId={selectedBuilding}
                            onBuildingSelect={setSelectedBuilding}
                            selectedRoomId={selectedRoom}
                            onRoomSelect={setSelectedRoom}
                        />

                        {/* Поле isMicrophoneOn */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="isMicrophoneOn"
                                {...register("isMicrophoneOn", {required: "Это поле обязательно"})}
                            />
                            <Label htmlFor="isMicrophoneOn">Микрофон включен <span
                                className="text-red-500">*</span></Label>
                        </div>

                        {/* Поле isVideoOn */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="isVideoOn"
                                {...register("isVideoOn", {required: "Это поле обязательно"})}
                            />
                            <Label htmlFor="isVideoOn">Видео включено <span className="text-red-500">*</span></Label>
                        </div>

                        {/* Поле isWaitingRoomEnabled */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="isWaitingRoomEnabled"
                                {...register("isWaitingRoomEnabled", {required: "Это поле обязательно"})}
                            />
                            <Label htmlFor="isWaitingRoomEnabled">Комната ожидания включена <span
                                className="text-red-500">*</span></Label>
                        </div>

                        {/* Поле needVideoRecording */}
                        <div className="flex items-center gap-2">
                            <Checkbox
                                id="needVideoRecording"
                                {...register("needVideoRecording")}
                            />
                            <Label htmlFor="needVideoRecording">Необходима видеозапись ВКС</Label>
                        </div>

                        {/* Поле comment */}
                        <div>
                            <Label htmlFor="comment">Комментарий</Label>
                            <Input
                                id="comment"
                                type="text"
                                {...register("comment", {
                                    maxLength: {value: 1000, message: "Максимальная длина 1000 символов"}
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
