import React from "react";
import { ArrowRight } from "lucide-react";

const CTASection = ({ onGetStarted }) => (
  <section className="py-24 bg-gradient-to-r from-blue-600 to-indigo-700 relative overflow-hidden">
    <div className="absolute inset-0 bg-black/10"></div>
    <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8 relative animate-fade-in-up">
      <h2 className="text-4xl font-bold text-white mb-6">
        Ready to Transform Your Healthcare Experience?
      </h2>
      <p className="text-xl text-blue-100 mb-12 leading-relaxed">
        Join thousands of patients and healthcare providers who trust IHMP for their medical management needs. Start your journey today.
      </p>
      <div className="flex flex-col sm:flex-row gap-6 justify-center">
        <button
          className="bg-white text-blue-600 hover:bg-gray-50 px-8 py-4 text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 rounded"
          onClick={() => onGetStarted("patient")}
        >
          Start as Patient
          <ArrowRight className="ml-2 h-5 w-5" />
        </button>
        <button
          className="border-2 border-white text-white hover:bg-white hover:text-blue-600 px-8 py-4 text-lg transition-all duration-300 transform hover:scale-105 rounded"
          onClick={() => onGetStarted("doctor")}
        >
          Healthcare Provider Portal
        </button>
      </div>
    </div>
  </section>
);

export default CTASection;