import React from "react";
import { Heart, Stethoscope, ArrowRight, Zap, Award, Star } from "lucide-react";

const HeroSection = ({ onGetStarted }) => (
  <section className="relative py-32 px-4 sm:px-6 lg:px-8 overflow-hidden">
    {/* Animated Background Blobs */}
    <div className="absolute inset-0 pointer-events-none">
      <div className="absolute top-20 left-10 w-72 h-72 bg-blue-400/10 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-indigo-400/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-purple-400/5 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
    </div>
    <div className="max-w-7xl mx-auto text-center relative">
      {/* Trust Badge */}
      <div className="animate-fade-in-up mb-8">
        <div className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200/50 text-blue-800 rounded-full text-sm font-medium shadow-lg backdrop-blur-sm">
          <Award className="h-4 w-4 mr-2 text-blue-600" />
          <span className="font-semibold">Trusted by healthcare professionals worldwide</span>
          <div className="ml-2 flex space-x-1">
            {[...Array(5)].map((_, i) => (
              <Star key={i} className="h-3 w-3 fill-yellow-400 text-yellow-400" />
            ))}
          </div>
        </div>
      </div>
      {/* Heading */}
      <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-8 leading-tight tracking-tight animate-fade-in-up" style={{animationDelay: '0.2s'}}>
        <span className="block mb-3 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600">
          Intelligent Healthcare
        </span>
        <span className="block text-gray-800">Management Platform</span>
      </h1>
      {/* Subtitle */}
      <p className="text-xl lg:text-2xl text-gray-600 mb-12 max-w-4xl mx-auto leading-relaxed font-light animate-fade-in-up" style={{animationDelay: '0.4s'}}>
        Revolutionizing healthcare with <span className="font-semibold text-blue-600">AI-powered tools</span> that streamline medical processes, enhance patient care, and reduce administrative burden for healthcare professionals.
      </p>
      {/* CTA Buttons */}
      <div className="flex flex-col sm:flex-row gap-6 justify-center mb-20 animate-fade-in-up" style={{animationDelay: '0.6s'}}>
        <button
          className="group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-10 py-5 text-lg shadow-2xl hover:shadow-blue-500/25 transition-all duration-700 transform hover:scale-105 hover:-translate-y-2 animate-button-float rounded"
          onClick={() => onGetStarted("patient")}
        >
          <Heart className="mr-3 h-5 w-5 group-hover:animate-pulse" />
          Get Started as Patient
          <ArrowRight className="ml-3 h-5 w-5 group-hover:translate-x-2 transition-transform duration-500" />
        </button>
        <button
          className="group border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white px-10 py-5 text-lg shadow-xl hover:shadow-indigo-500/25 transition-all duration-700 transform hover:scale-105 hover:-translate-y-2 animate-button-float rounded"
          onClick={() => onGetStarted("doctor")}
        >
          <Stethoscope className="mr-3 h-5 w-5 group-hover:animate-pulse" />
          Healthcare Provider Access
          <Zap className="ml-3 h-5 w-5 group-hover:rotate-12 transition-transform duration-500" />
        </button>
      </div>
    </div>
  </section>
);

export default HeroSection;