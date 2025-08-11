# impact-experience-project
# Medical Patient Management System

## Project Overview
A Flask-based medical records management system designed specifically for maternal healthcare in Cambodia, with bilingual support (English/Khmer). The system helps healthcare providers track and manage patient information throughout the pregnancy journey, from prenatal to postnatal care.

### Key Features
- 🌐 Bilingual Interface (English/Khmer)
- 👤 Patient Information Management
- 🏥 Comprehensive Medical Records:
  - ANC (Ante Natal Care)
  - LDR (Labour and Delivery Records)
  - PNC (Post Natal Care)
- 🔒 Secure Authentication System
- 🔍 Patient Search Functionality

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- SQLite3

### Installation Steps
1. Clone the repository:
````bash
git clone <repository-url>
cd iex
````

2. Create and activate a virtual environment:
````bash
python -m venv venv
source venv/bin/activate  # For Mac/Linux
````

3. Install required dependencies:
````bash
pip install -r requirements.txt
````

4. Initialize the database:
````bash
flask init-db
````

5. Start the application:
````bash
flask run
````

## Usage Instructions

1. **Access the Application**
   - Open your browser and navigate to `http://localhost:5000`
   - Register/Login using your credentials

2. **Patient Management**
   - Add new patients with basic information
   - View patient details
   - Search for existing patients

3. **Medical Records**
   - Create and manage ANC records
   - Document labour and delivery information
   - Track post-natal care

## Code Structure

```
iex/
├── flaskr/
│   ├── __init__.py          # Application factory
│   ├── auth.py              # Authentication views
│   ├── diagnosis.py         # Medical records handling
│   ├── patient.py           # Patient management
│   ├── db.py               # Database operations
│   └── templates/
│       ├── auth/           # Authentication templates
│       ├── patient/        # Patient management templates
│       └── base.html       # Base template
├── instance/
│   └── flaskr.sqlite       # SQLite database
└── tests/                  # Test suite
```

### Key Components
- **Authentication Module**: Handles user registration, login, and session management
- **Patient Module**: Manages patient information and records
- **Diagnosis Module**: Handles different types of medical records (ANC, LDR, PNC)
- **Database Layer**: SQLite database with Flask-SQLAlchemy integration

## Code Walkthrough

### 1. Application Core (`flaskr/__init__.py`)
- Initializes the Flask application
- Configures database connection
- Registers blueprints for different modules
- Sets up authentication middleware

### 2. Authentication System (`flaskr/auth.py`)
- Manages user registration and login
- Implements password hashing and verification
- Provides login_required decorator for protected routes
- Handles user session management

### 3. Patient Management (`flaskr/patient.py`)
- CRUD operations for patient records
- Search functionality for patients
- Patient profile management
- Links patients to their medical records

### 4. Medical Records (`flaskr/diagnosis.py`)
- Handles three types of medical records:
  - **ANC (Ante Natal Care)**
    - Tracks pregnancy progress
    - Records vital signs and measurements
    - Manages prenatal appointments
  
  - **LDR (Labour and Delivery)**
    - Documents labour onset and progress
    - Records delivery details
    - Tracks complications and interventions
  
  - **PNC (Post Natal Care)**
    - Monitors post-delivery recovery
    - Tracks infant health metrics
    - Records follow-up appointments

### 5. Templates (`flaskr/templates/`)
- `base.html`: Main template with common layout
- `patient/`: Patient-related views
  - `view_patient.html`: Displays patient information in both English and Khmer
  - Forms for different medical record types
- `auth/`: Authentication-related templates

### 6. Database Schema (`flaskr/db.py`)
- Defines database models and relationships
- Implements database initialization
- Manages database connections and sessions

### Key Implementation Features
- Bilingual support throughout the application
- Role-based access control
- Form validation and sanitization
- Secure password handling
- Audit trails for medical records

### Core Dependencies
- Flask
- Flask-SQLAlchemy
- Werkzeug
- Jinja2
- Click

### Development Dependencies
- pytest
- coverage
- python-dotenv

### System Requirements
- Python 3.8+
- SQLite3
- Modern web browser with JavaScript enabled

## Security Notes
- The system implements user authentication
- Medical records are protected but viewable by all authenticated users
- Password hashing is implemented for user security

---

For support or questions, please create an issue or contact the development team.