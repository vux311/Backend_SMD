# Syllabus Management System (SMD) - Backend ✅

## Description
A RESTful API built with **Flask** following a **Clean Architecture** style for managing university course syllabuses. The backend supports creating syllabuses, defining Course Learning Outcomes (CLOs), managing teaching plans, assessment schemes, rubrics, and an approval workflow with history logging.

---

## Tech Stack 🧰
- **Framework:** Flask
- **Database:** MS SQL Server (accessed via SQLAlchemy + pymssql)
- **Architecture:** Clean Architecture (Controller → Service → Repository → Model)
- **DI Container:** dependency-injector
- **Serialization/Validation:** Marshmallow
- **Documentation:** Swagger UI (Flasgger)

---

## Key Features ✨
- **Master Data Management:** Faculties, Departments, Subjects, Academic Years, Programs, Users, Roles
- **Syllabus Management:** Create / Update syllabus header and general info (time allocation, prerequisites, versioning)
- **Syllabus Components:**
  - **CLOs:** Manage Course Learning Outcomes
  - **Materials:** Manage textbooks and references
  - **Teaching Plan:** Weekly schedule and activities
- **Assessment System:**
  - Define **Schemes** (Progress, Midterm, Final)
  - Define **Components** (Quiz, Lab, Exam)
  - **Rubrics:** Detailed scoring criteria
  - **Mapping:** Map assessment components to CLOs
- **Workflow:** Submit → Approve / Reject process with **WorkflowLog** history
- **Auth (Demo):** Basic auth controller returning a demo token; token decorator available for protecting endpoints

---

## Project Structure (brief)
```
src/
├─ api/                # HTTP controllers, schemas, middleware, swagger
│  ├─ controllers/     # Blueprints for each resource
│  └─ schemas/         # Marshmallow schemas
├─ services/           # Business logic (services)
├─ infrastructure/     # DB models, repositories, DB adapters
│  ├─ models/
│  └─ repositories/
├─ domain/             # Domain models/constants/exceptions
├─ scripts/            # Helper scripts (seed data, etc.)
├─ dependency_container.py  # DI wiring
└─ app.py              # App factory + blueprint registration
```

## Setup & Installation ⚙️

Follow these steps to get the backend running locally.

1. Clone the repository

```bash
git clone https://github.com/vux311/Backend_SMD.git
cd Backend_SMD
```

2. Create a virtual environment and activate it

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r src/requirements.txt
```

4. Environment variables

Create a `.env` file inside the `src/` folder containing at least:

```env
# Flask
SECRET_KEY=your_secret_key

# Database (SQLAlchemy URL)
DATABASE_URI=mssql+pymssql://sa:YourPassword@127.0.0.1:1433/YourDatabase
```

5. Database (MS SQL Server) via Docker (example)

```bash
docker pull mcr.microsoft.com/mssql/server:2025-latest
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=YourPassword" -p 1433:1433 --name sql1 -d mcr.microsoft.com/mssql/server:2025-latest
```

---

## Seeding Data (Important) 🌱

A seed script creates default roles and an example syllabus (Admin, Lecturer, Subject, sample CLOs, materials).

Run from repository root:

```bash
python -m src.scripts.seed_users
```

The script is idempotent and can be re-run safely.

---

## Running the App ▶️

Start the development server:

```bash
python src/app.py
```

- Default port: **9999**
- Swagger UI: **http://localhost:9999/docs**

---

## API Documentation

Interactive API specification is available at the Swagger UI endpoint above. Use it to explore endpoints, request/response schemas, and try sample requests.

---

## Project Notes & Next Steps 💡

- Authentication included in a demo form (dummy tokens). For production, integrate full JWT-based auth and role-based access control.
- Recommended: add automated tests (unit + integration) and CI checks (linting/tests) for PR validation.

---

If you'd like, I can add a CONTRIBUTING guide, CI pipeline, or a small integration test that exercises the workflow (submit → approve/reject).




 







