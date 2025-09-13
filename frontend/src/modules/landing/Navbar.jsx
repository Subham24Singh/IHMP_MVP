// src/modules/landing/Navbar.jsx
import React from "react";
import { Heart } from "lucide-react";

const Navbar = ({ onLogin }) => (
  <nav className="bg-white shadow-sm sticky top-0 z-50">
    <div className="max-w-7xl mx-auto px-6 flex justify-between items-center h-16">
      <div className="flex items-center">
        <Heart className="h-7 w-7 text-blue-600" />
        <span className="font-bold text-xl text-gray-900 ml-2">IHMP</span>
      </div>
      <div className="hidden md:flex items-center space-x-8">
        <a href="#features" className="text-gray-700 hover:text-blue-600">Features</a>
        <a href="#about" className="text-gray-700 hover:text-blue-600">About</a>
        <a href="#contact" className="text-gray-700 hover:text-blue-600">Contact</a>
        <button
          className="border border-blue-600 text-blue-600 px-5 py-2 rounded hover:bg-blue-600 hover:text-white transition"
          onClick={onLogin}
        >
          Login
        </button>
      </div>
    </div>
  </nav>
);

export default Navbar;