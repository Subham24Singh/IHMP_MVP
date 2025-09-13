import React from "react";
import { Navigate } from "react-router-dom";

function getUserRoleFromToken() {
  try {
    const token = localStorage.getItem("token");
    if (!token) return null;
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.role?.toLowerCase();
  } catch {
    return null;
  }
}

const ProtectedRoute = ({ allowedRoles, children }) => {
  const userRole = getUserRoleFromToken();
  if (!userRole) return <Navigate to="/auth" />;
  if (!allowedRoles.includes(userRole)) {
    // Redirect to correct dashboard if logged in but wrong role
    if (userRole === "patient") return <Navigate to="/patient/dashboard" />;
    if (userRole === "doctor") return <Navigate to="/doctor/dashboard" />;
    return <Navigate to="/auth" />;
  }
  return children;
};

export default ProtectedRoute;