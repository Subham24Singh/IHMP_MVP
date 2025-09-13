import React, { useState, useEffect } from 'react';
import DoctorCard from './DoctorCard';
import { useNavigate } from 'react-router-dom';

const DoctorsList = () => {
  const [doctors, setDoctors] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const response = await fetch('/api/appointments/doctors');
        const data = await response.json();
        setDoctors(data);
      } catch (error) {
        console.error('Error fetching doctors:', error);
      }
    };

    fetchDoctors();
  }, []);

  const handleBookAppointment = (doctorId) => {
    navigate(`/appointments/book/${doctorId}`);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Find a Doctor</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {doctors.map((doctor) => (
          <DoctorCard 
            key={doctor.id} 
            doctor={doctor}
          />
        ))}
      </div>
    </div>
  );
};

export default DoctorsList;
