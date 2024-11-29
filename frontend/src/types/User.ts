import {User} from "@/types/Meetings.ts";
import {BaseData} from "@/types/Base.ts";

export interface IUser {
    id: number;
    departmentId: number;
    post: null | string;
    permissions: string[];
    login: string;
    email: string;
    lastName: string;
    firstName: string;
    middleName: string;
    birthday: null | string;
    phone: null | string;
    updatedAt: string;
    priority: number;
    roles: IRole[];
    department: IDepartment;
}

export interface IRole {
    name: string;
    description: string;
    id: number;
    permissions: string[];
}

export interface IDepartment {
    name: string;
    shortName: string;
    address: string;
    email: string;
    parentId: null | number;
    id: number;
    ldapName: null | string;
}

export interface ICheckUserResponse extends BaseData<User> {}
