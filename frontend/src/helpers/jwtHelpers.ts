import {IToken} from "../types/auth/Auth.ts";
import {jwtDecode} from "jwt-decode";

export const getRefreshToken = (token: string) => {
    try {
        const decoded: IToken = jwtDecode(token);
        return decoded.refresh_token;
    } catch (error) {
        return `Ошибка при декодировании токена: ${error}`;
    }
}

export const getDecodedToken = (token: string): IToken | null => {
    try {
        return jwtDecode<IToken>(token);
    } catch (error) {
        return null;
    }
}

export const getUserIdFromToken = (): number | null => {
    const token = localStorage.getItem("token");
    let tokenData: IToken | null = null;

    if (token) {
        tokenData = getDecodedToken(token);
    }

    return tokenData ? tokenData.user.id : null;
};