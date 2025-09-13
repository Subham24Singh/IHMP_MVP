import { Calendar, HeartPulse, Pill, Activity, ClipboardList, Mic, Bell, ChevronRight } from "lucide-react";

export default function DashboardHome() {
  return (
    <>
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-8 mb-8 shadow-lg flex items-center animate-fade-in-up">
        <div>
          <div className="text-2xl font-bold text-white mb-1">Welcome back, John Doe!</div>
          <div className="text-white text-lg">Your next appointment is in 2 hours. Stay healthy and take care!</div>
        </div>
      </div>
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow flex flex-col items-center animate-fade-in-up">
          <div className="flex items-center gap-2 text-gray-500 text-sm mb-1">
            <Calendar className="h-5 w-5 text-blue-600" /> Upcoming Appointments
          </div>
          <div className="text-3xl font-bold text-blue-700">3</div>
          <div className="text-green-500 text-xs mt-1">↑ 12%</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow flex flex-col items-center animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
          <div className="flex items-center gap-2 text-gray-500 text-sm mb-1">
            <HeartPulse className="h-5 w-5 text-green-600" /> Health Score
          </div>
          <div className="text-3xl font-bold text-green-600">92%</div>
          <div className="text-red-500 text-xs mt-1">↓ 5%</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow flex flex-col items-center animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
          <div className="flex items-center gap-2 text-gray-500 text-sm mb-1">
            <Pill className="h-5 w-5 text-yellow-500" /> Active Prescriptions
          </div>
          <div className="text-3xl font-bold text-yellow-500">2</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow flex flex-col items-center animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
          <div className="flex items-center gap-2 text-gray-500 text-sm mb-1">
            <Activity className="h-5 w-5 text-red-500" /> Last Checkup
          </div>
          <div className="text-2xl font-bold text-red-600">2 weeks ago</div>
          <div className="text-red-500 text-xs mt-1">─</div>
        </div>
      </div>
      {/* Upcoming Appointments & Recent Activity */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 shadow flex flex-col animate-fade-in-up">
          <div className="flex items-center justify-between mb-4">
            <div className="font-bold text-lg">Upcoming Appointments</div>
            <button className="text-blue-600 hover:underline text-sm flex items-center">
              View All <ChevronRight className="h-4 w-4 ml-1" />
            </button>
          </div>
          <div className="space-y-3 overflow-y-auto max-h-56">
            <div className="flex items-center justify-between p-3 rounded-lg bg-blue-50">
              <div>
                <div className="font-semibold text-gray-900">Dr. Sarah Johnson</div>
                <div className="text-sm text-gray-500">Cardiology</div>
                <div className="text-xs text-gray-400">Today • 2:30 PM • Room 301</div>
              </div>
              <span className="bg-blue-200 text-blue-700 px-3 py-1 rounded-full text-xs font-semibold">In-Person</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-purple-50">
              <div>
                <div className="font-semibold text-gray-900">Dr. Michael Chen</div>
                <div className="text-sm text-gray-500">Dermatology</div>
                <div className="text-xs text-gray-400">Tomorrow • 10:00 AM • Virtual</div>
              </div>
              <span className="bg-purple-200 text-purple-700 px-3 py-1 rounded-full text-xs font-semibold">Virtual</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-blue-50">
              <div>
                <div className="font-semibold text-gray-900">Dr. Emily Rodriguez</div>
                <div className="text-sm text-gray-500">General Practice</div>
                <div className="text-xs text-gray-400">Next week • In-Person</div>
              </div>
              <span className="bg-blue-200 text-blue-700 px-3 py-1 rounded-full text-xs font-semibold">In-Person</span>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow flex flex-col animate-fade-in-up">
          <div className="font-bold text-lg mb-4">Recent Activity</div>
          <div className="space-y-3 overflow-y-auto max-h-56">
            <div className="flex items-center gap-3">
              <Calendar className="h-5 w-5 text-blue-600" />
              <div>
                <div className="font-semibold text-gray-900">Cardiology Consultation</div>
                <div className="text-xs text-gray-500">2 hours ago</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <ClipboardList className="h-5 w-5 text-green-600" />
              <div>
                <div className="font-semibold text-gray-900">Lab Results Updated</div>
                <div className="text-xs text-gray-500">4 hours ago</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Mic className="h-5 w-5 text-purple-600" />
              <div>
                <div className="font-semibold text-gray-900">Telemedicine Session</div>
                <div className="text-xs text-gray-500">1 day ago</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Bell className="h-5 w-5 text-orange-500" />
              <div>
                <div className="font-semibold text-gray-900">Medication Reminder</div>
                <div className="text-xs text-gray-500">3 days ago</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}