import axios from 'axios';
import { AuthResponse } from '../types/auth/Auth.ts';
import {getRefreshToken} from "@/helpers/jwtHelpers.ts";

export const API_URL = 'https://test.vcc.uriit.ru/api';
export const TELEGRAM_API_URL = 'https://arzyo4-176-59-5-221.ru.tuna.am/api';

const $api = axios.create({
    baseURL: API_URL,
});

export const $telegram_api = axios.create({
    baseURL: TELEGRAM_API_URL,
});

$api.interceptors.request.use((config) => {
    config.headers['Authorization'] = `Bearer ${localStorage.getItem("token")}`;
    return config;
})

$api.interceptors.response.use((config) => {
    return config;
}, async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status == 401 && error.config && !error.config._isRetry) {
        originalRequest._isRetry = true;
        try {
            const response = await axios.post<AuthResponse>(`${API_URL}/auth/refresh-token`, {
                    "token": localStorage.getItem("refreshToken")
            });
            localStorage.setItem('refreshToken', getRefreshToken(response.data.token));
            localStorage.setItem('token', response.data.token);
            return $api.request(originalRequest);
        } catch {
            localStorage.removeItem("token");
            localStorage.removeItem("refreshToken");
            console.log("НЕ АВТОРИЗОВАН")
        }
    }
    throw error;
})

export default $api;