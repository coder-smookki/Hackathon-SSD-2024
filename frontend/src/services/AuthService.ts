import $api, {$telegram_api} from "../http";
import {AuthResponse} from "../types/Auth.ts";
import axios, {AxiosResponse} from "axios";

export default class AuthService {
    static async login(login: string, password: string): Promise<AxiosResponse<AuthResponse>> {
        try {
            return await $api.post<AuthResponse>('/auth/login', { login, password });
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error('Ошибка авторизации:', error.response?.data?.message || 'Неизвестная ошибка');
                throw new Error(error.response?.data?.message || 'Произошла ошибка при попытке авторизации');
            } else {
                console.error('Произошла непредвиденная ошибка:', error);
                throw new Error('Ошибка сети');
            }
        }
    }

    static async fetchUserJWT(id: number) {
        try {
            const response = await $telegram_api.get(`/users_jwt/${id}`);
            if (response.status === 200) {
                const userJwt = response.data.user_jwt;
                localStorage.setItem('token', userJwt);
                return userJwt;
            }
        } catch (error) {
            console.error('Ошибка при получении user JWT:', error);
        }
    };
}