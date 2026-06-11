# Travel Planner API

A RESTful API for managing travel projects and places to visit, built with Django REST Framework.

The application allows travelers to create projects, collect places from the Art Institute of Chicago API, attach personal notes, track visited locations, and automatically complete projects when all places have been visited.

---

## Features

### Travel Projects

* Create travel projects
* Update project information
* Delete projects
* List all projects
* Retrieve a single project

### Places Management

* Create a project with places in a single request
* Add places to existing projects
* Update notes for places
* Mark places as visited
* List all places in a project
* Retrieve a single place

### Business Rules

* Maximum 10 places per project
* Duplicate places are not allowed within the same project
* Places are validated through the Art Institute of Chicago API
* Projects containing visited places cannot be deleted
* Projects are automatically marked as completed when all places are visited

### Documentation

* Swagger / OpenAPI documentation included

---

## Tech Stack

* Python 3.12+
* Django
* Django REST Framework
* DRF Spectacular (Swagger/OpenAPI)
* SQLite
* Requests
* Art Institute of Chicago API

---

## Project Structure

```text
travel_planner/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── services/
│       └── artic_api.py
│
├── requirements.txt
├── manage.py
└── README.md
```

---

## Installation

### 1. Clone repository

```bash
git clone https://github.com/OWLsTyLe/TEST.git
cd TEST
```

### 2. Create virtual environment

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/api/
```

---

## API Documentation 


Swagger UI:

```text
http://127.0.0.1:8000/api/docs/
```

OpenAPI Schema:

```text
http://127.0.0.1:8000/api/schema/
```

---

## Endpoints

### Projects

| Method | Endpoint              | Description       |
| ------ | --------------------- | ----------------- |
| GET    | `/api/projects/`      | List all projects |
| POST   | `/api/projects/`      | Create project    |
| GET    | `/api/projects/{id}/` | Retrieve project  |
| PATCH  | `/api/projects/{id}/` | Update project    |
| DELETE | `/api/projects/{id}/` | Delete project    |

### Places

| Method | Endpoint                                | Description         |
| ------ | --------------------------------------- | ------------------- |
| GET    | `/api/projects/{id}/places/`            | List project places |
| POST   | `/api/projects/{id}/places/`            | Add place           |
| GET    | `/api/projects/{id}/places/{place_id}/` | Retrieve place      |
| PATCH  | `/api/projects/{id}/places/{place_id}/` | Update place        |

---

## Example Requests

### Create Project

```json
{
    "name": "Summer Trip",
    "description": "Chicago Art Tour",
    "start_date": "2026-07-01",
    "place_ids": [27992, 28560]
}
```

### Add Place

```json
{
    "external_id": 4473
}
```

### Update Place

```json
{
    "notes": "Must visit first",
    "is_visited": true
}
```

---

## Data Model

### Project

| Field        | Type    |
| ------------ | ------- |
| id           | Integer |
| name         | String  |
| description  | Text    |
| start_date   | Date    |
| is_completed | Boolean |

### Place

| Field       | Type       |
| ----------- | ---------- |
| id          | Integer    |
| project     | ForeignKey |
| external_id | Integer    |
| title       | String     |
| notes       | Text       |
| is_visited  | Boolean    |

---

## Third-Party Integration

The application validates places through the Art Institute of Chicago API before storing them in the database.

Example endpoint:

```http
GET https://api.artic.edu/api/v1/artworks/{id}
```

Validation ensures that only existing places can be added to a project.

---

## Validation Rules

| Rule                 | Description                                           |
| -------------------- | ----------------------------------------------------- |
| Maximum places       | 10 places per project                                 |
| Duplicate prevention | Same place cannot be added twice                      |
| Project deletion     | Forbidden if visited places exist                     |
| Auto completion      | Project becomes completed when all places are visited |
| External validation  | Place must exist in Art Institute API                 |

---

## HTTP Status Codes

| Code | Meaning            |
| ---- | ------------------ |
| 200  | OK                 |
| 201  | Created            |
| 204  | No Content         |
| 400  | Validation Error   |
| 404  | Resource Not Found |

---

## Author

Developed as a technical assessment project using Django REST Framework.
