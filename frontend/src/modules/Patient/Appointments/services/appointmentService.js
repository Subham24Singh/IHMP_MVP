import axios from 'axios';
import { API_BASE_URL } from '../../../../config';

export const appointmentService = {
  bookAppointment: async (appointmentData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:8000/patient/appointments/',
        {
          doctor_id: appointmentData.doctor_id,
          appointment_date: appointmentData.appointment_date
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to book appointment' };
    }
  },

  getMyAppointments: async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(
        'http://localhost:8000/patient/appointments/',
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch appointments' };
    }
  }
};
