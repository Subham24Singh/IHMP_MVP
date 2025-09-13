import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

function DoctorProfile() {
  const { doctorId } = useParams();
  const [doctor, setDoctor] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/doctors/${doctorId}/profile`)
      .then((res) => res.json())
      .then(setDoctor);
  }, [doctorId]);

  if (!doctor) return <div>Loading...</div>;

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: 32 }}>
      <h2>Education and background</h2>
      <div>
        <strong>Specialties</strong>
        <div>{doctor.specialty}</div>
      </div>
      <div>
        <strong>Practice names</strong>
        <div>{doctor.full_name}</div>
      </div>
      <div>
        <strong>Hospital affiliations</strong>
        <div>{doctor.clinic_address}</div>
      </div>
      <div>
        <strong>Board certifications</strong>
        <div>{doctor.board_certifications || 'N/A'}</div>
      </div>
      <div>
        <strong>Education and training</strong>
        <ul>
          <li>{doctor.education}</li>
          <li>{doctor.experience}</li>
        </ul>
      </div>
      <div>
        <strong>Professional memberships</strong>
        <div>{doctor.professional_memberships || 'N/A'}</div>
      </div>
      <div>
        <strong>Languages</strong>
        <div>{doctor.languages || 'English'}</div>
      </div>
      <div>
        <strong>Provider's gender</strong>
        <div>{doctor.gender || 'N/A'}</div>
      </div>
      <div>
        <strong>NPI number</strong>
        <div>{doctor.npi_number || 'N/A'}</div>
      </div>
    </div>
  );
}

export default DoctorProfile;
