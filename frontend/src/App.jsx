import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LandingPage from "./modules/landing/LandingPage";
import AuthPage from "./modules/auth/AuthPage";
import PatientDashboard from "./modules/Patient/PatientDashboard";
import DashboardHome from "./modules/Patient/DashboardHome";
import Appointments from "./modules/Patient/Appointments/Appointments"; // Updated path for modular appointments
import BookDoctor from "./modules/Patient/Appointments/BookingModal"; // Added BookDoctor page
import EHR from "./modules/Patient/EHR";
import Prescriptions from "./modules/Patient/Prescriptions";
import LabResults from "./modules/Patient/LabResults";
import Allergies from "./modules/Patient/Allergies";
import Reminders from "./modules/Patient/Reminders";
import Transcription from "./modules/Patient/Transcription";
import HealthLogs from "./modules/Patient/HealthLogs";
import Profile from "./modules/Patient/Profile";
import Settings from "./modules/Patient/Settings";
import ProtectedRoute from "./modules/auth/ProtectedRoute";
import FindDoctor from "./modules/Patient/Appointments/FindDoctor";
import DoctorProfile from "./modules/Patient/Appointments/DoctorProfile";

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/auth" element={<AuthPage />} />

        {/* Protected Routes for Patients */}
        <Route
          path="/patient/dashboard/*"
          element={
            <ProtectedRoute allowedRoles={["patient"]}>
              <PatientDashboard />
            </ProtectedRoute>
          }
        >
          <Route index element={<DashboardHome />} />
          <Route path="appointments" element={<Appointments />} />
          <Route path="appointments/book" element={<FindDoctor />} /> {/* Route for booking doctors */}
          <Route path="ehr" element={<EHR />} />
          <Route path="prescriptions" element={<Prescriptions />} />
          <Route path="lab-results" element={<LabResults />} />
          <Route path="allergies" element={<Allergies />} />
          <Route path="reminders" element={<Reminders />} />
          <Route path="transcription" element={<Transcription />} />
          <Route path="health-logs" element={<HealthLogs />} />
          <Route path="profile" element={<Profile />} />
          <Route path="settings" element={<Settings />} />
          <Route path="appointments/doctor/:doctorId" element={<DoctorProfile />} />
          <Route path="*" element={<Navigate to="" />} />
        </Route>

        {/* Catch-All Route */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;