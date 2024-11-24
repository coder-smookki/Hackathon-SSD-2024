import React from 'react';
import LoginPage from "@/pages/LoginPage.tsx";
import {Route, Routes} from "react-router";
import NotFoundPage from "@/pages/NotFoundPage.tsx";
import EventsPage from "@/pages/EventsPage.tsx";
import ProtectedRoute from "@/hoc/ProtectedRoute.tsx";
import { ThemeProvider } from '@/components/theme-provider.tsx';
import ProfilePage from "@/pages/ProfilePage.tsx";

const App: React.FC = () => {
    return (
        <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
            <Routes>
                <Route path="/login" element={<LoginPage/>} />
                <Route
                    path="/events"
                    element={
                        <ProtectedRoute>
                            <EventsPage/>
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
                <Route path="*" element={<NotFoundPage />} />
            </Routes>
        </ThemeProvider>
    );
};

export default App;
