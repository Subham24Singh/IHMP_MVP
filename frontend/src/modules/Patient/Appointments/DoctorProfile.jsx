import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { 
  ArrowLeft, 
  Star, 
  MapPin, 
  Clock, 
  Calendar, 
  Phone, 
  Mail, 
  MessageSquare,
  Award,
  GraduationCap,
  Clock as ClockIcon,
  CheckCircle,
  ChevronRight,
  Heart,
  ChevronDown,
  ChevronUp,
  DollarSign,
  Shield,
  UserCheck,
  Briefcase,
  Map,
  Navigation,
  Globe
} from 'lucide-react';
import BookAppointmentModal from './BookAppointmentModal';
import DoctorAvailabilityCalendar from './DoctorAvailabilityCalendar';

function DoctorProfile() {
  const [bookingModalOpen, setBookingModalOpen] = useState(false);
  const { doctorId } = useParams();
  const [doctor, setDoctor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [expandedSections, setExpandedSections] = useState({
    about: true,
    experience: false,
    availability: false,
    reviews: false
  });
  const [availabilitySlots, setAvailabilitySlots] = useState([]);
  const [calendarOpen, setCalendarOpen] = useState(false);
  const navigate = useNavigate();

  // Verify user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/auth');
      return;
    }
  }, [navigate]);

  // Fetch doctor details
  useEffect(() => {
    const fetchDoctorProfile = async () => {
      if (!doctorId) return;
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:8000/api/doctors/${doctorId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) {
          if (response.status === 401) {
            navigate('/auth');
            return;
          }
          throw new Error('Failed to fetch doctor details');
        }
        const data = await response.json();
        setDoctor(data);
      } catch (err) {
        console.error('Error fetching doctor:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    const fetchAvailabilitySlots = async () => {
      if (!doctorId) return;
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:8000/api/doctors/${doctorId}/availability`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        if (response.ok) {
          const slots = await response.json();
          setAvailabilitySlots(expandSlots(slots, 30));
        } else {
          setAvailabilitySlots([]);
        }
      } catch (err) {
        setAvailabilitySlots([]);
      }
    };
    if (doctorId) {
      fetchDoctorProfile();
      fetchAvailabilitySlots();
    }
  }, [doctorId, navigate]);

  // Helper: split slots into intervals
  function timeToMinutes(t) {
    const [h, m] = t.split(':');
    return parseInt(h, 10) * 60 + parseInt(m, 10);
  }
  function minutesToTime(mins) {
    const h = Math.floor(mins / 60).toString().padStart(2, '0');
    const m = (mins % 60).toString().padStart(2, '0');
    return `${h}:${m}:00`;
  }
  function expandSlots(rawSlots, intervalMins = 30) {
    let expanded = [];
    for (const slot of rawSlots) {
      if (slot.status !== 'available') continue;
      const startMins = timeToMinutes(slot.start_time);
      const endMins = timeToMinutes(slot.end_time);
      let t = startMins;
      while (t < endMins) {
        const nextT = Math.min(t + intervalMins, endMins);
        if (nextT - t >= 10) {
          expanded.push({
            ...slot,
            start_time: minutesToTime(t),
            end_time: minutesToTime(nextT),
            orig_slot_id: slot.slot_id,
            slot_id: `${slot.slot_id}_${t}`
          });
        }
        t = nextT;
      }
    }
    return expanded;
  }

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Use only API data for doctor profile fields.
  // Show slots for the next available date
  const today = new Date().toISOString().slice(0, 10);
  const futureSlots = availabilitySlots.filter(slot => slot.slot_date >= today);
  const groupedByDate = {};
  for (const slot of futureSlots) {
    if (!groupedByDate[slot.slot_date]) groupedByDate[slot.slot_date] = [];
    groupedByDate[slot.slot_date].push(slot);
  }
  const nextDate = Object.keys(groupedByDate).sort()[0];
  const slotsToShow = nextDate ? groupedByDate[nextDate] : [];

  const doctorFirstName = doctor?.full_name ? doctor.full_name.split(' ')[0] : 'Doctor';

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading doctor's profile...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-sm p-6 text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
            <Shield className="h-6 w-6 text-red-600" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Error loading profile</h3>
          <p className="text-gray-500 mb-6">{error}</p>
          <div className="flex space-x-3 justify-center">
            <button
              onClick={() => navigate(-1)}
              className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Go Back
            </button>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!doctor) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-sm p-6 text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
            <UserCheck className="h-6 w-6 text-blue-600" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Doctor Not Found</h3>
          <p className="text-gray-500 mb-6">The requested doctor profile could not be found.</p>
          <button
            onClick={() => navigate(-1)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-blue-600 hover:bg-blue-700"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to doctors
          </button>
        </div>
      </div>
    );
  }


  return (
    <div className="min-h-screen bg-gray-50">
      {calendarOpen && (
        <DoctorAvailabilityCalendar slots={availabilitySlots} onClose={() => setCalendarOpen(false)} />
      )}
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center py-4">
            <button
              onClick={() => navigate(-1)}
              className="p-2 rounded-full hover:bg-gray-100 mr-4"
            >
              <ArrowLeft className="h-5 w-5 text-gray-600" />
            </button>
            <h1 className="text-xl font-bold text-gray-900">Doctor Profile</h1>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left Sidebar */}
          <div className="lg:w-1/3">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
              <div className="p-6">
                <div className="flex flex-col items-center text-center">
                  <div className="relative mb-4">
                    <img
                      src={doctor.photo_url || 'https://randomuser.me/api/portraits/doctors/men/1.jpg'}
                      alt={doctor.full_name}
                      className="w-40 h-40 rounded-2xl object-cover border-4 border-white shadow-lg"
                    />
                    <div className="absolute -bottom-2 -right-2 bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded-full flex items-center">
                      <Star className="h-3 w-3 fill-current text-yellow-400 mr-1" />
                      {doctor.average_rating?.toFixed(1) || '4.8'}
                    </div>
                  </div>
                  
                  <h2 className="text-2xl font-bold text-gray-900">{doctor.full_name}</h2>
                  <p className="text-blue-600 font-medium mt-1">{doctor.specialty}</p>
                  <p className="text-gray-500 text-sm mt-1">{doctor.experience || '10+'} years of experience</p>
                  
                  <div className="mt-4 flex items-center space-x-2">
                    <div className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                      Available Today
                    </div>
                    <div className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                      Video Consult
                    </div>
                  </div>
                </div>

                <div className="mt-6 space-y-4">
                  <button
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-xl flex items-center justify-center transition-colors"
                    onClick={() => setBookingModalOpen(true)}
                  >
                    <Calendar className="h-5 w-5 mr-2" />
                    Book Appointment
                  </button>
                  <button className="w-full border border-blue-600 text-blue-600 hover:bg-blue-50 font-medium py-3 px-4 rounded-xl flex items-center justify-center transition-colors">
                    <MessageSquare className="h-5 w-5 mr-2" />
                    Send Message
                  </button>
                </div>

                <div className="mt-6 pt-6 border-t border-gray-100">
                  <h3 className="text-sm font-medium text-gray-900 mb-3">Contact Information</h3>
                  <div className="space-y-3">
                    <div className="flex items-start">
                      <MapPin className="h-5 w-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
                      <div>
                        <p className="text-sm text-gray-600">{doctor.clinic_address || '123 Medical Center, Suite 100'}</p>
                        <button className="mt-1 text-sm text-blue-600 hover:text-blue-800 flex items-center">
                          <span>View on map</span>
                          <ChevronRight className="h-4 w-4 ml-1" />
                        </button>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <Phone className="h-5 w-5 text-blue-600 mr-3" />
                      {doctor.phone ? (
                        <a href={`tel:${doctor.phone}`} className="text-gray-600 hover:text-blue-600">
                          {doctor.phone}
                        </a>
                      ) : (
                        <span className="text-gray-500">N/A</span>
                      )}
                    </div>
                    <div className="flex items-center">
                      <Mail className="h-5 w-5 text-blue-600 mr-3" />
                      {doctor.email ? (
                        <a href={`mailto:${doctor.email}`} className="text-gray-600 hover:text-blue-600">
                          {doctor.email}
                        </a>
                      ) : (
                        <span className="text-gray-500">N/A</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-sm font-medium text-gray-900 mb-4">Languages Spoken</h3>
              <div className="flex flex-wrap gap-2">
                {Array.isArray(doctor.languages_spoken) && doctor.languages_spoken.length > 0 ? (
                  doctor.languages_spoken.map((language, index) => (
                    <span key={index} className="bg-gray-100 text-gray-800 text-xs font-medium px-3 py-1.5 rounded-full">
                      {language}
                    </span>
                  ))
                ) : (
                  <span className="text-gray-500">N/A</span>
                )}
              </div>
            </div>
          </div>

          {/* Right Content */}
          <div className="lg:w-2/3">
            {/* Tabs */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-6">
              <div className="border-b border-gray-200">
                <nav className="flex -mb-px">
                  <button
                    onClick={() => setActiveTab('overview')}
                    className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                      activeTab === 'overview'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Overview
                  </button>
                  <button
                    onClick={() => setActiveTab('reviews')}
                    className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                      activeTab === 'reviews'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Reviews ({doctor.total_ratings || 0})
                  </button>
                  <button
                    onClick={() => setActiveTab('locations')}
                    className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                      activeTab === 'locations'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Locations
                  </button>
                </nav>
              </div>

              {/* Tab Content */}
              <div className="p-6">
                {activeTab === 'overview' && (
                  <div className="space-y-6">
                     {/* About Section */}
                    <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
                      <button
                        onClick={() => toggleSection('about')}
                        className="w-full px-6 py-4 flex justify-between items-center text-left"
                      >
                        <div className="flex items-center">
                          <UserCheck className="h-5 w-5 text-blue-600 mr-3" />
                          <h3 className="text-lg font-medium text-gray-900">About Dr. {doctor.full_name.split(' ')[0]}</h3>
                        </div>
                        {expandedSections.about ? (
                          <ChevronUp className="h-5 w-5 text-gray-400" />
                        ) : (
                          <ChevronDown className="h-5 w-5 text-gray-400" />
                        )}
                      </button>
                      {expandedSections.about && (
                        <div className="px-6 pb-6 pt-2 border-t border-gray-100">
                          <p className="text-gray-600 leading-relaxed">
                            {doctor.bio || `Dr. ${doctor.full_name} is a highly experienced ${doctor.specialty} with ${doctor.Experience || '10+'} years of experience in providing exceptional patient care. Specializing in preventive medicine and personalized treatment plans, Dr. ${doctor.full_name.split(' ')[0]} is committed to delivering the highest standard of healthcare.`}
                          </p>
                        </div>
                      )}
                    </div>

                    {/* --- Availability Section --- */}
                    <div className="bg-white rounded-xl border border-green-100 overflow-hidden">
                      <button
                        onClick={() => toggleSection('availability')}
                        className="w-full px-6 py-4 flex justify-between items-center text-left"
                      >
                        <div className="flex items-center">
                          <ClockIcon className="h-5 w-5 text-green-600 mr-3" />
                          <h3 className="text-lg font-medium text-gray-900">Available Time Slots</h3>
                        </div>
                        {expandedSections.availability ? (
                          <ChevronUp className="h-5 w-5 text-gray-400" />
                        ) : (
                          <ChevronDown className="h-5 w-5 text-gray-400" />
                        )}
                      </button>
                      {expandedSections.availability && (
                        <div className="px-6 pb-6 pt-2 border-t border-gray-100">
                          {slotsToShow && slotsToShow.length > 0 ? (
                            <div>
                              <div className="text-sm text-gray-600 mb-2">
                                <span className="font-semibold">Next Available Date:</span> {nextDate}
                              </div>
                              <ul className="space-y-2">
                                {slotsToShow.map(slot => (
                                  <li key={slot.slot_id} className="flex items-center gap-3 text-sm text-gray-700">
                                    <span className={`inline-block w-2 h-2 rounded-full ${slot.status === 'available' ? 'bg-green-400' : 'bg-gray-400'}`}></span>
                                    <span>{slot.start_time.slice(0,5)} - {slot.end_time.slice(0,5)}</span>
                                  </li>
                                ))}
                              </ul>
                              {availabilitySlots.length > 5 && (
                                <button
                                  className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                                  onClick={() => setCalendarOpen(true)}
                                >
                                  View Full Calendar
                                </button>
                              )}
                            </div>
                          ) : (
                            <div className="text-gray-500">No available slots found.</div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Experience & Education */}
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  {/* Experience */}
  <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
    <button
      onClick={() => toggleSection('experience')}
      className="w-full px-6 py-4 flex justify-between items-center text-left"
    >
      <div className="flex items-center">
        <Briefcase className="h-5 w-5 text-blue-600 mr-3" />
        <h3 className="text-lg font-medium text-gray-900">Experience</h3>
      </div>
      {expandedSections.experience ? (
        <ChevronUp className="h-5 w-5 text-gray-400" />
      ) : (
        <ChevronDown className="h-5 w-5 text-gray-400" />
      )}
    </button>
    {expandedSections.experience && (
      <div className="px-6 pb-6 pt-2 border-t border-gray-100">
        <div className="space-y-4">
          {Array.isArray(doctor.experience) && doctor.experience.length > 0 ? (
            doctor.experience.map((exp, index) => (
              <div key={index} className="relative pl-6 pb-6 border-l-2 border-blue-100 last:border-transparent last:pb-0">
                <div className="absolute -left-2.5 top-0 h-5 w-5 rounded-full bg-blue-500 flex items-center justify-center">
                  <div className="h-2 w-2 rounded-full bg-white"></div>
                </div>
                <p className="font-medium text-gray-900">{exp.position || exp.title || exp || 'N/A'}</p>
                <p className="text-blue-600 text-sm">{exp.hospital || exp.organization || ''}</p>
                <p className="text-gray-500 text-sm">{exp.duration || ''}</p>
              </div>
            ))
          ) : (typeof doctor.experience === 'string' && doctor.experience.trim() !== '' ? (
            <div className="relative pl-6 pb-6 border-l-2 border-blue-100 last:border-transparent last:pb-0">
              <div className="absolute -left-2.5 top-0 h-5 w-5 rounded-full bg-blue-500 flex items-center justify-center">
                <div className="h-2 w-2 rounded-full bg-white"></div>
              </div>
              <p className="font-medium text-gray-900">{doctor.experience}</p>
            </div>
          ) : (
            <p className="text-gray-500">N/A</p>
          ))}
        </div>
      </div>
    )}
  </div>

  {/* Education */}
  <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
    <div className="px-6 py-4">
      <div className="flex items-center">
        <GraduationCap className="h-5 w-5 text-blue-600 mr-3" />
        <h3 className="text-lg font-medium text-gray-900">Education</h3>
      </div>
      <div className="mt-4 space-y-4">
        {Array.isArray(doctor.education) && doctor.education.length > 0 ? (
          doctor.education.map((edu, index) => (
            <div key={index} className="pl-8 relative">
              <div className="absolute left-0 top-1 h-3 w-3 rounded-full bg-blue-200"></div>
              <p className="font-medium text-gray-900">{edu.degree || edu || 'N/A'}</p>
              <p className="text-gray-600 text-sm">{edu.institution || ''}</p>
              <p className="text-gray-500 text-xs">{edu.year || ''}</p>
            </div>
          ))
        ) : (typeof doctor.education === 'string' && doctor.education.trim() !== '' ? (
          <div className="pl-8 relative">
            <div className="absolute left-0 top-1 h-3 w-3 rounded-full bg-blue-200"></div>
            <p className="font-medium text-gray-900">{doctor.education}</p>
          </div>
        ) : (
          <p className="text-gray-500">N/A</p>
        ))}
      </div>
    </div>
  </div>
</div>

{/* Certifications */}
<div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
  <div className="px-6 py-4">
    <div className="flex items-center">
      <Award className="h-5 w-5 text-blue-600 mr-3" />
      <h3 className="text-lg font-medium text-gray-900">Certifications</h3>
    </div>
    <div className="mt-4 space-y-2">
      {Array.isArray(doctor.certifications) && doctor.certifications.length > 0 ? (
        doctor.certifications.map((cert, index) => (
          <div key={index} className="flex items-start">
            <Award className="h-5 w-5 text-blue-600 mr-2 mt-1" />
            <span className="text-gray-900">{cert}</span>
          </div>
        ))
      ) : (typeof doctor.certifications === 'string' && doctor.certifications.trim() !== '' ? (
        <div className="flex items-start">
          <Award className="h-5 w-5 text-blue-600 mr-2 mt-1" />
          <span className="text-gray-900">{doctor.certifications}</span>
        </div>
      ) : (
        <p className="text-gray-500">N/A</p>
      ))}
    </div>
  </div>
</div>

{/* Languages Spoken */}
<div className="mt-6 bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
  <h3 className="text-sm font-medium text-gray-900 mb-4">Languages Spoken</h3>
  <div className="flex flex-wrap gap-2">
    {Array.isArray(doctor.languages_spoken) && doctor.languages_spoken.length > 0 ? (
      doctor.languages_spoken.map((language, index) => (
        <span key={index} className="bg-gray-100 text-gray-800 text-xs font-medium px-3 py-1.5 rounded-full">
          {language}
        </span>
      ))
    ) : (
      <span className="text-gray-500">N/A</span>
    )}
  </div>
</div>

                    {/* Availability */}
                    <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
                      <button
                        onClick={() => toggleSection('availability')}
                        className="w-full px-6 py-4 flex justify-between items-center text-left"
                      >
                        <div className="flex items-center">
                          <Clock className="h-5 w-5 text-blue-600 mr-3" />
                          <h3 className="text-lg font-medium text-gray-900">Availability</h3>
                        </div>
                        {expandedSections.availability ? (
                          <ChevronUp className="h-5 w-5 text-gray-400" />
                        ) : (
                          <ChevronDown className="h-5 w-5 text-gray-400" />
                        )}
                      </button>
                      {expandedSections.availability && (
                        <div className="px-6 pb-6 pt-2 border-t border-gray-100">
                          <div className="space-y-6">
                            <div>
                              <h4 className="font-medium text-gray-900 mb-3">Available Days</h4>
                              <div className="flex flex-wrap gap-2">
                                {availableDays.map((day, index) => (
                                  <span 
                                    key={index}
                                    className="px-3 py-1.5 bg-blue-50 text-blue-700 rounded-lg text-sm font-medium"
                                  >
                                    {day}
                                  </span>
                                ))}
                              </div>
                            </div>
                            
                            <div>
                              <h4 className="font-medium text-gray-900 mb-3">Available Time Slots</h4>
                              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                                {availableTimeSlots.map((time, index) => (
                                  <button
                                    key={index}
                                    onClick={() => setSelectedSlot(time)}
                                    className={`px-3 py-2 rounded-lg border text-sm font-medium transition-colors ${
                                      selectedSlot === time
                                        ? 'bg-blue-600 text-white border-blue-600'
                                        : 'bg-white text-gray-700 border-gray-200 hover:border-blue-500 hover:text-blue-600'
                                    }`}
                                  >
                                    {time}
                                  </button>
                                ))}
                              </div>
                            </div>
                            
                            <div className="pt-2">
                              <button className="text-blue-600 text-sm font-medium flex items-center">
                                View full calendar
                                <ChevronRight className="h-4 w-4 ml-1" />
                              </button>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {activeTab === 'reviews' && (
                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-lg font-medium text-gray-900">Patient Reviews</h3>
                        <div className="flex items-center mt-1">
                          <div className="flex items-center">
                            <Star className="h-5 w-5 text-yellow-400 fill-yellow-400" />
                            <span className="ml-1 font-medium text-gray-900">
                              {doctor.average_rating?.toFixed(1) || '4.8'}
                            </span>
                            <span className="mx-1 text-gray-500">•</span>
                            <span className="text-gray-500">{doctor.total_ratings || 24} reviews</span>
                          </div>
                        </div>
                      </div>
                      <button className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700">
                        Write a Review
                      </button>
                    </div>

                    <div className="space-y-6">
                      {reviews.map((review) => (
                        <div key={review.id} className="border-b border-gray-100 pb-6 last:border-0 last:pb-0">
                          <div className="flex items-start justify-between">
                            <div>
                              <h4 className="font-medium text-gray-900">{review.name}</h4>
                              <div className="flex items-center mt-1">
                                <div className="flex">
                                  {[...Array(5)].map((_, i) => (
                                    <Star
                                      key={i}
                                      className={`h-4 w-4 ${i < review.rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}`}
                                    />
                                  ))}
                                </div>
                                <span className="text-sm text-gray-500 ml-2">{review.date}</span>
                              </div>
                            </div>
                          </div>
                          <p className="mt-3 text-gray-600">{review.comment}</p>
                        </div>
                      ))}
                    </div>

                    <button className="w-full mt-6 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50">
                      Load More Reviews
                    </button>
                  </div>
                )}

                {activeTab === 'locations' && (
                  <div className="space-y-6">
                    <div className="bg-white rounded-xl border border-gray-100 p-6">
                      <div className="flex items-start">
                        <div className="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                          <MapPin className="h-5 w-5 text-blue-600" />
                        </div>
                        <div className="ml-4">
                          <h3 className="text-lg font-medium text-gray-900">Main Clinic</h3>
                          <p className="mt-1 text-gray-600">{doctor.clinic_address || '123 Medical Center, Suite 100'}</p>
                          <div className="mt-3 flex space-x-3">
                            <a 
                              href="https://maps.google.com" 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800"
                            >
                              <Map className="h-4 w-4 mr-1" />
                              View on Map
                            </a>
                            <a 
                              href="https://maps.google.com/directions" 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800"
                            >
                              <Navigation className="h-4 w-4 mr-1" />
                              Get Directions
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white rounded-xl border border-gray-100 p-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Contact Information</h3>
                      <div className="space-y-4">
                        <div className="flex items-start">
                          <div className="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                            <Phone className="h-5 w-5 text-blue-600" />
                          </div>
                          <div className="ml-4">
                            <p className="text-sm font-medium text-gray-900">Phone</p>
                            <a 
                              href={`tel:${doctor.phone || '+1234567890'}`} 
                              className="text-blue-600 hover:text-blue-800"
                            >
                              {doctor.phone || '+1 (234) 567-890'}
                            </a>
                          </div>
                        </div>

                        <div className="flex items-start">
                          <div className="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                            <Mail className="h-5 w-5 text-blue-600" />
                          </div>
                          <div className="ml-4">
                            <p className="text-sm font-medium text-gray-900">Email</p>
                            <a 
                              href={`mailto:${doctor.email || 'contact@example.com'}`} 
                              className="text-blue-600 hover:text-blue-800"
                            >
                              {doctor.email || 'contact@example.com'}
                            </a>
                          </div>
                        </div>

                        <div className="flex items-start">
                          <div className="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                            <Globe className="h-5 w-5 text-blue-600" />
                          </div>
                          <div className="ml-4">
                            <p className="text-sm font-medium text-gray-900">Website</p>
                            <a 
                              href="https://www.example.com" 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:text-blue-800"
                            >
                              www.example.com
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Fixed Bottom CTA for Mobile */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 shadow-lg">
        <div className="flex space-x-3">
          <BookAppointmentModal>
            <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-xl flex items-center justify-center">
              <Calendar className="h-5 w-5 mr-2" />
              Book Appointment
            </button>
          </BookAppointmentModal>
          <button className="w-12 h-12 flex items-center justify-center border border-gray-300 rounded-xl text-gray-600 hover:bg-gray-50">
            <MessageSquare className="h-5 w-5" />
          </button>
        </div>
      </div>
      <BookAppointmentModal
        open={bookingModalOpen}
        onClose={() => setBookingModalOpen(false)}
        doctor={doctor}
      />
    </div>
  );
}

export default DoctorProfile;