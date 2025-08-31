# 🏥 Advanced Medical Diagnosis System

An interactive Streamlit-based medical diagnosis support tool with modern UI, doctor authentication, signup/approval workflow, patient management, ML model inference, comprehensive statistics dashboards, and email notifications.

## ✨ Key Features

### 🔐 **Authentication & Security**

- **Doctor Registration**: Secure signup with email verification and admin approval workflow
- **HMAC-signed Tokens**: Tamper-proof approval/rejection links with secure token validation
- **Password Protection**: SHA-256 hashed passwords with secure login system
- **Per-Doctor Isolation**: Each doctor can only access their own patients

### 🎯 **Medical Diagnosis**

- **AI-Powered Predictions**: Pre-trained scikit-learn breast cancer classification model
- **Real-time Analysis**: Instant diagnosis with confidence scores and probability distributions
- **Feature Analysis**: Comprehensive feature input with automatic scaling and normalization
- **Treatment Planning**: Integrated treatment plan creation and progress tracking

### 📊 **Advanced Analytics Dashboard**

- **Global Trends**: Date-based patient statistics and prediction trends
- **Distribution Analysis**: Visual prediction distribution with pie charts and tables
- **Feature Insights**: Top feature averages and comparative analysis
- **Patient-Specific Analytics**: Detailed per-patient metrics and timeline visualization
- **Data Quality Monitoring**: Automated checks for missing data and integrity issues

### 💾 **Data Management**

- **SQLite Database**: Robust local data persistence for doctors, patients, and applications
- **Real-time Sync**: Automatic synchronization between UI and database
- **Progress Tracking**: Detailed treatment progress logs with timestamps and status updates
- **Export Capabilities**: Patient data export and management features

### 🎨 **Modern User Interface**

- **Dark Theme**: Professional black and white design with 3D shadow effects
- **Responsive Design**: Mobile-friendly interface with adaptive layouts
- **Custom Styling**: Hand-crafted CSS with neumorphism effects and smooth animations
- **Accessibility**: High contrast text (white on dark) for optimal readability
- **Interactive Elements**: Hover effects, smooth transitions, and intuitive navigation

## 🛠️ Technology Stack

- **Frontend**: Streamlit (UI & state management)
- **Machine Learning**: scikit-learn (model + scaler), joblib (model persistence)
- **Database**: SQLite (doctors, pending applications, patients)
- **Data Processing**: NumPy, Pandas (data handling)
- **Visualization**: Matplotlib (charts and analytics)
- **Email**: SMTP (automated notifications)
- **Security**: HMAC token signing, SHA-256 password hashing

## Folder Structure

```text
MedicalDiagnosis/
  advanced_medical_ui_fixed.py    # Main Streamlit application (UI, auth, DB, ML, analytics)
  Medical.ipynb                   # Notebook (exploration / experimentation)
  Dataset/                        # (Optional) Source data used for training/evaluation
    ...                           # Your dataset files (not required at runtime if model is present)
  breast_cancer_model.pkl         # Trained scikit-learn classifier (runtime dependency)
  scaler.pkl                      # Feature scaler paired with the model
  medical_app.db                  # SQLite database (auto-created at first run)
  .streamlit/
    secrets.toml                  # Private secrets (SMTP, keys) – DO NOT COMMIT
  .gitignore                      # Ignore rules (db, models, secrets, etc.)
  README.md                       # Project documentation
```

Notes:

- `medical_app.db` and `secrets.toml` are environment / runtime artifacts and should remain untracked.
- If the model or scaler is large or proprietary, keep them out of version control and document retrieval steps instead.
- The `Dataset/` folder is optional for running the app; it is only needed if you plan to retrain or experiment.

## Prerequisites

- Python 3.9+ recommended
- Model files: `breast_cancer_model.pkl` and `scaler.pkl` present in the folder

## Installation

```bash
pip install streamlit scikit-learn joblib numpy pandas matplotlib
```

(Optional: create a virtual environment first.)

host = "smtp.gmail.com"
port = 587
user = "your_email@example.com"
password = "your_app_password"  # Use an App Password (e.g., Gmail 2FA)
use_tls = true
use_ssl = false
from = "no-reply@example.com"
to = "admin@example.com"

admin_email = "admin@example.com"
app_base_url = "http://localhost:8501"   # Adjust if deploying
APP_SECRET_KEY = "replace-with-a-long-random-string"
 
