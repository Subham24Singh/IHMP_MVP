import { NavLink } from "react-router-dom";
import {
  Calendar, FileText, Pill, ClipboardList, Syringe, Bell, Mic, FileBarChart2,
  UserCircle2, Settings, LogOut
} from "lucide-react";

const navItems = [
  { to: "", label: "Dashboard", icon: <Calendar /> },
  { to: "appointments", label: "Appointments & Follow-Ups", icon: <Calendar /> },
  { to: "ehr", label: "EHR Summary", icon: <FileText /> },
  { to: "prescriptions", label: "Prescription Management", icon: <Pill /> },
  { to: "lab-results", label: "Lab Results Management", icon: <ClipboardList /> },
  { to: "allergies", label: "Allergy Tracking", icon: <Syringe /> },
  { to: "reminders", label: "Reminders", icon: <Bell /> },
  { to: "transcription", label: "AI Doctor Transcription", icon: <Mic /> },
  { to: "health-logs", label: "Health Monitoring Logs", icon: <FileBarChart2 /> },
  { to: "profile", label: "Profile", icon: <UserCircle2 /> },
  { to: "settings", label: "Settings", icon: <Settings /> },
];

export default function Sidebar() {
  return (
    <aside className="w-72 bg-white border-r border-blue-100 flex flex-col p-6">
      <div className="flex items-center mb-10">
        <span className="font-extrabold text-2xl text-blue-700">IHMP</span>
        <span className="ml-2 text-sm text-gray-500">Healthcare Portal</span>
      </div>
      <div className="flex items-center mb-8">
        <div className="bg-blue-100 rounded-full p-2">
          <UserCircle2 className="h-8 w-8 text-blue-600" />
        </div>
        <div className="ml-3">
          <div className="font-bold text-lg text-gray-900">John Doe</div>
          <div className="text-blue-600 text-sm font-semibold">Patient</div>
        </div>
      </div>
      <nav className="flex-1 space-y-1">
        {navItems.map(item => (
          <NavLink
            key={item.label}
            to={item.to}
            end
            className={({ isActive }) =>
              `w-full flex items-center px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                isActive
                  ? "bg-blue-100 text-blue-700 shadow"
                  : "text-gray-700 hover:bg-blue-50"
              }`
            }
          >
            <span className="mr-3">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>
      <button className="mt-8 w-full flex items-center px-4 py-2 rounded-lg text-red-600 hover:bg-red-50 font-semibold transition">
        <LogOut className="mr-3" /> Logout
      </button>
    </aside>
  );
}