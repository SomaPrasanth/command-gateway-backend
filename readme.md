# 🛡️ Command Gateway - Backend API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-blue)
![Status](https://img.shields.io/badge/Status-Deployed-success)

The secure brain behind the Command Gateway. This API handles **Role-Based Access Control (RBAC)**, **Regex Rule Matching**, **Transactional Credits**, and **Approval Workflows**.

## 🚀 Key Features

* **🔐 Secure Authentication:** API Keys are SHA-256 hashed. Keys are never stored in plain text.
* **⚡ Regex Rule Engine:** Blocks dangerous commands (e.g., `rm -rf`) using pattern matching.
* **🧠 Smart Conflict Detection:** Prevents Admins from creating redundant or overlapping rules by analyzing regex logic.
* **🚦 Approval Workflow:** "Risky" commands are paused and stored in the database. Admins must approve them via the dashboard before the user can retry execution.
* **💰 Atomic Transactions:** Credits are deducted *only* if execution succeeds.
* **📜 Audit Logging:** Every action (success, rejection, or pending approval) is permanently recorded with user attribution.

## 🛠️ Tech Stack

* **Framework:** Python (FastAPI)
* **Database:** PostgreSQL (Production) / SQLite (Dev)
* **ORM:** SQLAlchemy
* **Security:** `hashlib` (SHA-256), `secrets`

## ⚙️ Setup & Installation

### 1. Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/command-gateway-backend.git
cd command-gateway-backend
```
### 2. Create Virtual EnvironmentBash
### Windows
```
python -m venv venv
venv\Scripts\activate
```
### Mac/Linux
```
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Configure Environment
 Create a .env file (optional) or set these variables in your cloud provider
 
| Variable | Description |
| :--- | :--- |
| `DATABASE_URL` | Connection string (e.g., `postgresql://user:pass@host/db`). Defaults to local SQLite if empty. |
### 5. Run the Server
```
uvicorn main:app --reload
````
The API will be available at http://127.0.0.1:8000. Visit /docs for the interactive Swagger UI.

## 🧪 Default Users (Seed Data)

When setting up the database, you can seed these default users via the `/seed-db` endpoint:

* **Admin:** `superuser` (Key: `admin-secret-key`)
* **Member:** `johndoe` (Key: `member-secret-key`)

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/commands/execute` | Submit a command. Handles execution, blocking, or queuing for approval. |
| `POST` | `/rules` | (Admin) Add a new regex rule with conflict detection. |
| `GET` | `/audit-logs` | (Admin) View system history with user attribution. |
| `POST` | `/users` | (Admin) Create a new user & generate a one-time API key. |


