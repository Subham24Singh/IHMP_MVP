import { Outlet, Link, useLocation } from "react-router-dom";
import {
  User,
  Calendar,
  FileText,
  Pill,
  FlaskConical,
  Bell,
  Mic,
  HeartPulse,
  Settings as SettingsIcon,
  LogOut,
  UserCircle,
} from "lucide-react";

const navItems = [
  { label: "Dashboard", icon: <HeartPulse className="h-5 w-5" />, path: "/" },
  { label: "Appointments", icon: <Calendar className="h-5 w-5" />, path: "appointments" },
  { label: "EHR", icon: <FileText className="h-5 w-5" />, path: "ehr" },
  { label: "Prescriptions", icon: <Pill className="h-5 w-5" />, path: "prescriptions" },
  { label: "Lab Results", icon: <FlaskConical className="h-5 w-5" />, path: "lab-results" },
  { label: "Allergies", icon: <Bell className="h-5 w-5" />, path: "allergies" },
  { label: "Reminders", icon: <Bell className="h-5 w-5" />, path: "reminders" },
  { label: "Transcription", icon: <Mic className="h-5 w-5" />, path: "transcription" },
  { label: "Health Logs", icon: <HeartPulse className="h-5 w-5" />, path: "health-logs" },
  { label: "Profile", icon: <User className="h-5 w-5" />, path: "profile" },
  { label: "Settings", icon: <SettingsIcon className="h-5 w-5" />, path: "settings" },
];

export default function PatientDashboard() {
  const location = useLocation();

  // Helper to get absolute path for each nav item
  const getAbsPath = (itemPath) =>
    `/patient/dashboard${itemPath === "/" ? "" : "/" + itemPath}`;

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-white">
      {/* Sidebar */}
      <aside className="w-64 bg-white/90 border-r border-blue-100 shadow-xl flex flex-col py-8 px-6 animate-fade-in-left">
        <div className="flex items-center mb-10">
          <div className="p-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600">
            <HeartPulse className="h-7 w-7 text-white" />
          </div>
          <span className="font-bold text-2xl text-gray-900 ml-3 tracking-tight">
            IHMP
          </span>
        </div>
        <nav className="flex-1">
          <ul className="space-y-2">
            {navItems.map((item) => {
              const absPath = getAbsPath(item.path);
              const isActive =
                location.pathname === absPath ||
                (item.path === "/" && location.pathname === "/patient/dashboard");
              return (
                <li key={item.label}>
                  <Link
                    to={absPath}
                    className={`flex items-center w-full px-4 py-3 rounded-lg transition-all duration-200 font-medium text-base gap-3 ${
                      isActive
                        ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg scale-105"
                        : "text-gray-700 hover:bg-blue-50"
                    }`}
                  >
                    {item.icon}
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
        <button className="mt-10 flex items-center gap-2 text-red-600 hover:text-red-800 transition-colors duration-200 font-semibold">
          <LogOut className="h-5 w-5" />
          Logout
        </button>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="flex items-center justify-between px-10 py-6 bg-white/80 shadow animate-fade-in-up">
          <div>
            <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight animate-fade-in-up">
              Welcome back, <span className="text-blue-600">Patient</span>
            </h1>
            <p className="text-gray-500 mt-1 animate-fade-in-up delay-100">
              Here’s your health summary and upcoming activities.
            </p>
          </div>
          <div className="flex items-center gap-4">
            <UserCircle className="h-12 w-12 text-blue-500 bg-blue-100 rounded-full shadow" />
            <span className="font-semibold text-gray-800 text-lg">John Doe</span>
          </div>
        </header>
        {/* Animated Main Content */}
        <main className="flex-1 p-8 animate-fade-in-up">
          <Outlet />
        </main>
      </div>
    </div>
  );
}