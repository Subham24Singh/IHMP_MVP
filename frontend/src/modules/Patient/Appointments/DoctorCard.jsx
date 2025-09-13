import React from 'react';
import { Link } from 'react-router-dom';

const DoctorCard = ({ doctor }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center gap-4 mb-4">
        <img 
          src={doctor.photo_url} 
          alt="Doctor Photo" 
          className="w-24 h-24 rounded-full object-cover"
        />
        <div>
          <h2 className="text-xl font-semibold">{doctor.full_name}</h2>
          <p className="text-gray-600">{doctor.specialty}</p>
          <div className="flex items-center gap-2 mt-2">
            <span className="text-yellow-400">⭐</span>
            <span className="text-gray-700">{doctor.average_rating.toFixed(1)}</span>
            <span className="text-gray-500">({doctor.total_ratings} reviews)</span>
          </div>
        </div>
      </div>
      
      <div className="mt-4">
        <p className="text-gray-600">{doctor.bio}</p>
      </div>
      
      <div className="mt-4 flex justify-between">
        <Link 
          to={`/doctors/${doctor.id}/profile`} 
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
        >
          View Profile
        </Link>
        <Link 
          to={`/appointments/book/${doctor.id}`} 
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors"
        >
          Book Appointment
        </Link>
      </div>
    </div>
  );
};

export default DoctorCard;
