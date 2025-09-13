import React from "react";
import { Heart } from "lucide-react";

const Footer = () => (
  <footer className="bg-gray-900 text-white py-16 animate-fade-in-up">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid md:grid-cols-4 gap-8 mb-8">
        <div>
          <div className="flex items-center mb-6">
            <div className="p-2 rounded-lg bg-blue-600">
              <Heart className="h-6 w-6 text-white" />
            </div>
            <span className="font-bold text-xl ml-3">IHMP</span>
          </div>
          <p className="text-gray-400 leading-relaxed">
            Intelligent Healthcare Management Platform - Revolutionizing medical care through advanced technology and compassionate design.
          </p>
        </div>
        <div>
          <h3 className="font-semibold mb-6 text-lg">Platform</h3>
          <ul className="space-y-3 text-gray-400">
            <li className="hover:text-white transition-colors cursor-pointer">Patient Portal</li>
            <li className="hover:text-white transition-colors cursor-pointer">Doctor Dashboard</li>
            <li className="hover:text-white transition-colors cursor-pointer">EHR Management</li>
            <li className="hover:text-white transition-colors cursor-pointer">AI Transcription</li>
          </ul>
        </div>
        <div>
          <h3 className="font-semibold mb-6 text-lg">Support</h3>
          <ul className="space-y-3 text-gray-400">
            <li className="hover:text-white transition-colors cursor-pointer">Help Center</li>
            <li className="hover:text-white transition-colors cursor-pointer">Contact Us</li>
            <li className="hover:text-white transition-colors cursor-pointer">Privacy Policy</li>
            <li className="hover:text-white transition-colors cursor-pointer">Terms of Service</li>
          </ul>
        </div>
        <div>
          <h3 className="font-semibold mb-6 text-lg">Company</h3>
          <ul className="space-y-3 text-gray-400">
            <li className="hover:text-white transition-colors cursor-pointer">About Us</li>
            <li className="hover:text-white transition-colors cursor-pointer">Careers</li>
            <li className="hover:text-white transition-colors cursor-pointer">Security</li>
            <li className="hover:text-white transition-colors cursor-pointer">Compliance</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
        <p>&copy; {new Date().getFullYear()} IHMP. All rights reserved. Built with care for better healthcare.</p>
      </div>
    </div>
  </footer>
);

export default Footer;