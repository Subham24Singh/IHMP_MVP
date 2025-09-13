import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAppointments, cancelAppointment, rescheduleAppointment } from "../../../api/api";
import styles from "./Appointments.module.css";

function StatusChip({ type }) {
  let label = "";
  let className = styles.statusChip;
  if (type === "inPerson") {
    label = "In-Person";
    className += ` ${styles.inPerson}`;
  } else if (type === "virtual") {
    label = "Virtual";
    className += ` ${styles.virtual}`;
  } else if (type === "completed") {
    label = "Completed";
    className += ` ${styles.completed}`;
  }
  return <span className={className}>{label}</span>;
}

export default function Appointments() {
  const [appointments, setAppointments] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found. Redirecting to login.");
      navigate("/auth");
      return;
    }

    getAppointments(token)
      .then((data) => {
        console.log("Fetched appointments:", data); // Debugging log
        setAppointments(data);
      })
      .catch((err) => console.error("Failed to fetch appointments:", err));
  }, [navigate]);

  const now = new Date();
  const upcoming = appointments.filter(
    (appt) => new Date(appt.appointment_date) > now
  );
  const past = appointments.filter(
    (appt) => new Date(appt.appointment_date) <= now
  );

  return (
    <div className={styles.container}>
      {/* Top Header Row */}
      <div className={styles.appointmentsHeader}>
        <div>
          <div className={styles.title}>Appointments</div>
          <div className={styles.subtitle}>Manage your upcoming and past appointments</div>
        </div>
        <div>
          <button className={styles.findDoctorsBtn} onClick={() => navigate("/patient/dashboard/appointments/book")}>Find Doctors</button>
          <button className={styles.actionBtn} onClick={() => navigate("/patient/dashboard/appointments/book")}>+ Quick Book</button>
        </div>
      </div>
      {/* Upcoming Appointments */}
      <div className={styles.sectionCard}>
        <div className={styles.sectionTitle}>
          <svg width="28" height="28" fill="none" stroke="currentColor" strokeWidth="2.2" style={{color:'#2563eb'}}><rect x="3" y="5" width="16" height="14" rx="3"/><path d="M16 3v4M8 3v4M3 9h16"/></svg>
          Upcoming Appointments
        </div>
        <div className={styles.cardsList}>
          {upcoming.length === 0 ? (
            <div className={styles.noAppointments}>No upcoming appointments.</div>
          ) : (
            upcoming.map((appt, i) => (
              <div key={appt.id || appt.appointment_id} className={styles.appointmentCard} style={{animationDelay: `${0.09 * i + 0.18}s`}}>
                <div className={styles.avatar}>{appt.doctor_name?.[0] || 'D'}</div>
                <div className={styles.details}>
                  <div className={styles.doctorName}>Dr. {appt.doctor_name}</div>
                  <div className={styles.specialization}>{appt.specialization || 'Specialist'}</div>
                  <div className={styles.infoRow}>
                    <span><svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"><rect x="2" y="4" width="12" height="10" rx="2"/><path d="M10 2v2M6 2v2M2 7h12"/></svg> {new Date(appt.appointment_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })}</span>
                    <span><svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="8" cy="8" r="6"/><path d="M8 4v4l2 2"/></svg> {new Date(appt.appointment_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                    {appt.location ? (
                      <span><svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"><path d="M8 14s5-4.33 5-7.5A5 5 0 0 0 3 6.5C3 9.67 8 14 8 14Z"/><circle cx="8" cy="6.5" r="1.5"/></svg> {appt.location}</span>
                    ) : (
                      <span><svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="6" width="10" height="7" rx="2"/><path d="M8 6v7"/></svg> Virtual</span>
                    )}
                  </div>
                </div>
                <div style={{minWidth:120, display:'flex', flexDirection:'column', alignItems:'flex-end', gap:8}}>
                  <StatusChip type={appt.location ? 'inPerson' : 'virtual'} />
                  <div className={styles.actionGroup} style={{marginTop:6}}>
                    <button
  className={styles.actionBtnSecondary}
  disabled={appt._isRescheduling}
  onClick={() => {
    setAppointments((prev) => prev.map(a =>
      (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
        ? { ...a, _showRescheduleModal: true, _rescheduleDate: a.appointment_date }
        : a
    ));
  }}
>
  {appt._isRescheduling ? 'Rescheduling...' : 'Reschedule'}
</button>
{appt._showRescheduleModal && (
  <div className={styles.modalOverlay}>
    <div className={styles.modalCard} role="dialog" aria-modal="true" aria-labelledby="reschedule-title">
      <div className={styles.modalTitle} id="reschedule-title">Reschedule Appointment</div>
      <div className={styles.modalText} style={{marginBottom: '1.2rem'}}>Select a new date and time for your appointment with Dr. {appt.doctor_name}.</div>
      <input
        className={styles.dateTimeInput}
        type="datetime-local"
        value={
          appt._rescheduleDate
            ? new Date(appt._rescheduleDate).toISOString().slice(0,16)
            : ''
        }
        min={new Date().toISOString().slice(0,16)}
        onChange={e => {
          const val = e.target.value;
          setAppointments((prev) => prev.map(a =>
            (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
              ? { ...a, _rescheduleDate: val }
              : a
          ));
        }}
        style={{marginBottom:'1.5rem', width:'100%', fontSize:'1.06rem', padding:'0.45rem 1rem', borderRadius:'0.7rem', border:'1px solid #cbd5e1'}}
      />
      <div className={styles.modalActions}>
        <button
          className={styles.actionBtnSecondary}
          disabled={appt._isRescheduling}
          onClick={async () => {
            setAppointments((prev) => prev.map(a =>
              (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
                ? { ...a, _isRescheduling: true }
                : a
            ));
            try {
              const token = localStorage.getItem("token");
              // Convert to ISO string for backend
              const isoDate = new Date(appt._rescheduleDate).toISOString();
              await rescheduleAppointment(token, appt.id || appt.appointment_id, isoDate);
              // Optionally animate fade-out or just refresh
              const updated = await getAppointments(token);
              setAppointments(updated);
            } catch (err) {
              alert('Failed to reschedule appointment');
            } finally {
              setAppointments((prev) => prev.map(a =>
                (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
                  ? { ...a, _isRescheduling: false, _showRescheduleModal: false }
                  : a
              ));
            }
          }}
        >
          {appt._isRescheduling ? 'Rescheduling...' : 'Confirm'}
        </button>
        <button
          className={styles.actionBtnDanger}
          disabled={appt._isRescheduling}
          style={{marginLeft: 16}}
          onClick={() => {
            setAppointments((prev) => prev.map(a =>
              (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
                ? { ...a, _showRescheduleModal: false }
                : a
            ));
          }}
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
)}
                    <button
  className={styles.actionBtnDanger}
  disabled={appt._isCancelling}
  onClick={() => {
    setAppointments((prev) => prev.map(a =>
      (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
        ? { ...a, _showCancelModal: true }
        : a
    ));
  }}
>
  {appt._isCancelling ? 'Cancelling...' : 'Cancel'}
</button>
{appt._showCancelModal && (
  <div className={styles.modalOverlay}>
    <div className={styles.modalCard} role="dialog" aria-modal="true" aria-labelledby="cancel-title">
      <div className={styles.modalTitle} id="cancel-title">Cancel Appointment?</div>
      <div className={styles.modalText}>Are you sure you want to cancel your appointment with Dr. {appt.doctor_name}? This action cannot be undone.</div>
      <div className={styles.modalActions}>
        <button
          className={styles.actionBtnDanger}
          disabled={appt._isCancelling}
          onClick={async () => {
            setAppointments((prev) => prev.map(a =>
              (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
                ? { ...a, _isCancelling: true }
                : a
            ));
            try {
              const token = localStorage.getItem("token");
              await cancelAppointment(token, appt.id || appt.appointment_id);
              // Animate fade-out
              setAppointments((prev) => prev.map(a =>
                (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
                  ? { ...a, _isFading: true }
                  : a
              ));
              setTimeout(() => {
                setAppointments((prev) => prev.filter(a => (a.id || a.appointment_id) !== (appt.id || appt.appointment_id)));
              }, 400);
            } catch (err) {
              alert('Failed to cancel appointment');
              setAppointments((prev) => prev.map(a =>
                (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
                  ? { ...a, _isCancelling: false, _showCancelModal: false }
                  : a
              ));
            }
          }}
        >
          {appt._isCancelling ? 'Cancelling...' : 'Yes, Cancel'}
        </button>
        <button
          className={styles.actionBtnSecondary}
          disabled={appt._isCancelling}
          style={{marginLeft: 16}}
          onClick={() => {
            setAppointments((prev) => prev.map(a =>
              (a.id || a.appointment_id) === (appt.id || appt.appointment_id)
                ? { ...a, _showCancelModal: false }
                : a
            ));
          }}
        >
          No, Go Back
        </button>
      </div>
    </div>
  </div>
)}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
      {/* Past Appointments */}
      <div className={styles.sectionCard} style={{background:'linear-gradient(120deg,rgba(255,255,255,0.82) 80%,rgba(232,240,255,0.38) 100%)', boxShadow:'0 6px 32px 0 rgba(30,41,59,0.07)'}}>
        <div className={styles.sectionTitle} style={{color:'#64748b'}}>
          <svg width="28" height="28" fill="none" stroke="currentColor" strokeWidth="2.2" style={{color:'#a3a3a3'}}><circle cx="14" cy="14" r="11"/><path d="M14 9v6l3 3"/></svg>
          Past Appointments
        </div>
        <div className={styles.cardsList}>
          {past.length === 0 ? (
            <div className={styles.noAppointments}>No past appointments.</div>
          ) : (
            past.map((appt, i) => (
              <div key={appt.id || appt.appointment_id} className={styles.appointmentCard + ' ' + styles.pastCard} style={{animationDelay: `${0.09 * i + 0.18}s`, opacity:0.92}}>
                <div className={styles.avatar + ' ' + styles.avatarGray}>{appt.doctor_name?.[0] || 'D'}</div>
                <div className={styles.details}>
                  <div className={styles.doctorName}>Dr. {appt.doctor_name}</div>
                  <div className={styles.specialization}>{appt.specialization || 'Specialist'}</div>
                  <div className={styles.infoRow}>
                    <span><svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"><rect x="2" y="4" width="12" height="10" rx="2"/><path d="M10 2v2M6 2v2M2 7h12"/></svg> {new Date(appt.appointment_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })}</span>
                    <span><svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="8" cy="8" r="6"/><path d="M8 4v4l2 2"/></svg> {new Date(appt.appointment_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                  </div>
                </div>
                <div style={{minWidth:120, display:'flex', flexDirection:'column', alignItems:'flex-end', gap:8}}>
                  <StatusChip type="completed" />
                  <div className={styles.actionGroup} style={{marginTop:6}}>
                    <button className={styles.actionBtnSecondary}>View Details</button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}