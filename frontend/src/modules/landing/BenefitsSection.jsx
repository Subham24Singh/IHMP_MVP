import React from "react";
import { benefits } from "./landingData";
import { CheckCircle, Heart } from "lucide-react";

const BenefitsSection = () => (
  <section className="py-24 bg-gradient-to-br from-blue-50 to-indigo-50">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid lg:grid-cols-2 gap-16 items-center">
        <div className="animate-fade-in-up">
          <h2 className="text-4xl font-bold text-gray-900 mb-8">
            Transform Your Healthcare Experience
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of patients and healthcare providers who have revolutionized their medical management with our comprehensive platform.
          </p>
          <div className="space-y-4">
            {benefits.map((benefit, idx) => (
              <div key={idx} className="flex items-center space-x-3">
                <CheckCircle className="h-6 w-6 text-green-500" />
                <span className="text-gray-700 text-lg">{benefit}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="relative animate-fade-in-up" style={{animationDelay: '0.2s'}}>
          <div className="bg-white rounded-2xl shadow-2xl p-8 transform rotate-2 hover:rotate-0 transition-transform duration-500">
            <div className="flex items-center mb-6">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center">
                <Heart className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <h3 className="font-semibold text-gray-900">Health Dashboard</h3>
                <p className="text-gray-600">Real-time insights</p>
              </div>
            </div>
            <div className="space-y-4">
              <div className="h-2 bg-gray-200 rounded-full">
                <div className="h-2 bg-gradient-to-r from-green-400 to-green-600 rounded-full w-4/5"></div>
              </div>
              <div className="h-2 bg-gray-200 rounded-full">
                <div className="h-2 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full w-3/5"></div>
              </div>
              <div className="h-2 bg-gray-200 rounded-full">
                <div className="h-2 bg-gradient-to-r from-purple-400 to-purple-600 rounded-full w-4/6"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
);

export default BenefitsSection;