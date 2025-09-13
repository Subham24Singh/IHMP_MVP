const API_BASE = "http://localhost:8000";
export const getAppointments = async (token) => {
  try {
    console.log("Fetching appointments from:", `${API_BASE}/patient/appointments/`);
    const res = await fetch(`${API_BASE}/patient/appointments/`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    if (!res.ok) {
      throw new Error(`Failed to fetch appointments: ${res.statusText}`);
    }
    return res.json();
  } catch (error) {
    console.error("Error fetching appointments:", error);
    throw error;
  }
};

export const getDoctors = async (token) => {
  const res = await fetch(`${API_BASE}/api/doctors/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch doctors");
  return res.json();
};

export const createAppointment = async (token, appointmentData) => {
  const res = await fetch(`${API_BASE}/patient/appointments/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(appointmentData),
  });
  if (!res.ok) throw new Error("Failed to create appointment");
  return res.json();
};

export const cancelAppointment = async (token, appointmentId) => {
  const res = await fetch(`${API_BASE}/patient/appointments/${appointmentId}/`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
  if (!res.ok) throw new Error("Failed to cancel appointment");
  return true;
};

export const rescheduleAppointment = async (token, appointmentId, newDate) => {
  const res = await fetch(`${API_BASE}/patient/appointments/${appointmentId}/`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ appointment_date: newDate }),
  });
  if (!res.ok) throw new Error("Failed to reschedule appointment");
  return res.json();
};