# SpotiQue - Smart Queue Management System

SpotiQue is a comprehensive queue management system designed to streamline customer flow, improve service efficiency, and provide real-time queue tracking. This project was developed for the Group 114 ITECH report.

## 🌟 Features by Role

**Managers**
* Access to a comprehensive analytics dashboard to track queue statistics and operator performance.
* Manage operator accounts and system configurations.
* Monitor live queue status and historical data.

**Operators**
* Dedicated dashboard to manage assigned queues.
* Call the next guest, mark guests as served, or handle no-shows.
* Seamless interface for updating queue status in real-time.

**Guests/Customers**
* Join queues digitally without waiting in physical lines.
* Receive real-time queue status updates and notifications via WhatsApp.

## 🛠️ Tech Stack

* **Frontend:** Bootstrap, Vanilla JavaScript, HTML5/CSS3
* **Backend:** Python, Django
* **Database:** PostgreSQL (SQLite supported for local development)
* **Integrations:** Twilio API (WhatsApp Sandbox for notifications)

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd spotique

```

### 2. Set up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Environment Variables

Create a `.env` file in the root directory (alongside `manage.py`) and add your configuration. *Note: For local testing, you can use SQLite by omitting the database URL, but PostgreSQL is recommended to mirror production.*

```env
# Twilio Credentials (Required for WhatsApp notifications)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token

# Database Configuration (If using PostgreSQL locally)
DATABASE_URL=postgres://user:password@localhost:5432/spotique_db

```

*Note on Twilio:* The project uses the Twilio WhatsApp Sandbox. For notifications to work during development, target phone numbers must be manually verified in your Twilio Console.

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate

```

### 6. Populate Fake Data (Optional but Recommended)

The project includes a custom management command using the `faker` library to generate dummy queues, operators, and guests for testing analytics.

```bash
python manage.py generate_fake_data

```

### 7. Run the Development Server

```bash
python manage.py runserver

```

Visit `http://127.0.0.1:8000` in your browser.

---

## 🧪 Testing the Application

Automated unit testing has been implemented using Django's `TestCase` framework, covering models, forms, views, and role-based decorators. To run the tests:

```bash
python manage.py test

```

### Test Credentials

If you have populated the database using `generate_fake_data`, you can use the following pre-configured accounts to explore the different dashboards:

| Role | Username | Password |
| --- | --- | --- |
| **Manager** | `xfernandez` | `defaultpassword` |
| **Manager** | `drodriguez` | `defaultpassword` |
| **Manager** | `allenmarvin` | `defaultpassword` |
| **Operator** | `michaelmckenzie` | `defaultpassword` |
| **Operator** | `kenneth95` | `defaultpassword` |

*(Note: It is recommended to log in as `xfernandez`, as most of the fake data is generated under this user).*

---

## 🏗️ System Architecture

SpotiQue follows a standard three-tier architecture:

1. **Presentation Layer (Frontend):** Role-based UI built with Bootstrap and Vanilla JS. Uses Django templates for dynamic rendering.
2. **Application Layer (Backend):** Django handles user authentication, business logic, queue algorithms, and API communications. Access is strictly controlled via custom decorators (`@manager_required`, `@operator_required`).
3. **Data Layer (Database):** PostgreSQL stores normalized data utilizing relationships between `Users`, `Customers`, `Managers`, `Operators`, `Queues`, `Categories`, and `Guests`.

---

## 👥 Contributors (Group 114)

* **Kanak Sengar** - Frontend Architecture, UI/UX Design, JavaScript Interactivity
* **Majd Alkawaas** - Backend Development, Authentication, API Integrations, CI/CD Setup
* **Rashi** - Backend Development, Database Schema, Twilio Integration, Test Engineering
