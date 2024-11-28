import $api from "../http";
import {AuthResponse} from "../types/Auth.ts";
import axios, {AxiosResponse} from "axios";

export default class AuthService {
    static async login(login: string, password: string): Promise<AxiosResponse<AuthResponse>> {
        try {
            return await $api.post<AuthResponse>('/auth/login', {
                login,
                password,
                fingerprint: {},
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