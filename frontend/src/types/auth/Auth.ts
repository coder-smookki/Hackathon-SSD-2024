import {IUser} from "@/types/user/User.ts";

export interface AuthResponse {
    token: string;
    user: IUser;
    tutorialsProgress: Record<string, unknown>;
}

export interface IToken {
    user: IUser;
    token_expired_at: number;
    token_created_at: number;
    refresh_token: string;
}
