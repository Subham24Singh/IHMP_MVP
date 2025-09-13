import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, MenuItem, CircularProgress, Alert, Box, Typography, Chip, Stack, Tooltip } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { DatePicker, TimePicker } from '@mui/x-date-pickers';
import { Calendar, CheckCircle2, Info, Clock as ClockIcon } from 'lucide-react';
import { appointmentService } from './services/appointmentService';
import { addDays, setHours, setMinutes, isBefore, isAfter, format } from 'date-fns';

const durations = [15, 30, 45, 60];

const weekdaysMap = {
  Sunday: 0,
  Monday: 1,
  Tuesday: 2,
  Wednesday: 3,
  Thursday: 4,
  Friday: 5,
  Saturday: 6,
};
const weekdayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

const BookAppointmentModal = ({ open, onClose, doctor, onBooked }) => {
  const [selectedSlotId, setSelectedSlotId] = useState('');
  const [selectedDate, setSelectedDate] = useState('');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [internalError, setInternalError] = useState(null);
  const [slots, setSlots] = useState([]);

  // Fetch slots if not provided
  // Fetch all slots for the doctor (regardless of date)
  // Helper to split a time string (HH:MM:SS) into minutes
  function timeToMinutes(t) {
    const [h, m] = t.split(':');
    return parseInt(h, 10) * 60 + parseInt(m, 10);
  }

  // Helper to convert minutes to time string (HH:MM:SS)
  function minutesToTime(mins) {
    const h = Math.floor(mins / 60).toString().padStart(2, '0');
    const m = (mins % 60).toString().padStart(2, '0');
    return `${h}:${m}:00`;
  }

  // Split slots into 30-minute bookable intervals, but allow partials if < 30min
  function expandSlots(rawSlots, intervalMins = 30) {
    let expanded = [];
    for (const slot of rawSlots) {
      // Only split slots that are marked as available
      if (slot.status !== 'available') continue;
      const startMins = timeToMinutes(slot.start_time);
      const endMins = timeToMinutes(slot.end_time);
      let t = startMins;
      // Always divide the entire range into intervals
      while (t < endMins) {
        const nextT = Math.min(t + intervalMins, endMins);
        // Only add if slot is at least 10 minutes
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

  // Fetch and expand slots
  React.useEffect(() => {
    async function fetchSlots() {
      if (!doctor?.id) return;
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:8000/api/doctors/${doctor.id}/availability`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        if (response.ok) {
          const data = await response.json();
          setSlots(expandSlots(data, 30)); // 30-minute slots
        } else {
          setSlots([]);
        }
      } catch {
        setSlots([]);
      }
    }
    if (open) fetchSlots();
  }, [doctor, open]);



  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setInternalError(null);
    try {
      if (!doctor || !doctor.id) throw new Error('Doctor not found.');
      if (!selectedSlotId) throw new Error('Please select an available slot.');
      const slot = slots.find(s => s.slot_id === selectedSlotId);
      if (!slot) throw new Error('Selected slot is invalid.');
      // Compose appointment_date as ISO string (date + start_time)
      const appointmentDateTime = `${slot.slot_date}T${slot.start_time}`;
      await appointmentService.bookAppointment({
        doctor_id: doctor.id,
        appointment_date: new Date(appointmentDateTime).toISOString()
      });
      setSuccess(true);
      // Refetch slots after booking to update UI
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/doctors/${doctor.id}/availability`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setSlots(expandSlots(data, 30));
      }
      if (onBooked) onBooked();
      setTimeout(() => {
        setSuccess(false);
        onClose();
      }, 1500);
    } catch (err) {
      setError(err.message || 'Failed to book appointment');
    } finally {
      setLoading(false);
    }
  };

  // Helper: get all unique dates from slots
  const slotDates = Array.from(new Set(slots.map(slot => slot.slot_date)));

  // Helper: get available slots for selected date
  // Ensure selectedDate is always a string in YYYY-MM-DD
const slotsForSelectedDate = selectedDate
  ? slots.filter(slot => slot.slot_date === selectedDate)
  : []; // fallback

  // Disable dates in picker that have no available slots
  const isDateAvailable = (dateObj) => {
    // Accept both string and Date for comparison
    const ymd = dateObj instanceof Date
      ? dateObj.toISOString().slice(0, 10)
      : dateObj;
    return slots.some(slot => slot.slot_date === ymd);
  };



  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      maxWidth="xs" 
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 4,
          boxShadow: '0 4px 24px 0 rgba(30, 41, 59, 0.08)',
          background: '#fff',
          border: '1px solid #ececec',
          overflow: 'hidden',
        }
      }}
    >
      <DialogTitle sx={{ fontWeight: 700, textAlign: 'center', pb: 0, fontSize: 22, color: '#23272f', letterSpacing: 0.1 }}>
        Book Appointment
      </DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent sx={{ 
          background: '#fafbfc', 
          borderRadius: 2, 
          px: { xs: 2, sm: 4 },
          py: { xs: 2, sm: 3 },
          minHeight: 240,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}>
          {error && <Alert severity="error" sx={{ mb: 2, borderRadius: 2, background: '#fff', color: '#d32f2f', border: '1px solid #f3d6d6' }}>{error}</Alert>}
          {internalError && <Alert severity="warning" sx={{ mb: 2, borderRadius: 2, background: '#fff', color: '#b08900', border: '1px solid #f6e9c6' }}>{internalError}</Alert>}
          {success ? (
            <Box
              sx={{
                width: '100%',
                maxWidth: 420,
                mx: 'auto',
                bgcolor: '#fafbfc',
                borderRadius: 2,
                boxShadow: '0 1px 4px 0 rgba(30,41,59,0.04)',
                px: { xs: 1, sm: 3 },
                py: { xs: 2, sm: 3 },
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'stretch',
                gap: 2,
                border: '1px solid #ececec',
              }}
            >
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <CheckCircle2 size={22} color="#3cb371" style={{ marginRight: 4 }} />
                <Typography variant="subtitle2" sx={{ color: '#3cb371', fontWeight: 500, fontSize: 15 }}>
                  Your appointment is confirmed
                </Typography>
              </Box>
              <Typography variant="h5" sx={{ fontWeight: 700, color: '#23272f', mb: 0.5, letterSpacing: 0.04, fontSize: 20 }}>
                Appointment Booked!
              </Typography>
              <Typography variant="body2" sx={{ color: '#6b7280', mb: 2, fontWeight: 400, fontSize: 15 }}>
                You will receive a confirmation soon.
              </Typography>
              {/* Doctor and location info */}
              <Box display="flex" alignItems="center" gap={1} mb={1}>
                {/* Replace with doctor avatar if available */}
                <Box sx={{ width: 36, height: 36, borderRadius: '50%', background: '#f1f5f9', mr: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, color: '#475569', fontSize: 18 }}>
                  {doctor?.name ? doctor.name[0] : 'D'}
                </Box>
                <Typography variant="body2" sx={{ color: '#64748b' }}>
                  with <b>{doctor?.name || 'Doctor Name'}</b>
                </Typography>
              </Box>
              <Box mb={1}>
                <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#212b36' }}>
                  {doctor?.clinic || 'Clinic Name'}
                </Typography>
                <Typography variant="body2" sx={{ color: '#2563eb', textDecoration: 'underline', cursor: 'pointer', display: 'inline-block' }}>
                  {doctor?.clinic_address || 'Clinic Address'}
                </Typography>
              </Box>
              {/* Date & Time Card */}
              {/* You can add a summary of the booked slot here if desired */}
              <Button
                variant="outlined"
                color="primary"
                onClick={onClose}
                sx={{ mt: 1, px: 3, borderRadius: 2, fontWeight: 600, fontSize: 15, letterSpacing: 0.1, borderColor: '#2563eb', color: '#2563eb', '&:hover': { borderColor: '#1d4ed8', background: '#f1f5f9' } }}
                autoFocus
              >
                Done
              </Button>
            </Box>
          ) : (
            <Box>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DatePicker
                  label="Select Date"
                  value={selectedDate ? new Date(selectedDate) : null}
                  onChange={(newValue) => {
                    if (newValue instanceof Date && !isNaN(newValue)) {
                      setSelectedDate(newValue.toISOString().slice(0, 10));
                    } else {
                      setSelectedDate('');
                    }
                    setSelectedSlotId('');
                  }}
                  renderInput={(params) => <TextField {...params} />}
                  shouldDisableDate={date => !isDateAvailable(date)}
                />
              </LocalizationProvider>
              <TextField
                select
                label="Available Time Slots"
                value={selectedSlotId}
                onChange={e => setSelectedSlotId(e.target.value)}
                fullWidth
                required
                margin="normal"
                disabled={loading || slotsForSelectedDate.length === 0}
                helperText={slotsForSelectedDate.length === 0 ? 'No available slots found for this date.' : ''}
              >
                {slotsForSelectedDate.map(slot => (
                  <MenuItem key={slot.slot_id} value={slot.slot_id}>
                    {`${slot.start_time.slice(0,5)} - ${slot.end_time.slice(0,5)}`}
                  </MenuItem>
                ))}
              </TextField>
              <TextField
                label="Notes (optional)"
                value={notes}
                onChange={e => setNotes(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                minRows={2}
                sx={{ background: '#f1f5f9', borderRadius: 2 }}
              />
            </Box>
          )}
        </DialogContent>
        {!success && (
          <DialogActions sx={{ pb: 2 }}>
            <Button onClick={onClose} disabled={loading}>Cancel</Button>
            <Button type="submit" variant="contained" color="primary" disabled={loading} startIcon={<Calendar size={18} />}>
              {loading ? <CircularProgress size={20} /> : 'Book Appointment'}
            </Button>
          </DialogActions>
        )}
      </form>
    </Dialog>
  );
};

export default BookAppointmentModal;
