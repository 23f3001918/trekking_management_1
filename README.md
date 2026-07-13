# Trekking Management System

A web-based Trekking Management System developed using **Flask**, **SQLite**, **SQLAlchemy**, **Jinja2**, **HTML**, and **CSS**. The application provides role-based access for **Admin**, **Trek Staff**, and **Users (Trekkers)** to efficiently manage trekking activities, bookings, and participant information.


## 📌 Features

### Authentication
- Secure login system
- User registration
- Trek Staff registration
- Role-based access (Admin, Staff, User)

### Admin
- Dashboard with application statistics
- Add, edit, and delete treks
- Add and manage trek staff
- Assign staff to treks
- View and manage users
- Blacklist/Activate users and staff
- View all bookings
- Search users, staff, and treks

### Trek Staff
- View assigned treks
- Update trek status
- Update available slots
- View registered participants
- Manage trek progress

### User (Trekker)
- Register and login
- Browse available treks
- Search and filter treks
- Book treks
- Cancel bookings
- View booking status
- View trekking history
- Update profile

### Booking System
- Prevent duplicate bookings
- Prevent overbooking
- Allow booking only for open treks
- Automatic slot management
- Booking history tracking


## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Flask | Backend Web Framework |
| SQLAlchemy | ORM for database operations |
| SQLite | Database |
| Jinja2 | HTML Template Engine |
| HTML | Structure of web pages |
| CSS | Styling and UI |
| Flask Sessions | Authentication and Role Management |


## 📂 Project Structure

trekking_management/
│
├── app.py
├── models/
│   └── models.py
├── controllers/
│   ├── auth_controller.py
│   ├── admin_controller.py
│   ├── staff_controller.py
│   └── user_controller.py
├── templates/
│   ├── admin/
│   ├── staff/
│   ├── user/
│   └── base.html
├── static/
│   └── css/
├── utils/
│   └── decorators.py
└── requirements.txt
```

---

## 🗄️ Database Tables

- Users
- Staff Profiles
- Treks
- Bookings

---

## 🚀 Installation

### Clone the repository

```bash
git clone <repository-url>
cd trekking_management
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 👤 Default Admin Credentials

```
Email: admin@gmail.com
Password: admin123
```



## 📖 Functionalities

- Role-based authentication
- Trek management
- Staff management
- User management
- Trek booking
- Booking cancellation
- Participant management
- Trek status updates
- Booking validation
- Trek history

## 🔒 Validations

- Duplicate trek booking prevention
- Overbooking prevention
- Only assigned staff can manage treks
- Only open treks can be booked
- Role-based dashboard access

Demo Video Link: https://drive.google.com/file/d/1Ma_KZd0nMAmATIR5A7O3OjKl_Z95Tlsp/view?usp=drive_link

Report Link:https://drive.google.com/file/d/1k1FDNAXCoHhHjdZx7xt3aIB1skE_pKsB/view?usp=drive_link
