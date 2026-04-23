# SmartCare - Blood Donation Management System

## 🚀 Overview

SmartCare is a backend system built using FastAPI to manage blood donors, blood requests, and secure user authentication.
The system is designed with a scalable, layered architecture and focuses on real-world backend practices such as role-based access, request lifecycle management, and efficient data handling.

---

## ✨ Features

### 🔐 Authentication & Authorization

* User registration with secure password hashing
* JWT-based authentication
* Role-based access control (Patient / Donor / Admin)

### 🧑‍🤝‍🧑 Donor Management

* Donor profile creation
* Availability tracking
* Blood group & location-based matching

### 🩸 Blood Request System

* Create blood requests
* Request lifecycle management:

  * `pending → accepted → completed`
* Donor assignment to requests
* Business rule validations (blood group & location match)

### 🔍 Smart Matching Logic

* Filters donors based on:

  * Blood group
  * Location
  * Availability

### 📊 User-Specific APIs

* “My Requests” API for patients
* Donor-specific request dashboard

### ⚙️ Advanced Backend Features

* State transition validation
* Role-based permissions enforcement
* Clean API structure

### 🆕 Currently Working On

* Pagination for large datasets
* Filtering APIs (e.g., status-based filtering)
* Performance optimization for queries

---

## 🛠 Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication

---

## 🏗 Architecture

The project follows a **layered architecture**:

```text
API Layer → Service Layer → Repository Layer → Database
```

* **API Layer**: Handles HTTP requests & responses
* **Service Layer**: Business logic (matching, validation, workflows)
* **Repository Layer**: Database interactions
* **Database**: PostgreSQL

---

## ⚡ Setup Instructions

```bash
git clone https://github.com/VivekKumarMahato/SmartCare.git
cd SmartCare
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 📄 API Documentation

After running the server:

👉 http://127.0.0.1:8000/docs

---

## 🧪 Core API Flow

```text
User → Register/Login → Get JWT Token
↓
Patient → Create Blood Request
↓
Donor → View Matching Requests → Accept
↓
Admin → Complete Request
↓
System → Updates donor availability
```

---

## 🚧 Future Improvements

* Docker containerization
* Advanced search & sorting
* Blood compatibility logic (universal donors/receivers)
* Notification system (email/SMS)
* AI-based features (prediction & optimization)

---

## 📌 Project Status

🟢 Actively in development
🔄 Currently enhancing APIs with **pagination and filtering for scalable data handling**

---

## 👨‍💻 Author

Vivek Kumar Mahato
