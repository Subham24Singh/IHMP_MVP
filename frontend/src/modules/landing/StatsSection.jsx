import React from "react";
import { stats } from "./landingData";

const iconColors = [
  "text-blue-500",
  "text-green-500",
  "text-purple-500",
  "text-orange-500"
];

const StatsSection = () => (
  <section className="py-12 bg-gradient-to-b from-white to-blue-50">
    <div className="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 animate-fade-in-up">
      {stats.map((stat, idx) => {
        const Icon = stat.icon;
        return (
          <div
            key={idx}
            className="group bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-700 transform hover:scale-110 hover:-translate-y-3 border border-gray-100/50"
          >
            <div className="flex items-center justify-center mb-4">
              <div className="p-3 rounded-full bg-gradient-to-r from-gray-50 to-gray-100 group-hover:from-blue-50 group-hover:to-indigo-50 transition-all duration-500 group-hover:scale-110">
                <Icon className={`h-8 w-8 ${iconColors[idx]} group-hover:animate-pulse`} />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors duration-500">
              {stat.number}
            </div>
            <div className="text-gray-700 font-semibold mb-1 group-hover:text-blue-700 transition-colors duration-300">
              {stat.label}
            </div>
            <div className="text-gray-500 text-sm group-hover:text-gray-600 transition-colors duration-300">
              {stat.description}
            </div>
          </div>
        );
      })}
    </div>
  </section>
);

export default StatsSection;