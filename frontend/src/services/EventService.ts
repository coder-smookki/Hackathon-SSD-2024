import $api from "../http";
import axios, {AxiosResponse} from "axios";
import {IEventsData} from "../types/Events.ts";

export default class EventService {
    static async fetchEvents(page: number, rowsPerPage: number): Promise<AxiosResponse<IEventsData>> {
        try {
            return await $api.get<IEventsData>(`/events`, {
                params: { page, rowsPerPage },
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