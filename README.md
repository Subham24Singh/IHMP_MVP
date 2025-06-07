# IHMP - Integrated Healthcare Management Platform

A modular, scalable, and secure healthcare management system built with **FastAPI** and **PostgreSQL**.  
This project is designed for startups and teams building real-world healthcare solutions, supporting features like EHR, AI transcriptions, appointments, lab results, prescriptions, and more, with strict role-based access for patients, doctors, and admins.

---

## 🚀 Features

- 👨‍⚕️ User Authentication & Role-Based Access (Patient, Doctor, Admin)
- 📝 Electronic Health Record (EHR) & EHR Summary
- 💊 Prescription Management
- 🧪 Lab Results Management
- 💉 Allergy Tracking
- 📅 Appointments & Follow-Ups
- 🔔 Reminders
- 🎙️ AI-Based Doctor Transcription Module
- 🩺 Health Monitoring Logs
- 🗂️ Modular, role-based API structure
- 🛡️ Secure JWT Authentication

---

## 🛠️ Prerequisites

- **Python 3.10+** (recommended)
- **PostgreSQL** (for main database)
- **Git** (for version control)
- **Node.js & npm** (if using the recommended React frontend)
- **Alembic** (for database migrations)

---

## 📦 Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/piyushGit1229/IHMP_MVP.git
cd IHMP_MVP
```

---

### 2. Set Up Environment Variables

Create a `.env` file in the project root (see `.env.example` for reference):

```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<db>
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 3. Install Python Dependencies

```sh
pip install -r requirements.txt
```

---

### 4. Set Up the Database

- Ensure PostgreSQL is running and your database is created.
- Update `DATABASE_URL` in your `.env` file accordingly.

---

### 5. Run Alembic Migrations

```sh
alembic upgrade head
```

This will create all tables as per the latest models.

---

### 6. Start the FastAPI Backend

```sh
uvicorn app.main:app --reload
```

- The API will be available at `http://127.0.0.1:8000/`
- Interactive docs: `http://127.0.0.1:8000/docs`

---

### 7. (Optional) Set Up the Frontend

If you are using the recommended React frontend:

```sh
cd frontend
npm install
npm start
```

- The frontend will run on `http://localhost:3000/` by default.

---

## 🧩 Project Structure

```
IHMP_MVP/
│
├── app/
│   ├── modules/
│   │   ├── patient/
│   │   ├── doctor/
│   │   ├── admin/
│   │   ├── appointment/
│   │   ├── ehr/
│   │   ├── prescription/
│   │   ├── ...
│   ├── database/
│   ├── main.py
│   └── ...
├── alembic/
├── frontend/           # (if using React)
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md
```

---

## ⚠️ Important Notes

- **Environment Variables:** Always keep your `.env` file secret and never commit it.
- **Database Management:** Use Alembic for all schema changes.
- **Testing:** Add/extend tests as needed for your modules.
- **CORS:** Backend is configured for local frontend development.

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

---

**Built for modern healthcare startups. Modular. Secure. Scalable.**