import $api from "../http";
import axios, { AxiosResponse } from "axios";
import { formatISO } from 'date-fns';
import {CreateMeetingResponse, GetMeetingResponse, IMeetingsData, MeetingFormValues} from "../types/Meetings";
import { getDecodedToken } from "@/utils/decodeToken";
import {IToken} from "@/types/Auth.ts";

export default class MeetingService {
    static async fetchMeetings(
        page: number,
        rowsPerPage: number,
        fromDatetime: string,
        toDatetime: string,
        state?: string,
        userId?: number | null
    ): Promise<AxiosResponse<IMeetingsData>> {
        try {
            const params: any = {
                toDatetime,
                fromDatetime,
                rowsPerPage,
                page,
            };

            if (userId) {
                params.userId = userId;
                params.userParticipant = userId;
            }
            if (state) {
                params.state = state;
            }
            console.log(params)
            return await $api.get<IMeetingsData>(`/meetings`, { params });
        } catch (error) {
            // Обработка ошибки
            if (axios.isAxiosError(error)) {
                console.error('Ошибка при получении мероприятий:', error.response?.data?.message || 'Неизвестная ошибка');
                throw new Error(error.response?.data?.message || 'Ошибка при получении мероприятий');
            } else {
                console.error('Произошла непредвиденная ошибка:', error);
                throw new Error('Ошибка сети');
            }
        }
    }

    static async fetchOneMeeting(id: number): Promise<AxiosResponse<GetMeetingResponse>> {
        try {
            return await $api.get<GetMeetingResponse>(`/meetings/${id}`);
        } catch (error) {
            // Обработка ошибки
            if (axios.isAxiosError(error)) {
                console.error('Ошибка при получении мероприятий:', error.response?.data?.message || 'Неизвестная ошибка');
                throw new Error(error.response?.data?.message || 'Ошибка при получении мероприятий');
            } else {
                console.error('Произошла непредвиденная ошибка:', error);
                throw new Error('Ошибка сети');
            }
        }
    }

    static async createMeeting(meeting: MeetingFormValues): Promise<AxiosResponse<CreateMeetingResponse>> {
        const token = localStorage.getItem("token");
        let tokenData: IToken | null = null;

        if (token) {
            tokenData = getDecodedToken(token);
        }

        const normalizedData = {
            name: meeting.name,
            comment: meeting.comment || null,
            participantsCount: Number(meeting.participantsCount),
            sendNotificationsAt: meeting.sendNotificationsAt,
            startedAt: formatISO(new Date(meeting.startedAt)),
            endedAt: meeting.endedAt || null,
            duration: Number(meeting.duration),
            ciscoSettings: {
                isMicrophoneOn: meeting.isMicrophoneOn,
                isVideoOn: meeting.isVideoOn,
                isWaitingRoomEnabled: meeting.isWaitingRoomEnabled,
                needVideoRecording: meeting.needVideoRecording,
            },
            vinteoSettings: {
                needVideoRecording: meeting.needVideoRecording,
            },
            participants: tokenData ? [
                {
                    id: tokenData.user.id || 0,
                    email: tokenData.user.email || "",
                    lastName: null,
                    firstName: null,
                    middleName: null,
                    isApproved: null,
                },
            ] : [],
            recurrenceUpdateType: "only",
            roomId: meeting.roomId,
            isVirtual: meeting.isVirtual || false,
            state: meeting.state || "booked",
            backend: meeting.backend || "cisco",
            organizedBy: {
                id: tokenData ? tokenData.user.id : 544,
            },
        };

        console.log(normalizedData);
        try {
            return await $api.post<CreateMeetingResponse>(`/meetings`, normalizedData);
        } catch (error) {
            // Обработка ошибки
            if (axios.isAxiosError(error)) {
                console.error('Ошибка при создании мероприятия:', error.response?.data?.message || 'Неизвестная ошибка');
                throw new Error(error.response?.data?.message || 'Ошибка при создании мероприятия');
            } else {
                console.error('Произошла непредвиденная ошибка:', error);
                throw new Error('Ошибка сети');
            }
        }
    }
}
