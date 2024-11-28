import React from 'react';
import LoginPage from "@/pages/LoginPage.tsx";
import {Route, Routes} from "react-router";
import NotFoundPage from "@/pages/NotFoundPage.tsx";
import MeetingsPage from "@/pages/MeetingsPage.tsx";
import ProtectedRoute from "@/hoc/ProtectedRoute.tsx";
import { ThemeProvider } from '@/components/theme-provider.tsx';
import ProfilePage from "@/pages/ProfilePage.tsx";
import CreateMeetingPage from "@/pages/CreateMeetingPage.tsx";
import MeetingDetailsPage from "@/pages/DetailsMeetingPage.tsx";
import UserMeetingsPage from "@/pages/UserMeetingsPage.tsx";
import QuestionsPage from "@/pages/QuestionsPage.tsx";

const App: React.FC = () => {
    return (
        <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
            <Routes>
                <Route path="/login" element={<LoginPage/>} />
                <Route path="/" element={<LoginPage/>} />
                <Route
                    path="/meetings"
                    element={
                        <ProtectedRoute>
                            <MeetingsPage/>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/meetings/:id"
                    element={
                        <ProtectedRoute>
                            <MeetingDetailsPage/>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/my-meetings"
                    element={
                        <ProtectedRoute>
                            <UserMeetingsPage/>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/profile"
                    element={
                        <ProtectedRoute>
                            <ProfilePage/>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/create-meeting"
                    element={
                        <ProtectedRoute>
                            <CreateMeetingPage/>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/faq"
                    element={
                        <ProtectedRoute>
                            <QuestionsPage/>
                        </ProtectedRoute>
                    }
                />
                <Route path="*" element={<NotFoundPage />} />
            </Routes>
        </ThemeProvider>
    );
};

export default App;
