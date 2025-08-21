# MedicalDiagnosis Application

An interactive Streamlit-based medical diagnosis support tool with doctor authentication, signup/approval workflow, patient management, model inference, statistics dashboards, and email notifications.

## Features
- Doctor signup & email notification to admin (SMTP) with secure approval / rejection links
- HMAC-signed approval tokens; activation inserts doctor into SQLite DB
- Secure login (hashed passwords) and per‑doctor patient isolation
- Patient diagnosis form feeding a pre-trained scikit-learn breast cancer model (loaded via joblib)
- Automatic persistence of patients, treatment plans, and progress logs (SQLite)
- Statistics page: global trends, prediction distribution, feature averages, per‑patient analytics, treatment timeline
- Editable treatment plans + progress tracking
- Responsive UI with custom CSS (3D card effects & themed components)

## Technology Stack
- Streamlit (UI & state management)
- scikit-learn (model + scaler)
- joblib (model persistence)
- SQLite (doctors, pending applications, patients)
- NumPy / Pandas (data handling)
- Matplotlib (charts)
- SMTP (email notifications)

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

Create `MedicalDiagnosis/.streamlit/secrets.toml`:

```toml
[smtp]
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
```

## Running the App

From the `MedicalDiagnosis` directory:

```bash
streamlit run advanced_medical_ui_fixed.py
```

## Workflow Summary

1. Doctor applies via signup form → pending application stored → admin email sent with Approve / Reject links.
2. Admin clicks link → token verified → doctor auto-added to DB → applicant notified.
3. Doctor logs in → their patients (from SQLite) are loaded.
4. Doctor runs a diagnosis → model inference → patient record persisted with features, probabilities, plan.
5. Statistics page aggregates data (per doctor scope) + allows per-patient drill‑down and treatment progress updates.

## Environment Variables (Optional Overrides)

- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`
- `APP_SECRET_KEY` (if not in secrets)
- `APP_BASE_URL` (deployment URL for action links)

## Data Persistence

SQLite file: `medical_app.db`

Tables:

- `doctors`: approved accounts
- `pending_applications`: awaiting approval
- `patients`: per‑doctor patient records

## Security Notes

- Replace `APP_SECRET_KEY` with a strong secret in production.
- Use app passwords / provider-specific credentials for SMTP.
- Consider upgrading password hashing to bcrypt/argon2 (currently SHA‑256).
- Add HTTPS termination in front (reverse proxy) for deployment.

## Extensibility Ideas

- Admin in-app dashboard for approvals
- Role-based access (admin vs doctor)
- Audit logging of actions
- Model versioning & confidence calibration
- Export / import patient data
- Multi-factor authentication

## Troubleshooting

| Issue | Cause | Action |
|-------|-------|--------|
| Email not sent | Missing/invalid SMTP secrets | Verify `secrets.toml` values |
| Approval link invalid | Stale token or base URL mismatch | Confirm `app_base_url` matches deployed URL |
| Empty statistics | No patients or missing `prediction`/`features` fields | Run new diagnosis to populate |
| Login fails after approval | Doctor not inserted | Check logs & DB (`doctors` table) |

## Architecture & Code Walkthrough

### High-Level Flow
 
1. Visitor lands on the app (Streamlit session starts; `main()` initializes session state + processes any approval/rejection query params first).
2. Doctor either logs in or clicks a toggle to open the signup form.
3. Signup submission:
   - Generates an `application_id`.
   - Stores pending record in `pending_applications` (SQLite).
   - Creates two HMAC-signed action links (accept / reject) embedding `app_id`, `action`, and `token`.
   - Sends an email to the admin with those links.
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