## Secrets Configuration

## 📁 Project Structure

```text
MedicalDiagnosis/
├── advanced_medical_ui_fixed.py    # 🚀 Main Streamlit application
├── Medical.ipynb                   # 📓 Jupyter notebook for ML experimentation
├── Dataset/                        # 📊 Training data (optional for runtime)
│   └── data.csv                    # Original breast cancer dataset
├── breast_cancer_model.pkl         # 🤖 Trained ML classifier
├── scaler.pkl                      # 📏 Feature normalization scaler
├── medical_app.db                  # 🗄️ SQLite database (auto-generated)
├── .streamlit/
│   └── secrets.toml                # 🔐 SMTP & security config (DO NOT COMMIT)
├── .gitignore                      # 🚫 Version control exclusions
└── README.md                       # 📖 This documentation
```

## 🎨 User Interface Highlights

### **Modern Dark Theme Design**
- **Professional Aesthetic**: Sleek black and white color scheme with subtle gradients
- **3D Effects**: Neumorphism-inspired shadows and depth for interactive elements
- **High Contrast**: White text on dark backgrounds for excellent readability
- **Responsive Layout**: Adapts beautifully to different screen sizes

### **Interactive Elements**
- **Input Fields**: Dark-themed input boxes with white text and focus effects
- **Dropdown Menus**: Purple gradient selectboxes with white text options
- **Buttons**: 3D-styled buttons with hover animations and click feedback
- **Cards**: Elevated card components with smooth shadow transitions

### **Accessibility Features**
- **Optimal Contrast**: Meets WCAG guidelines for text visibility
- **Alert Messages**: White text on colored backgrounds (error, success, warning)
- **Navigation**: Clear sidebar with white text and intuitive icons
- **Form Design**: Logical field grouping with proper spacing

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** (recommended)
- **Required Model Files**: `breast_cancer_model.pkl` and `scaler.pkl`

### Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd MedicalDiagnosis
   ```

2. **Install dependencies**:

   ```bash
   pip install streamlit scikit-learn joblib numpy pandas matplotlib
   ```

3. **Configure email settings** (create `.streamlit/secrets.toml`):

   ```toml
   [smtp]
   host = "smtp.gmail.com"
   port = 587
   user = "your_email@example.com"
   password = "your_app_password"  # Use App Password for Gmail 2FA
   use_tls = true
   use_ssl = false
   from = "no-reply@example.com"
   to = "admin@example.com"

   admin_email = "admin@example.com"
   app_base_url = "http://localhost:8501"   # Update for deployment
   APP_SECRET_KEY = "your-super-secret-key-here"
   ```

4. **Run the application**:

   ```bash
   streamlit run advanced_medical_ui_fixed.py
   ```

5. **Access the app**: Navigate to `http://localhost:8501` in your browser

## 🔧 Configuration

### Environment Variables (Alternative to secrets.toml)

You can also use environment variables instead of or alongside the secrets file:

- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`
- `APP_SECRET_KEY` (for HMAC token signing)
- `APP_BASE_URL` (deployment URL for approval links)

## 🚦 Application Workflow

### 1. **Doctor Registration Process**

- New doctors complete the registration form with professional details
- Application is stored in the database with pending status
- Admin receives an email with secure approve/reject links
- HMAC-signed tokens ensure link integrity and prevent tampering

### 2. **Admin Approval System**

- Admin clicks approval link from email
- System verifies token authenticity
- Approved doctors are added to the active database
- Automatic email notifications sent to applicants
- Rejected applications are logged and cleaned up

### 3. **Secure Login & Session Management**

- Doctors log in with approved credentials
- SHA-256 password verification
- Patient data automatically loaded into session
- Per-doctor data isolation enforced

### 4. **Medical Diagnosis Pipeline**

- Input patient demographic and clinical features
- Real-time ML model inference with confidence scores
- Results stored with complete audit trail
- Treatment plans integrated with diagnosis

### 5. **Analytics & Patient Management**

- Comprehensive statistics dashboard with trends
- Patient-specific analytics and progress tracking
- Data quality monitoring and validation
- Treatment plan updates with timeline visualization

## 🗄️ Database Schema

### SQLite Database: `medical_app.db`

The application uses three main tables for data persistence:

#### **Tables Overview**

| Table | Purpose | Key Features |
|-------|---------|--------------|
| `doctors` | Approved medical professionals | Username, hashed passwords, specializations |
| `pending_applications` | Doctor registration queue | Temporary storage until approval/rejection |
| `patients` | Patient records per doctor | Demographics, features, predictions, treatment plans |

#### **Detailed Schema**

**`doctors` Table:**
```sql
- username (TEXT PRIMARY KEY): Unique login identifier
- password (TEXT): SHA-256 hashed password
- name (TEXT): Doctor's full name
- email (TEXT): Contact email address
- specialization (TEXT): Medical specialization
- created_at (TEXT): Account creation timestamp
```

**`pending_applications` Table:**
```sql
- application_id (TEXT PRIMARY KEY): Unique application identifier
- username (TEXT): Requested username
- name (TEXT): Applicant's full name
- email (TEXT): Contact email
- specialization (TEXT): Medical specialization
- password (TEXT): Pre-hashed password (temporary)
- created_at (TEXT): Application submission timestamp
```

**`patients` Table:**
```sql
- patient_id (TEXT PRIMARY KEY): Unique patient identifier
- doctor_username (TEXT): Associated doctor
- name (TEXT): Patient name
- age (INTEGER): Patient age
- gender (TEXT): Patient gender
- diagnosis (TEXT): Clinical diagnosis
- prediction (TEXT): ML model prediction
- confidence (REAL): Prediction confidence score
- created_at (TEXT): Record creation timestamp
- features_json (TEXT): JSON-encoded feature vector
- proba_json (TEXT): JSON-encoded probability array
- treatment_plan (TEXT): Treatment recommendations
- progress_json (TEXT): JSON-encoded progress updates
```

## 🔐 Security Considerations

### **Current Security Measures**
- **Token-based Approval**: HMAC-SHA256 signed tokens for approval links
- **Password Hashing**: SHA-256 password storage (upgradeable to bcrypt/argon2)
- **Session Management**: Streamlit-native session isolation
- **Data Isolation**: Per-doctor patient access control

### **Production Recommendations**
- **Strong Secret Keys**: Replace default `APP_SECRET_KEY` with cryptographically secure random string
- **HTTPS Deployment**: Use reverse proxy (nginx, Caddy) with TLS certificates
- **App Passwords**: Use provider-specific app passwords for SMTP (not account passwords)
- **Environment Isolation**: Keep secrets in environment variables or secure vaults
- **Regular Backups**: Implement automated database backup strategies

## 🚀 Future Enhancement Ideas

### **Administrative Features**
- **In-app Admin Dashboard**: Web-based approval interface instead of email links
- **Role-based Access Control**: Separate admin and doctor permissions
- **Audit Logging**: Track all user actions and system events
- **Bulk Operations**: Mass approve/reject applications

### **Medical Features**
- **Model Versioning**: Track and compare different ML model versions
- **Confidence Calibration**: Improve prediction reliability scoring
- **Multi-disease Support**: Extend beyond breast cancer diagnosis
- **Clinical Decision Support**: Integration with medical guidelines

### **Data & Analytics**
- **Advanced Analytics**: Predictive trends and population health insights
- **Data Export/Import**: CSV, JSON, FHIR format support
- **Real-time Dashboards**: Live monitoring of system usage
- **Comparative Studies**: Cross-doctor performance analysis

### **Security & Authentication**
- **Multi-factor Authentication**: SMS, TOTP, hardware tokens
- **Single Sign-On (SSO)**: Integration with hospital systems
- **API Authentication**: JWT tokens for external integrations
- **Advanced Encryption**: End-to-end encryption for sensitive data

## 🛠️ Troubleshooting Guide

| **Issue** | **Likely Cause** | **Solution** |
|-----------|------------------|-------------|
| 📧 Email not sent | Missing/invalid SMTP configuration | Verify `.streamlit/secrets.toml` SMTP settings |
| 🔗 Approval link invalid | Token mismatch or expired URL | Check `app_base_url` matches deployment URL |
| 📊 Empty statistics page | No patient data or missing fields | Complete at least one diagnosis to populate data |
| 🔐 Login fails after approval | Doctor record not created | Check `doctors` table in `medical_app.db` |
| 🚫 Model loading error | Missing pickle files | Ensure `breast_cancer_model.pkl` and `scaler.pkl` exist |
| 💾 Database connection error | File permissions or corruption | Check write permissions and database integrity |

### **Debug Commands**

```bash
# Check database tables
sqlite3 medical_app.db ".tables"

