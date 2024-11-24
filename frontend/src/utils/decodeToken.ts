import {IToken} from "../types/Auth.ts";
import {jwtDecode} from "jwt-decode";

export const getRefreshToken = (token: string) => {
    try {
        const decoded: IToken = jwtDecode(token);
        return decoded.refresh_token;
    } catch (error) {
        return `Ошибка при декодировании токена: ${error}`;
    }
}