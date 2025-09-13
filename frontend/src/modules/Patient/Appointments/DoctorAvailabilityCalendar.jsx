import React from 'react';
import { Calendar as BigCalendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const localizer = momentLocalizer(moment);

// Convert API slots to calendar events
function slotsToEvents(slots) {
  return slots.map(slot => ({
    id: slot.slot_id,
    title: `${slot.status === 'available' ? 'Available' : 'Booked'}`,
    start: new Date(`${slot.slot_date}T${slot.start_time}`),
    end: new Date(`${slot.slot_date}T${slot.end_time}`),
    allDay: false,
    status: slot.status,
  }));
}

const DoctorAvailabilityCalendar = ({ slots, onClose }) => {
  const events = slotsToEvents(slots);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div className="bg-white rounded-xl shadow-lg w-full max-w-3xl p-6 relative">
        <button
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
          onClick={onClose}
        >
          ✕
        </button>
        <h2 className="text-xl font-semibold mb-4">Doctor's Full Calendar</h2>
        <div style={{ height: 500 }}>
          <BigCalendar
            localizer={localizer}
            events={events}
            startAccessor="start"
            endAccessor="end"
            views={['month', 'week', 'day']}
            defaultView="week"
            eventPropGetter={(event) => ({
              style: {
                backgroundColor: event.status === 'available' ? '#34d399' : '#f87171',
                color: '#111827',
                borderRadius: '6px',
                border: 'none',
                padding: '2px 8px',
              },
            })}
            titleAccessor="title"
          />
        </div>
      </div>
    </div>
  );
};

export default DoctorAvailabilityCalendar;
