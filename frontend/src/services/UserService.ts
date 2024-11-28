import $api from "../http";
import axios, {AxiosResponse} from "axios";
import { ICheckUserResponse, IUser} from "@/types/User.ts";
import {User} from "@/types/Meetings.ts";

export default class UserService {
    static async fetchProfile(): Promise<AxiosResponse<IUser>> {
        try {
            return await $api.get<IUser>(`/account/user-info`);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error('Ошибка получения профиля:', error.response?.data?.message || 'Неизвестная ошибка');
                throw new Error(error.response?.data?.message || 'Произошла ошибка при получении профиля');
            } else {
                console.error('Произошла непредвиденная ошибка:', error);
                throw new Error('Ошибка сети');
            }
        }
    }

    static async checkParticipant(email: string): Promise<User | null> {
        try {
            const response = await $api.get<ICheckUserResponse>(`/users?email=${email}`);
            const participants = response.data.data;
            if (participants.length === 0) {
                return null;
            }
            return participants[0];
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error('Ошибка проверки участника:', error.response?.data?.message || 'Неизвестная ошибка');
                throw new Error(error.response?.data?.message || 'Произошла ошибка при проверке участника');
            } else {
                console.error('Произошла непредвиденная ошибка:', error);
                throw new Error('Ошибка сети');
            }
        }
    }
}