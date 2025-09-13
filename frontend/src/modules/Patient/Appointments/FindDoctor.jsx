import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getDoctors } from "../../../api/api";
import { Search, Filter, MapPin, Clock, Star, Calendar, ChevronRight, Heart } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function FindDoctor() {
  const [doctors, setDoctors] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [specialtyFilter, setSpecialtyFilter] = useState("");
  const [activeTab, setActiveTab] = useState("all");

  useEffect(() => {
    const fetchDoctors = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found. Redirecting to login.");
        navigate('/auth');
        return;
      }

      try {
        setIsLoading(true);
        const data = await getDoctors(token);
        setDoctors(data);
      } catch (err) {
        console.error("Failed to fetch doctors:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDoctors();
  }, [navigate]);

  const filteredDoctors = doctors.filter((doctor) => {
    const matchesSearch = doctor.full_name?.toLowerCase().includes(searchQuery.toLowerCase()) || 
                         doctor.specialty?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSpecialty = specialtyFilter ? doctor.specialty === specialtyFilter : true;
    return matchesSearch && matchesSpecialty;
  });

  const specialties = [...new Set(doctors.map(doc => doc.specialty).filter(Boolean))];

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Finding the best doctors for you...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Find a Doctor</h1>
          <p className="mt-2 text-gray-600">Book appointments with top specialists near you</p>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="relative max-w-2xl">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-xl bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:outline-none transition-all duration-200"
              placeholder="Search doctors, specialties, or conditions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="mt-6 flex space-x-4 overflow-x-auto pb-2 scrollbar-hide">
            <button
              onClick={() => setActiveTab("all")}
              className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap ${
                activeTab === "all"
                  ? "bg-blue-100 text-blue-700"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              All Specialties
            </button>
            {specialties.slice(0, 6).map((specialty) => (
              <button
                key={specialty}
                onClick={() => {
                  setActiveTab(specialty);
                  setSpecialtyFilter(specialty);
                }}
                className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap ${
                  activeTab === specialty
                    ? "bg-blue-100 text-blue-700"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {specialty}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Doctors List */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900">
            {filteredDoctors.length} {filteredDoctors.length === 1 ? "Doctor" : "Doctors"} Available
          </h2>
          <div className="relative">
            <select
              className="appearance-none bg-white border border-gray-300 rounded-lg pl-3 pr-8 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={specialtyFilter}
              onChange={(e) => {
                setSpecialtyFilter(e.target.value);
                setActiveTab(e.target.value || "all");
              }}
            >
              <option value="">Filter by specialty</option>
              {specialties.map((spec) => (
                <option key={spec} value={spec}>
                  {spec}
                </option>
              ))}
            </select>
            <div className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
              <Filter className="h-4 w-4 text-gray-400" />
            </div>
          </div>
        </div>

        <AnimatePresence>
          {filteredDoctors.length > 0 ? (
            <motion.div
              variants={container}
              initial="hidden"
              animate="show"
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              {filteredDoctors.map((doctor) => (
                <motion.div
                  key={doctor.id}
                  variants={item}
                  className="bg-white rounded-2xl shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden border border-gray-100"
                >
                  <div className="p-5">
                    <div className="flex items-start space-x-4">
                      <div className="relative">
                        <img
                          src={doctor.photo_url || "https://randomuser.me/api/portraits/doctors/men/1.jpg"}
                          alt={doctor.full_name}
                          className="h-20 w-20 rounded-xl object-cover border-2 border-white shadow-sm"
                        />
                        <div className="absolute -bottom-2 -right-2 bg-white rounded-full p-1 shadow-md">
                          <div className="bg-blue-100 text-blue-700 text-xs font-medium px-2 py-1 rounded-full flex items-center">
                            <Star className="h-3 w-3 fill-current text-yellow-400 mr-1" />
                            {doctor.average_rating?.toFixed(1) || '4.8'}
                          </div>
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="text-lg font-semibold text-gray-900 truncate">
                              {doctor.full_name}
                            </h3>
                            <p className="text-sm text-blue-600 font-medium">
                              {doctor.specialty || 'General Practitioner'}
                            </p>
                          </div>
                          <button className="text-gray-400 hover:text-red-500 transition-colors">
                            <Heart className="h-5 w-5" />
                          </button>
                        </div>
                        
                        <div className="mt-2 flex items-center text-sm text-gray-500">
                          <MapPin className="h-4 w-4 text-gray-400 mr-1" />
                          <span className="truncate">
                            {doctor.clinic_address || '123 Medical Center, City'}
                          </span>
                        </div>
                        
                        <div className="mt-3 flex items-center text-sm text-gray-500">
                          <Clock className="h-4 w-4 text-gray-400 mr-1" />
                          <span>Available {doctor.available_days || 'Mon-Fri'}</span>
                        </div>
                        
                        <div className="mt-3 flex justify-between items-center">
                          <div>
                            <p className="text-xs text-gray-500">Next available</p>
                            <p className="text-sm font-medium text-gray-900">
                              {doctor.next_available || 'Today, 3:00 PM'}
                            </p>
                          </div>
                          <button
                            onClick={() => navigate(`/patient/dashboard/appointments/doctor/${doctor.id}`)}
                            className="flex items-center text-blue-600 hover:text-blue-800 text-sm font-medium"
                          >
                            View Profile
                            <ChevronRight className="h-4 w-4 ml-1" />
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-gray-100">
                      <button
                        onClick={() => console.log("Book Now clicked for:", doctor.full_name)}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded-xl flex items-center justify-center transition-colors"
                      >
                        <Calendar className="h-4 w-4 mr-2" />
                        Book Appointment
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          ) : (
            <div className="text-center py-12">
              <div className="mx-auto h-24 w-24 text-gray-300 mb-4">
                <svg
                  className="h-full w-full"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1}
                    d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900">No doctors found</h3>
              <p className="mt-1 text-gray-500">
                Try adjusting your search or filter to find what you're looking for.
              </p>
              <button
                onClick={() => {
                  setSearchQuery('');
                  setSpecialtyFilter('');
                  setActiveTab('all');
                }}
                className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Clear all filters
              </button>
            </div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}