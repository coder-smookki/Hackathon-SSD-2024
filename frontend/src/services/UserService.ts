import $api from "../http";
import axios, {AxiosResponse} from "axios";
import {IUser} from "@/types/User.ts";
import {User} from "@/types/Meetings.ts";

interface checkUserResponse {
    rowsPerPage: number;
    page: number;
    rowsNumber: number;
    showDeleted: boolean;
    data: User[];
    sortBy: string;
}

export default class UserService {
    static async fetchProfile(): Promise<AxiosResponse<IUser>> {
        try {
            return await $api.get<IUser>(`/account/user-info`);
        } catch (error) {
            // Обработка ошибки
            if (axios.isAxiosError(error)) {
                // Обработка ошибки, возвращенной сервером
                console.error('Ошибка получения профиля:', error.response?.data?.message || 'Unknown error');
                throw new Error(error.response?.data?.message || 'Login failed');
            } else {
                // Обработка других ошибок (например, проблемы с сетью)
                console.error('An unexpected error occurred:', error);
                throw new Error('Login failed due to a network error');
            }
        }
    }

    static async checkParticipant(email: string): Promise<User | null> {
        try {
            const response = await $api.get<checkUserResponse>(`/users?email=${email}`);
            if (response.data.data.length === 0) {
                return null;
            }

            return response.data.data[0];
        } catch (error) {
            // Обработка ошибки
            if (axios.isAxiosError(error)) {
                // Обработка ошибки, возвращенной сервером
                console.error('Ошибка получения профиля:', error.response?.data?.message || 'Unknown error');
                throw new Error(error.response?.data?.message || 'Login failed');
            } else {
                // Обработка других ошибок (например, проблемы с сетью)
                console.error('An unexpected error occurred:', error);
                throw new Error('Login failed due to a network error');
            }
        }
    }
}