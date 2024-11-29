import $api from "../http";
import axios, { AxiosResponse } from "axios";
import { formatISO } from 'date-fns';
import { CreateMeetingResponse, GetMeetingResponse, IMeetingsData, MeetingFormValues } from "../types/meetings/Meetings.ts";
import { getUserIdFromToken } from "@/helpers/jwtHelpers.ts";

// export const fetchMeetings = async (
//     page: number,
//     rowsPerPage: number,
//     fromDatetime: string,
//     toDatetime: string,
//     state?: string,
//     userId?: number | null
// ): Promise<{data: IMeetingsData}> => {
//     const params: any = {
//         toDatetime,
//         fromDatetime,
//         rowsPerPage,
//         page,
//     };
//
//     if (userId) {
//         params.userId = userId;
//         params.userParticipant = userId;
//     }
//
//     if (state) {
//         params.state = state;
//     }
//
//     return await $api.get('/meetings', { params });
// };

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
            return await $api.get<IMeetingsData>(`/meetings`, { params });
        } catch (error) {
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
            if (axios.isAxiosError(error)) {
                console.error('Ошибка при получении мероприятия:', error.response?.data?.message || 'Неизвестная ошибка');
                throw new Error(error.response?.data?.message || 'Ошибка при получении мероприятия');
            } else {
                console.error('Произошла непредвиденная ошибка:', error);
                throw new Error('Ошибка сети');
            }
        }
    }

    static async createMeeting(meeting: MeetingFormValues): Promise<AxiosResponse<CreateMeetingResponse>> {
        const userId = getUserIdFromToken();

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
            participants: meeting.participants,
            recurrenceUpdateType: "only",
            roomId: meeting.roomId,
            isVirtual: meeting.isVirtual || false,
            state: meeting.state || "booked",
            backend: "cisco",
            organizedBy: { id: userId }
        };

        try {
            return await $api.post<CreateMeetingResponse>(`/meetings`, normalizedData);
        } catch (error) {
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
