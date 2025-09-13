import React, { useCallback } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import AuthBranding from "./AuthBranding";
import AuthForm from "./AuthForm";

const AuthPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Always get the latest params and role from the URL
  const params = new URLSearchParams(location.search);
  const role = params.get("role") === "doctor" ? "doctor" : "patient";

  // Handler to update the URL when role is toggled
  const handleRoleSwitch = useCallback(
    (newRole) => {
      // Always use the latest location.search for params
      const newParams = new URLSearchParams(location.search);
      newParams.set("role", newRole);
      navigate({ search: newParams.toString() }, { replace: true });
    },
    [navigate, location.search]
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 relative overflow-hidden">
      <div className="flex min-h-screen relative">
        <AuthBranding />
        <div className="w-full lg:w-1/2 flex items-center justify-center p-4 lg:p-12">
          <AuthForm initialRole={role} onRoleSwitch={handleRoleSwitch} />
        </div>
      </div>
    </div>
  );
};

export default AuthPage;