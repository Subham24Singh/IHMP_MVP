import React from "react";
import { features } from "./landingData";

const featureIconColors = [
  "text-blue-600",
  "text-blue-600",
  "text-blue-600",
  "text-blue-600"
];

const FeaturesSection = () => (
  <section id="features" className="py-20 bg-white">
    <div className="max-w-7xl mx-auto px-4">
      <h2 className="text-4xl font-bold text-center mb-6 animate-fade-in-up">Why Choose IHMP?</h2>
      <p className="text-lg text-gray-600 text-center mb-12 animate-fade-in-up" style={{animationDelay: '0.2s'}}>
        Our platform combines cutting-edge technology with intuitive design to deliver exceptional healthcare experiences for everyone.
      </p>
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 animate-fade-in-up" style={{animationDelay: '0.4s'}}>
        {features.map((feature, idx) => {
          const Icon = feature.icon;
          return (
            <div key={idx} className="bg-blue-50 rounded-xl shadow p-6 text-center transition-all duration-500 transform hover:-translate-y-2 hover:shadow-2xl group">
              <div className="flex justify-center mb-4">
                <Icon className={`h-8 w-8 ${featureIconColors[idx]} group-hover:animate-pulse`} />
              </div>
              <div className="font-semibold text-lg mb-2 group-hover:text-blue-600 transition-colors duration-300">{feature.title}</div>
              <div className="text-gray-600">{feature.description}</div>
            </div>
          );
        })}
      </div>
    </div>
  </section>
);

export default FeaturesSection;