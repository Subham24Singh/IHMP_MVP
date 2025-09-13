import React, { useState, useEffect } from "react"; // <--- Import useEffect here
import { Heart, Mail, Lock, User, Stethoscope, ArrowRight, Phone, CheckCircle, AlertTriangle } from "lucide-react";
import { useNavigate } from "react-router-dom"; // Import useNavigate as it's used in your AuthForm

const API_BASE = "http://127.0.0.1:8000/users"; // Change to your FastAPI backend base URL

// Accept onRoleSwitch as a prop from AuthPage
const AuthForm = ({ initialRole = "patient", onRoleSwitch }) => { // <--- Added onRoleSwitch prop
  const navigate = useNavigate(); // Initialize useNavigate

  const [isLogin, setIsLogin] = useState(true);
  const [selectedRole, setSelectedRole] = useState(initialRole); // Initialize with prop

  // --- FIX STARTS HERE ---
  // Use useEffect to update selectedRole when initialRole prop changes
  useEffect(() => {
    setSelectedRole(initialRole);
    // When role changes, also reset form data for a cleaner UX
    setFormData({
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      phone_number: "",
      registration_number: "",
    });
    setError("");
    setSuccess("");
  }, [initialRole]); // Dependency array: run this effect whenever initialRole changes
  // --- FIX ENDS HERE ---

  const [animKey, setAnimKey] = useState(0); // Kept for animation, though useEffect might handle resets implicitly

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    phone_number: "",
    registration_number: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Modified handleRoleSwitch to call the prop function
  const handleRoleSwitch = (role) => {
    if (role !== selectedRole) {
      setAnimKey((k) => k + 1); // Trigger animation (optional, but good for UX)
      setSelectedRole(role); // Update local state immediately
      onRoleSwitch(role); // <--- Propagate the role change up to AuthPage to update the URL
      setError("");
      setSuccess("");
      // Form data reset is now handled by the useEffect above,
      // which triggers when initialRole (from URL via AuthPage) changes.
      // This ensures data reset is in sync with URL.
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      if (isLogin) {
        // LOGIN
        const params = new URLSearchParams();
        params.append("username", formData.email);
        params.append("password", formData.password);

        const res = await fetch(`${API_BASE}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: params,
        });
        const data = await res.json();

        if (!res.ok) throw new Error(data.detail || "Login failed");

        const backendRole = (data.role || "").toLowerCase();
        if (!["patient", "doctor"].includes(backendRole)) {
          throw new Error("Invalid user role received from server.");
        }

        // Only allow login if backendRole matches the form's current selectedRole
        // This is a robust check, ensuring the user logs into the correct portal
        if (backendRole !== selectedRole) { // <--- Changed from initialRole to selectedRole
          throw new Error(`You are not authorized to access the ${selectedRole} portal.`);
        }

        localStorage.setItem("token", data.access_token);
        if (backendRole === "patient") {
          navigate("/patient/dashboard"); // <--- Use navigate from react-router-dom
        } else if (backendRole === "doctor") {
          navigate("/doctor/dashboard"); // <--- Use navigate from react-router-dom
        }
      } else {
        // REGISTER
        if (formData.password !== formData.confirmPassword) {
          setError("Passwords do not match");
          setLoading(false);
          return;
        }

        let endpoint = "";
        let payload = {};
        if (selectedRole === "doctor") {
          if (!formData.registration_number) {
            setError("Doctor registration requires a registration number.");
            setLoading(false);
            return;
          }
          endpoint = "/register_doctor";
          payload = {
            username: formData.username,
            email: formData.email,
            password: formData.password,
            confirm_password: formData.confirmPassword, // Frontend validation only, good to keep here
            phone_number: formData.phone_number,
            registration_number: formData.registration_number,
          };
        } else { // selectedRole === "patient"
          endpoint = "/register_patient";
          payload = {
            username: formData.username,
            email: formData.email,
            password: formData.password,
            confirm_password: formData.confirmPassword, // Frontend validation only
            phone_number: formData.phone_number,
          };
        }
        const res = await fetch(`${API_BASE}${endpoint}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Signup failed");
        setSuccess("Registration successful! Please sign in.");
        setIsLogin(true);
        // Reset form data after successful registration
        setFormData({
          username: "",
          email: "",
          password: "",
          confirmPassword: "",
          phone_number: "",
          registration_number: "",
        });
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-lg mx-auto">
      {/* Mobile Header (unchanged) */}
      <div className="text-center mb-8 lg:hidden animate-fade-in-up">
        <div className="flex items-center justify-center mb-4">
          <div className="p-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600">
            <Heart className="h-8 w-8 text-white" />
          </div>
          <span className="font-bold text-2xl text-gray-900 ml-3">IHMP</span>
        </div>
      </div>
      <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-2xl border border-blue-100 p-8 animate-fade-in-up transition-all duration-500 min-h-[540px] flex flex-col justify-center">
        <div className="text-center mb-6">
          <div className="text-3xl font-extrabold text-gray-900 tracking-tight">
            {isLogin ? "Welcome Back" : "Create Account"}
          </div>
          <div className="text-gray-600 mt-2">
            {isLogin
              ? "Sign in to access your healthcare portal"
              : "Join our secure healthcare platform"}
          </div>
        </div>
        {/* Role Selection */}
        <div className="flex justify-center mb-6 gap-2">
          <button
            type="button"
            onClick={() => handleRoleSwitch("patient")} // <--- Use handleRoleSwitch from AuthForm
            className={`flex items-center px-5 py-2.5 rounded-lg border transition-all duration-300 font-semibold text-base shadow-sm ${
              selectedRole === "patient"
                ? "bg-blue-600 text-white scale-105 shadow-lg"
                : "bg-gray-100 text-gray-700 hover:bg-blue-50"
            }`}
          >
            <User className="h-4 w-4 mr-2" />
            Patient
          </button>
          <button
            type="button"
            onClick={() => handleRoleSwitch("doctor")} // <--- Use handleRoleSwitch from AuthForm
            className={`flex items-center px-5 py-2.5 rounded-lg border transition-all duration-300 font-semibold text-base shadow-sm ${
              selectedRole === "doctor"
                ? "bg-blue-600 text-white scale-105 shadow-lg"
                : "bg-gray-100 text-gray-700 hover:bg-blue-50"
            }`}
          >
            <Stethoscope className="h-4 w-4 mr-2" />
            Doctor
          </button>
        </div>
        {/* Error */}
        {error && (
          <div className="mb-4 flex items-center justify-center gap-2 text-red-700 bg-red-50 border border-red-200 rounded-lg px-4 py-2 shadow animate-fade-in-up">
            <AlertTriangle className="h-5 w-5 text-red-500" />
            <span className="font-medium">{error}</span>
          </div>
        )}
        {/* Success */}
        {success && (
          <div className="mb-4 flex items-center justify-center gap-2 text-green-700 bg-green-50 border border-green-200 rounded-lg px-4 py-2 shadow animate-fade-in-up">
            <CheckCircle className="h-5 w-5 text-green-500 animate-bounce" />
            <span className="font-semibold">{success}</span>
          </div>
        )}
        {/* Animated form content */}
        <form
          key={animKey + (isLogin ? "login" : "signup") + selectedRole}
          onSubmit={handleSubmit}
          className="space-y-5 animate-fade transition-transform-opacity"
        >
          {!isLogin && (
            <>
              <div>
                <label className="block text-gray-700 font-medium mb-1">
                  Username
                </label>
                <input
                  name="username"
                  type="text"
                  className="w-full py-2 rounded border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all px-3"
                  value={formData.username}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 font-medium mb-1">
                  Phone Number
                </label>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    name="phone_number"
                    type="tel"
                    className="pl-10 w-full py-2 rounded border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                    value={formData.phone_number}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
              {selectedRole === "doctor" && (
                <div>
                  <label className="block text-gray-700 font-medium mb-1">
                    Registration Number
                  </label>
                  <input
                    name="registration_number"
                    type="text"
                    className="w-full py-2 rounded border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all px-3"
                    value={formData.registration_number}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              )}
              {/* Optional: Add allergies input for patients if needed */}
              {selectedRole === "patient" && (
                <div>
                  <label className="block text-gray-700 font-medium mb-1">
                    Allergies (optional)
                  </label>
                  <input
                    name="allergies"
                    type="text"
                    className="w-full py-2 rounded border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all px-3"
                    placeholder="e.g., Penicillin, Peanuts"
                    value={formData.allergies || ""} // Ensure controlled input
                    onChange={handleInputChange}
                  />
                </div>
              )}
            </>
          )}
          <div>
            <label htmlFor="email" className="block text-gray-700 font-medium mb-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                id="email"
                name="email"
                type="email"
                placeholder="Enter your email"
                className="pl-10 w-full py-2 rounded border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                value={formData.email}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>
          <div>
            <label htmlFor="password" className="block text-gray-700 font-medium mb-1">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                id="password"
                name="password"
                type="password"
                placeholder="Enter your password"
                className="pl-10 w-full py-2 rounded border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                value={formData.password}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>
          {!isLogin && (
            <div>
              <label className="block text-gray-700 font-medium mb-1">
                Confirm Password
              </label>
              <input
                name="confirmPassword"
                type="password"
                className="w-full py-2 rounded border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all px-3"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                required
              />
            </div>
          )}
          <button
            type="submit"
            disabled={loading}
            className={`w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white py-3 text-lg font-semibold rounded shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center ${
              loading ? "opacity-60 cursor-not-allowed" : ""
            }`}
          >
            {loading ? (
              <span className="animate-spin mr-2">⏳</span>
            ) : null}
            {isLogin ? "Sign In" : "Create Account"}
            <ArrowRight className="ml-2 h-5 w-5" />
          </button>
        </form>
        <div className="text-center mt-4">
          <button
            type="button"
            onClick={() => {
              setIsLogin(!isLogin);
              setError("");
              setSuccess("");
            }}
            className="text-blue-600 hover:text-blue-700 transition-colors duration-300 underline font-medium"
          >
            {isLogin
              ? "Don't have an account? Sign up"
              : "Already have an account? Sign in"}
          </button>
        </div>
        {isLogin && (
          <div className="text-center mt-2">
            <button
              type="button"
              className="text-sm text-gray-600 hover:text-gray-800 transition-colors duration-300 underline"
            >
              Forgot your password?
            </button>
          </div>
        )}
      </div>
      <div className="mt-6 text-center text-sm text-gray-600 animate-fade-in-up">
        By continuing, you agree to our{" "}
        <button className="text-blue-600 hover:text-blue-700 underline">
          Terms of Service
        </button>{" "}
        and{" "}
        <button className="text-blue-600 hover:text-blue-700 underline">
          Privacy Policy
        </button>
      </div>
    </div>
  );
};

export default AuthForm;