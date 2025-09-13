import React from "react";
import { Heart, Shield, CheckCircle } from "lucide-react";

const AuthBranding = () => (
  <div className="hidden lg:flex lg:w-1/2 flex-col justify-center px-16 relative">
    <div className="flex items-center mb-8 animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
      <div className="p-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600">
        <Heart className="h-8 w-8 text-white" />
      </div>
      <span className="font-bold text-3xl text-gray-900 ml-4">IHMP</span>
    </div>
    <h1
      className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6 leading-tight animate-fade-in-up"
      style={{ animationDelay: "0.2s" }}
    >
      <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600">
        Secure Access
      </span>
      <br />
      <span className="text-gray-800">to Healthcare</span>
    </h1>
    <p
      className="text-xl text-gray-600 mb-8 leading-relaxed animate-fade-in-up"
      style={{ animationDelay: "0.3s" }}
    >
      Join thousands of healthcare professionals and patients who trust our platform for secure, efficient healthcare management.
    </p>
    <div className="space-y-4">
      <div className="flex items-center space-x-3 animate-fade-in-up" style={{ animationDelay: "0.4s" }}>
        <div className="p-2 bg-green-100 rounded-full">
          <Shield className="h-5 w-5 text-green-600" />
        </div>
        <span className="text-gray-700">HIPAA Compliant & Secure</span>
      </div>
      <div className="flex items-center space-x-3 animate-fade-in-up" style={{ animationDelay: "0.5s" }}>
        <div className="p-2 bg-blue-100 rounded-full">
          <CheckCircle className="h-5 w-5 text-blue-600" />
        </div>
        <span className="text-gray-700">24/7 Available Access</span>
      </div>
      <div className="flex items-center space-x-3 animate-fade-in-up" style={{ animationDelay: "0.6s" }}>
        <div className="p-2 bg-purple-100 rounded-full">
          <Heart className="h-5 w-5 text-purple-600" />
        </div>
        <span className="text-gray-700">Patient-Centered Care</span>
      </div>
    </div>
  </div>
);

export default AuthBranding;