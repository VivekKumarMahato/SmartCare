# SmartCare - Blood Bank Management System

## Overview

SmartCare is a backend system built using FastAPI to manage blood donors, requests, and user authentication. It follows a clean layered architecture for scalability and maintainability.

## Features

* User registration & JWT authentication
* Donor management
* Blood request handling
* RESTful APIs

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic

## Architecture

Layered architecture:
API → Service → Repository → Database

## Setup Instructions

```bash
git clone https://github.com/VivekKumarMahato/SmartCare.git
cd SmartCare
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Docs

After running the server:
http://127.0.0.1:8000/docs

## Future Improvements

* Role-based access control
* Docker support
* AI-based features
