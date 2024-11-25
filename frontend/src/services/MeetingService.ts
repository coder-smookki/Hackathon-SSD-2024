import $api from "../http";
import axios, {AxiosResponse} from "axios";
import {IMeetingsData} from "../types/Meetings.ts";

export default class MeetingService {
    static async fetchEvents(page: number, rowsPerPage: number, toDatetime: string, fromDatetime: string): Promise<AxiosResponse<IMeetingsData>> {
        try {
            return await $api.get<IMeetingsData>(`/meetings`, {
                params: {
                    "toDatetime": toDatetime,
                    "fromDatetime": fromDatetime,
                    "rowsPerPage": rowsPerPage,
                    "page": page
                },
            });
        } catch (error) {
            // Обработка ошибки
            if (axios.isAxiosError(error)) {
                // Обработка ошибки, возвращенной сервером
                console.error('Login error:', error.response?.data?.message || 'Unknown error');
                throw new Error(error.response?.data?.message || 'Login failed');
            } else {
                // Обработка других ошибок (например, проблемы с сетью)
                console.error('An unexpected error occurred:', error);
                throw new Error('Login failed due to a network error');
            }
        }
    }
}