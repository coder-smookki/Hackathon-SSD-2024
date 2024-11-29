import React from "react";
import { IUser } from "@/types/User";

interface ProfileDetailsProps {
    profile: IUser;
}

const ProfileDetails: React.FC<ProfileDetailsProps> = ({ profile }) => (
    <div className="space-y-4">
        <p className="break-words">
            <strong>Имя:</strong> {profile.firstName} {profile.lastName} {profile.middleName}
        </p>
        <p>
            <strong>Логин:</strong> {profile.login}
        </p>
        <p>
            <strong>Почта:</strong> {profile.email}
        </p>
        <p>
            <strong>Телефон:</strong> {profile.phone || "Отсутствует"}
        </p>
        <p>
            <strong>Дата рождения:</strong> {profile.birthday || "Отсутствует"}
        </p>
        <DepartmentDetails department={profile.department} />
        <RoleList roles={profile.roles} />
    </div>
);

const DepartmentDetails: React.FC<{ department?: IUser["department"] }> = ({ department }) => (
    <div>
        <strong>Отдел:</strong>
        <ul className="list-disc list-inside mt-2">
            <li>
                <strong>Краткое имя:</strong> {department?.shortName || "Отсутствует"}
            </li>
            <li>
                <strong>Адрес:</strong> {department?.address || "Отсутствует"}
            </li>
        </ul>
    </div>
);

const RoleList: React.FC<{ roles?: { name: string }[] }> = ({ roles }) => (
    <div>
        <strong>Роли:</strong>
        <ul className="list-disc list-inside mt-2">
            {roles && roles.length > 0 ? (
                roles.map((role, index) => <li key={index}>{role.name || "Отсутствует"}</li>)
            ) : (
                <li>Отсутствует</li>
            )}
        </ul>
    </div>
);

export default ProfileDetails;
