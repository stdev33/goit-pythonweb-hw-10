# goit-pythonweb-hw-10

Homework 10. Fullstack Web Development with Python at GoIT Neoversity

# Contacts API

This is a RESTful API for managing contacts using FastAPI and PostgreSQL. The API allows users to create, read, update, delete, and search for contacts. It also includes a feature to retrieve contacts with upcoming birthdays within the next 7 days.

## Features
- CRUD operations for contacts
- Search functionality for contacts by name, surname, or email
- Endpoint for retrieving contacts with upcoming birthdays
- Fully documented API using Swagger (available at `/docs`)

## Prerequisites
Before running the application, ensure you have:
- **Docker** installed
- **Docker Compose** installed (optional but recommended)

## Setup Instructions

### Step 1: Create Docker Network
To ensure that the containers communicate properly, create a dedicated Docker network:
```bash
docker network create goit-pythonweb-hw-10-network
```

### Step 2: Start the PostgreSQL Container
Run the following command to start the PostgreSQL database:
```bash
docker run --name goit-pythonweb-hw-10-postgres \
  --network goit-pythonweb-hw-10-network \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=qumtum-dizsof-1tyRmu \
  -e POSTGRES_DB=contacts_db \
  -d postgres
```

### Step 3: Build the API Docker Image
Run the following command to build the API image:
```bash
docker build -t contacts_api .
```

### Step 4: Run the API Container
Run the following command to start the API container:
```bash
docker run --name contacts_api \
  --network goit-pythonweb-hw-10-network \
  -p 8000:8000 \
  --env-file .env \
  contacts_api
```

### Step 5: Access the API Documentation
Once the API container is running, you can access the Swagger documentation at:
- [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

### 1. Create Contact
**POST** `/contacts/`
- **Request Body:**
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "123456789",
    "birthday": "1990-01-01",
    "additional_info": "Friend from work"
  }
  ```

### 2. Get All Contacts
**GET** `/contacts/`

### 3. Get Contact by ID
**GET** `/contacts/{contact_id}`

### 4. Update Contact
**PUT** `/contacts/{contact_id}`
- **Request Body:** Partial or full update for contact fields.

### 5. Delete Contact
**DELETE** `/contacts/{contact_id}`

### 6. Search Contacts
**GET** `/contacts/search?query=<value>`
- Search by first name, last name, or email.

### 7. Get Upcoming Birthdays
**GET** `/contacts/upcoming-birthdays`
- Retrieves contacts with birthdays in the next 7 days.

---

## Notes
- Ensure that `.env` file exist and is correctly configured with the following content:
```env
DATABASE_URL=postgresql://postgres:dbpassword@goit-pythonweb-hw-10-postgres:5432/contacts_db
```


---
