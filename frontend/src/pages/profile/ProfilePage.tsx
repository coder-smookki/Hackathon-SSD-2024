import React, { useEffect, useState } from "react";
import UserService from "@/services/UserService.ts";
import { IUser } from "@/types/user/User.ts";
import { Card, CardContent } from "@/components/ui/card.tsx";
import { Skeleton } from "@/components/ui/skeleton.tsx";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert.tsx";
import SidebarLayout from "@/layouts/MainLayout.tsx";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar.tsx";
import ProfileDetails from "@/components/Profile/ProfileDetails.tsx";
import TitlePage from "@/components/Base/TitlePage.tsx";

const ProfilePage: React.FC = () => {
    const [profile, setProfile] = useState<IUser | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    useEffect(() => {
        const fetchUserProfile = async () => {
            setIsLoading(true);
            try {
                const response = await UserService.fetchProfile();
                setProfile(response.data);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };
        fetchUserProfile();
    }, []);

    return (
        <SidebarLayout>
            <TitlePage text="Ваш профиль"/>
            {isLoading ? (
                <div className="flex justify-center">
                    <Card className="w-80 p-4">
                        <Skeleton className="h-6 w-1/2 mb-4" />
                        <Skeleton className="h-4 w-3/4 mb-2" />
                        <Skeleton className="h-4 w-1/3" />
                    </Card>
                </div>
            ) : error ? (
                <div className="flex justify-center items-center">
                    <Alert variant="destructive" className="w-80">
                        <AlertTitle>Ошибка</AlertTitle>
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                </div>
            ) : (
                <Card className="w-[93vw] max-w-2xl mx-auto my-8">
                    <CardContent>
                        {profile ? (
                            <>
                                <Avatar className="my-5">
                                    <AvatarImage src="https://github.com/shadcn.png" />
                                    <AvatarFallback>
                                        {profile.firstName[0] + profile.lastName[0]}
                                    </AvatarFallback>
                                </Avatar>
                                <ProfileDetails profile={profile} />
                            </>
                        ) : (
                            <p>Нет данных профиля.</p>
                        )}
                    </CardContent>
                </Card>
            )}
        </SidebarLayout>
    );
};

export default ProfilePage;
