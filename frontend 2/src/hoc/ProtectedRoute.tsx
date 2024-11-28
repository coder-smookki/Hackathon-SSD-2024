import React from "react";
import { Navigate } from "react-router";

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const token = localStorage.getItem("token");

    if (!token) {
        localStorage.removeItem("token");
        localStorage.removeItem("refreshToken");
        return <Navigate to="/login" replace />;
    }

    return <>{children}</>;
};

export default ProtectedRoute;
