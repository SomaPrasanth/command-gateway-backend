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
git clone [https://github.com/YOUR_USERNAME/command-gateway-backend.git](https://github.com/YOUR_USERNAME/command-gateway-backend.git)
cd command-gateway-backend
2. Create Virtual EnvironmentBash# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install DependenciesBashpip install -r requirements.txt
4. Configure EnvironmentCreate a .env file (optional) or set these variables in your cloud provider:VariableDescriptionDATABASE_URLConnection string (e.g., postgresql://user:pass@host/db). Defaults to local SQLite if empty.5. Run the ServerBashuvicorn main:app --reload
The API will be available at http://127.0.0.1:8000.Visit /docs for the interactive Swagger UI.🧪 Default Users (Seed Data)When setting up the database, you can seed these default users via the /seed-db endpoint:RoleUsernameAPI Key (for testing)Adminsuperuseradmin-secret-keyMemberjohndoemember-secret-key📡 API Endpoints OverviewMethodEndpointDescriptionPOST/commands/executeSubmit a command. Handles execution, blocking, or queuing for approval.POST/rules(Admin) Add a new regex rule with conflict detection.GET/audit-logs(Admin) View system history with user attribution.POST/users(Admin) Create a new user & generate a one-time API key.GET/approvals(Admin) View pending requests.POST/approvals/{id}/approve(Admin) Approve a specific request.
---

### 2. Frontend Repository (`command-gateway-frontend/README.md`)

```markdown
# 💻 Command Gateway - Visual Terminal

![React](https://img.shields.io/badge/React-18-blue)
![Vite](https://img.shields.io/badge/Vite-Fast-yellow)
![Status](https://img.shields.io/badge/Status-Live-success)

A hacker-style terminal interface for the Command Gateway. It features a responsive UI that adapts based on user roles (Admin vs Member).

## 📸 Screenshots

*(Add your screenshot here)*

## 🌟 Features

* **🕵️ Role-Adaptive UI:**
    * **Members** see a Terminal and Credit Counter.
    * **Admins** get a Control Panel (Rule Manager, Audit Logs, User Management, Approvals).
* **⚡ Real-time Feedback:** Instant success/failure messages for commands.
* **📊 Visual Data:** Color-coded logs (Red for blocks, Green for success, Yellow for pending).
* **📋 Approval Dashboard:** Admins can view pending risky commands and approve them with one click.

## 🛠️ Tech Stack

* **Framework:** React (Vite)
* **Styling:** CSS Modules (Custom Hacker Theme)
* **HTTP Client:** Axios
* **Deployment:** Vercel

## ⚙️ Setup & Installation

### 1. Clone the Repo
```bash
git clone [https://github.com/YOUR_USERNAME/command-gateway-frontend.git](https://github.com/YOUR_USERNAME/command-gateway-frontend.git)
cd command-gateway-frontend
2. Install DependenciesBashnpm install
3. Configure EnvironmentCreate a file named .env in the root folder:Code snippetVITE_API_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
(Change this URL if your backend is deployed on Render/AWS)4. Run Development ServerBashnpm run dev
Open http://localhost:5173 in your browser.🎮 How to UseAuthenticate: Enter your API Key.Demo Admin: admin-secret-keyDemo Member: member-secret-keyRun Commands: Type ls, git status, or rm -rf / to test the rules.Manage Rules (Admin): Use the right-hand panel to add new Regex patterns.Approve Requests: If a command requires approval, the user receives a "Pending" status. Switch to the Admin account to find and approve the request in the "Pending Approvals" section.User Management: Create new users and receive a secure, one-time generated API Key.🔗 Live DemoLink to your Vercel Project
---

### Next Steps for you:
Would you like me to help you create a **`.gitignore`** file for either of these 