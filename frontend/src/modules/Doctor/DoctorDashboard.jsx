import React from "react";

const DoctorDashboard = () => (
  <div>
    <h2 className="text-2xl font-bold mb-4">Doctor dashboard</h2>
    {/* Add your appointments UI here */}
    <div className="bg-white rounded-xl shadow p-6">
      <p className="text-gray-600">No appointments scheduled yet.</p>
    </div>
  </div>
);

export default DoctorDashboard;