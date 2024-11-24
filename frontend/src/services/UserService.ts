import $api from "../http";
import axios, {AxiosResponse} from "axios";
import {IUser} from "@/types/User.ts";

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
}