# View doctor accounts
sqlite3 medical_app.db "SELECT username, name, specialization FROM doctors;"

# Check pending applications
sqlite3 medical_app.db "SELECT application_id, name, email FROM pending_applications;"

# Test SMTP configuration
python -c "import smtplib; print('SMTP modules loaded successfully')"
```

## 🏗️ Architecture Overview

### **System Components**

The application follows a modular architecture with clear separation of concerns:

| **Component** | **Responsibility** | **Key Functions** |
|---------------|-------------------|------------------|
| **Authentication** | User management & security | `authenticate_user()`, `_sign_token()`, `_verify_token()` |
| **Database** | Data persistence & retrieval | `init_db()`, `db_upsert_patient()`, `db_store_pending()` |
| **ML Pipeline** | Model inference & predictions | Feature scaling, classification, confidence scoring |
| **Email System** | Notifications & approvals | `send_signup_email()`, `send_generic_email()` |
| **Analytics** | Statistics & visualizations | Trend analysis, distribution charts, quality checks |
| **UI/UX** | User interface & theming | Custom CSS, responsive design, accessibility features |

## 📈 Performance & Scalability

### **Current Capabilities**
- **Response Time**: Sub-second model inference for individual predictions
- **Concurrent Users**: Supports multiple doctors with session isolation
- **Database**: SQLite handles hundreds of patient records efficiently
- **Email Processing**: Asynchronous SMTP for non-blocking notifications

### **Scaling Recommendations**
- **Database**: Migrate to PostgreSQL for production workloads
- **Authentication**: Implement Redis-based session management
- **Model Serving**: Deploy models via REST API for microservices architecture
- **Frontend**: Consider React/Vue.js for more complex UI requirements

## 🎯 Getting Started Checklist

- [ ] **Clone repository** and navigate to project directory
- [ ] **Install dependencies** via pip (consider using virtual environment)
- [ ] **Configure SMTP settings** in `.streamlit/secrets.toml`
- [ ] **Verify model files** (`breast_cancer_model.pkl`, `scaler.pkl`) are present
- [ ] **Run the application** with `streamlit run advanced_medical_ui_fixed.py`
- [ ] **Test registration flow** by creating a doctor account
- [ ] **Complete first diagnosis** to populate analytics dashboard
- [ ] **Review statistics page** to ensure data pipeline is working

## ⚠️ Important Disclaimers
### **Medical Use Disclaimer**

⚠️ **NOT FOR CLINICAL USE**: This application is for educational and demonstration purposes only. It is NOT a certified medical device and should NEVER be used for actual medical diagnosis or treatment decisions.

### **Professional Responsibility**

🏥 **Always Consult Qualified Professionals**: Any medical decisions must be made by licensed healthcare providers with appropriate training, certification, and access to complete patient information.

---

## 📄 License

**Created with passion by Soffar** 🚀  
*Aspiring AI Engineer at Arab Academy for Science, Technology & Maritime Transport*

This project is released under the **MIT License**. You are free to use, modify, and distribute this software for any purpose.

---

⭐ **If this project helped you, please consider giving it a star!** ⭐
4. Admin clicks a link (the same Streamlit app URL with query params). On load, `main()` detects the params, verifies the HMAC, then either:
   - Accept: moves applicant into `doctors` table and emails the applicant.
   - Reject: just emails the applicant. In both cases the pending record is deleted.
5. Approved doctor logs in; password hash is checked against stored SHA‑256 digest.
6. Post-login sidebar exposes navigation. Selecting “New Diagnosis” runs the ML inference pipeline and persists a patient entry.
7. “Statistics” and “Patient Management” read from in-memory `st.session_state.patients_data` (hydrated from DB at login) and provide analytics & editing. When patient data changes (e.g., new diagnosis), `db_upsert_patient()` keeps SQLite in sync.

### Core Modules (Single File Implementation)

All logic currently resides in `advanced_medical_ui_fixed.py`. Conceptually it can be split into layers:

| Layer | Responsibility | Representative Functions |
|-------|----------------|--------------------------|
| Config / Secrets | Retrieve SMTP + app key | `_get_secret_key()`, environment + Streamlit secrets access |
| Security | HMAC signing, password hashing | `_sign_token()`, `_verify_token()`, SHA‑256 usage |
| Persistence (DB) | CRUD for doctors, pending apps, patients | `init_db()`, `db_insert_doctor()`, `db_store_pending()`, `db_upsert_patient()` |
| Email | Outbound notifications | `send_signup_email()`, `send_generic_email()` |
| Auth | Login + session toggle | `authenticate_user()`, `login_page()` |
| Patient Logic | Save / load / enrich patient data | `save_patient_data()`, `load_doctor_patients_into_session()` |
| ML Inference | Scale inputs, predict, produce probabilities | (Inside diagnosis form handler) |
| Analytics | Aggregate, visualize, quality checks | Statistics page block (`Global Trends`, `Feature Averages`, etc.) |
| UI / Navigation | Routing via session state, theming | `main()`, sidebar buttons, custom CSS |

### Database Schema Details

`doctors`

| Column | Type | Notes |
|--------|------|------|
| username | TEXT PRIMARY KEY | Unique handle used for login |
| password | TEXT | SHA‑256 hex digest (improve later) |
| name | TEXT | Doctor full name |
| email | TEXT | Contact / notification address |
| specialization | TEXT | Displayed in sidebar |
| created_at | TEXT | ISO timestamp insertion time |

`pending_applications`

| Column | Type | Notes |
|--------|------|------|
| application_id | TEXT PRIMARY KEY | Random ID used in approval links |
| username | TEXT | Requested username |
| name | TEXT | Applicant name |
| email | TEXT | Applicant email |
| specialization | TEXT | Requested specialization |
| password | TEXT | SHA‑256 hash stored temporarily until approval |
| created_at | TEXT | Submission timestamp |

`patients`

| Column | Type | Notes |
|--------|------|------|
| patient_id | TEXT PRIMARY KEY | Generated ID (ensure uniqueness) |
| doctor_username | TEXT | Foreign-like reference (no FK constraint) |
| name | TEXT | Patient name |
| age | INTEGER | Age at diagnosis |
| gender | TEXT | Gender string |
| diagnosis | TEXT | Legacy / display diagnosis (mirrors prediction) |
| prediction | TEXT | Model output label (e.g., Malignant/Benign) |
| confidence | REAL | Probability associated with predicted class |
| created_at | TEXT | Timestamp of record creation |
| features_json | TEXT | JSON-serialized original feature vector dict |
| proba_json | TEXT | JSON-serialized list of class probabilities |
| treatment_plan | TEXT | Free-form plan text |
| progress_json | TEXT | JSON array of progress entries `{date, note, status}` |

### Data Objects (In-Memory Examples)

Doctor (after approval):

```json
{
  "username": "drsmith",
  "password": "<sha256-hex>",
  "name": "Dr. Anna Smith",
  "email": "anna@example.com",
  "specialization": "Oncology",
  "created_at": "2025-08-21T10:34:22"
}
```

Pending Application:

```json
{
  "application_id": "app_834bfd...",
  "username": "drnew",
  "name": "Dr. New User",
  "email": "new@example.com",
  "specialization": "Radiology",
  "password": "<sha256-hex>",
  "created_at": "2025-08-21T09:10:11"
}
```

Patient Record:

```json
{
  "name": "Jane Doe",
  "age": 52,
  "gender": "Female",
  "diagnosis": "Malignant",
  "prediction": "Malignant",
  "confidence": 0.9473,
  "date": "2025-08-22 14:55:03",
  "features": {"mean_radius": 14.2, "mean_texture": 17.5, "...": 0.123},
  "proba": [0.0527, 0.9473],
  "treatment_plan": "Start chemo cycle A...",
  "progress": [
    {"date": "2025-08-22 15:10", "note": "Baseline established", "status": "Planned"}
  ]
}
```

### Security Mechanisms Explained

1. Password Hashing: Plain text password is hashed with SHA‑256 on signup and compared on login. (Recommendation: migrate to `bcrypt` / `argon2` for salted adaptive hashing.)
2. Approval Links: A token = HMAC_SHA256(app_secret, application_id + action). When the link is clicked, the app recomputes and verifies equality to prevent tampering.
3. Query Parameter Clearing: After processing an approval, `st.query_params.clear()` removes sensitive tokens from the visible URL.
4. Session State: Streamlit runs per-user sessions; sensitive material (like hashes) is not re-sent to browser except through derived UI.
5. Potential Hardening (Not yet implemented): Rate limiting, token expiry, CSRF-style double-submit protections if POST endpoints are added, and stricter password policies.

### Model Inference Pipeline

1. User inputs feature values on the diagnosis form.
2. Features are assembled into a numeric vector (order must match training order of the scaler/model).
3. Scaler (`scaler.pkl`) transforms the raw vector for normalization/standardization.
4. Classifier (`breast_cancer_model.pkl`) predicts class probabilities.
5. Predicted class label + probability mapped to human-readable diagnosis and stored in patient record.
6. Raw feature dict and probability array persisted for later analytics and reproducibility.

### Statistics Page Internals

Sections:

- Global Trends: Aggregates counts over dates (extracted from patient timestamps) and displays a bar chart.
- Prediction Distribution: Value counts for `prediction`; pie + table.
- Feature Averages: Calculates mean for each numeric feature, sorts, and shows top 10 (ensures new features do not break layout).
- Patient-Specific Analytics: Select box loads a single patient; metrics + plan editing & progress timeline.
- Feature Comparison: Bar comparison of selected patient’s first N features vs population average.
- Data Quality Checks: Scans for missing `prediction` / `features` keys to help diagnose ingestion issues.

### Key Functions (Annotated)

| Function | Role | Notes |
|----------|------|------|
| `main()` | Entry point & router | Processes approval params before rendering login or pages |
| `send_signup_email()` | Initiate approval flow | Builds signed links and emails admin |
| `_sign_token()` / `_verify_token()` | HMAC signing | Ensures accept/reject links cannot be forged |
| `db_upsert_patient()` | Persistence | Uses `ON CONFLICT(patient_id)` to atomically insert/update |
| `load_doctor_patients_into_session()` | Hydration | Called after login to fill `st.session_state.patients_data` |
| `save_patient_data()` | In-memory + DB sync | Wraps session update & safe DB write |
| `authenticate_user()` | Login | Compares stored hash with SHA‑256 of user input |

### Session State Keys

| Key | Purpose |
|-----|---------|
| `logged_in` | Boolean flag controlling main view |
| `username` | Current doctor username |
| `current_doctor` | Doctor profile dict |
| `patients_data` | Dict of patient_id -> patient record |
| `page` | Current navigation target |
| `show_signup` | Toggles signup vs login display |

### Adding a New Feature (Example: Export Patients to CSV)

1. Add a button in the sidebar or Patient Management page.
2. When clicked, convert `st.session_state.patients_data` to a DataFrame.
3. Use `st.download_button` with `to_csv(index=False)` bytes.
4. (Optional) Log export action in a future `audit_logs` table.

### Deployment Notes

- For public deployment use: `streamlit run advanced_medical_ui_fixed.py --server.address=0.0.0.0 --server.port=8501` behind a reverse proxy (nginx, Caddy) with TLS.
- Update `app_base_url` in secrets to the public HTTPS URL so approval links are valid externally.
- Regularly backup `medical_app.db` (volume mount if using containers).

### Scaling Considerations

| Aspect | Current Approach | Scaling Path |
|--------|------------------|-------------|
| State | In-memory per session + SQLite | Migrate to server-side cache / API backend |
| DB | Single SQLite file | Move to PostgreSQL (SQLAlchemy ORM) |
| Auth | Basic username/password | Add OAuth / SSO; password resets; MFA |
| Email | Direct SMTP | Use transactional service (SendGrid, SES) |
| Model | Single file | Model registry + A/B testing |

### Known Limitations

- No token expiry for approval links.
- No password reset or lockout mechanisms.
- Patient IDs rely on generation logic not shown here—collision risk minimal but not namespaced per doctor.
- Editing treatment plan/progress updates DB only when patient saved through functions that call `db_upsert_patient()`; inline edits might need an explicit save button (future enhancement).

### Contributing

1. Fork repo / create a feature branch.
2. Add or modify code (keep functions cohesive; consider refactoring into modules if size grows).
3. Run local tests / manual Streamlit run.
4. Update README sections impacted by change.
5. Submit Pull Request with concise description & screenshots (if UI changes).


 
## Disclaimer

This project is for educational/demo purposes and is NOT a certified medical device. Always consult qualified professionals for clinical decisions.


## License

"Crafted with curiosity by **Soffar**, an aspiring AI engineer at the College of AAST 🤖✨"

You are free to use, modify, and share this project under the MIT License (feel free to swap if you prefer another). If you keep a credit note, a small shout‑out to Soffar is appreciated but not required.

### MIT License (Template)

Copyright (c) 2025 Soffar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

If you adopt a different license later, replace this section accordingly.
