import React, { useState } from "react";

export default function BookingModal({ doctor, onClose, onBook }) {
  const [appointmentDate, setAppointmentDate] = useState("");

  if (!doctor) {
    return null; // Don't render the modal if the doctor object is undefined
  }

  const handleSubmit = () => {
    if (!appointmentDate) {
      alert("Please select a date and time.");
      return;
    }
    onBook(appointmentDate);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">Book Appointment with {doctor.full_name}</h2>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2">Select Date and Time</label>
          <input
            type="datetime-local"
            className="w-full border rounded-lg px-3 py-2"
            value={appointmentDate}
            onChange={(e) => setAppointmentDate(e.target.value)}
          />
        </div>
        <div className="flex justify-end gap-4">
          <button
            className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg"
            onClick={onClose}
          >
            Cancel
          </button>
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded-lg"
            onClick={handleSubmit}
          >
            Book Appointment
          </button>
        </div>
      </div>
    </div>
  );
}