import { Bell, UserCircle2 } from "lucide-react";

export default function Topbar() {
  return (
    <div className="flex items-center justify-between mb-8">
      <div className="flex items-center">
        <span className="font-extrabold text-2xl text-blue-700">IHMP</span>
        <span className="ml-4 text-xl font-semibold text-gray-900">Welcome back, John Doe!</span>
      </div>
      <div className="flex items-center gap-4">
        <input
          type="text"
          placeholder="Search..."
          className="px-4 py-2 rounded-lg border border-blue-100 focus:ring-2 focus:ring-blue-400 outline-none bg-white text-gray-700"
        />
        <button className="relative">
          <Bell className="h-6 w-6 text-blue-600" />
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1.5">2</span>
        </button>
        <div className="bg-blue-100 rounded-full p-2">
          <UserCircle2 className="h-7 w-7 text-blue-600" />
        </div>
      </div>
    </div>
  );
}