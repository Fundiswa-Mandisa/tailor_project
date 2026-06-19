# Tailor Cost Prediction System
### University of Zululand – Group 7
### Django + Scikit-learn Cost Estimation App




## Project Structure

```
tailor_project/
│
├── manage.py
├── requirements.txt
├── db.sqlite3                     # Created after migrations
│
├── tailor_project/                # Django project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── estimator/                     # Main Django application
    ├── __init__.py
    ├── apps.py                    # Loads ML model at startup
    ├── admin.py                   # Django admin registrations
    ├── forms.py                   # Login, Register, Profile, and Estimate forms
    ├── models.py                  # TailorProfile and EstimateHistory models
    ├── views.py                   # Authentication, estimator, history, and profile views
    ├── urls.py                    # Application URL routes
    │
    ├── ml/
    │   ├── __init__.py
    │   ├── predictor.py           # ML model wrapper (load and predict)
    │   ├── fine_tuned_random_forest_regressor.joblib
    │   └── group_7_dataset.csv
    │
    ├── static/
    │   ├── css/
    │   │   ├── style.css          # Main application styles
    │   │   └── auth.css           # Authentication page styles
    │   │
    │   └── js/
    │       └── estimator.js       # AJAX and chat functionality
    │
    ├── templates/estimator/
    │   ├── base.html
    │   ├── login.html             # User login page
    │   ├── register.html          # User registration page
    │   ├── estimator.html         # Main cost estimation interface
    │   ├── history.html           # Estimation history page
    │   └── profile.html           # User profile page
    │
    └── management/commands/
        └── create_admin.py        # Quick admin creation command
```


# Quick Setup Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Run Database Migrations

```bash
python manage.py makemigrations estimator
python manage.py migrate
```

## 3. Create an Admin User

Default credentials:

```bash
python manage.py create_admin
```

Default account:

```text
Email: admin@unizulu.ac.za
Password: admin1234
```

Create a custom administrator account:

```bash
python manage.py create_admin --email yourname@unizulu.ac.za --password yourpassword
```

## 4. Start the Development Server

```bash
python manage.py runserver
```

## 5. Open the Application

Application:

```text
http://127.0.0.1:8000/login/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```



# URL Routes

| URL                     | View              | Description                               |
| ----------------------- | ----------------- | ----------------------------------------- |
| `/login/`               | `login_view`      | User login page using email and password  |
| `/register/`            | `register_view`   | User registration page                    |
| `/logout/`              | `logout_view`     | Logs the user out and redirects to login  |
| `/estimator/`           | `estimator_view`  | Main garment cost estimator               |
| `/api/predict/`         | `predict_ajax`    | AJAX prediction endpoint returning JSON   |
| `/api/chat/`            | `chat_predict`    | Natural language chat prediction endpoint |
| `/history/`             | `history_view`    | Paginated estimation history              |
| `/history/delete/<id>/` | `delete_estimate` | Deletes a selected estimate               |
| `/profile/`             | `profile_view`    | View and update tailor profile            |
| `/admin/`               | Django Admin      | Administrative dashboard                  |



# Model Inputs and Outputs

## Input Fields

The estimation form accepts the following inputs:

| Field       | Type   | Example |
| ----------- | ------ | ------- |
| Garment     | Select | Dress   |
| Fabric_Type | Select | Silk    |
| Fabric_m    | Float  | 2.5     |



## Output Fields

The system generates the following outputs:

| Field             | Description                                |
| ----------------- | ------------------------------------------ |
| Material_Cost_ZAR | Fabric metres × Price per metre            |
| Labour_Cost       | Total Cost − Material Cost − Overhead Cost |
| Overhead_Cost     | 8% of Total Cost                           |
| Total_Cost_ZAR    | Predicted by the Random Forest model       |

---

# Fabric Price Reference

| Fabric Type | Average Price per Metre (ZAR) |
| ----------- | ----------------------------- |
| Cotton      | R90                           |
| Denim       | R114                          |
| Leather     | R275                          |
| Linen       | R140                          |
| Nylon       | R70                           |
| Polyester   | R68                           |
| Silk        | R173                          |
| Wool        | R217                          |

---

# Machine Learning Model

The application uses a **Random Forest Regressor** implemented through a Scikit-learn Pipeline.

### Pipeline Components

* **OneHotEncoder** for:

  * Garment
  * Fabric_Type

* **Numeric Passthrough** for:

  * Fabric_m
  * Price_per_m

### Version Compatibility Handling

If the saved `.joblib` model was trained using a different version of Scikit-learn, the application automatically retrains a new Random Forest model using:

```text
group_7_dataset.csv
```

The newly trained model is then saved as:

```text
fine_tuned_random_forest_regressor_retrained.joblib
```

This retrained model will be used automatically during future application startups.



# System Features

* User Login, Registration, and Logout
* Email-based Authentication
* Tailor Profile Management
* Avatar Initials and User Statistics
* Garment Cost Estimation
* Material Cost Breakdown
* Labour and Overhead Cost Calculation
* Comparable Garment Recommendations
* Estimate History Tracking
* Filtering and Pagination
* Estimate Deletion
* Natural Language Input Support

  * Example: `"silk dress 3m"`
* AJAX-Based Predictions
* No Page Reload Required
* Django Administration Dashboard
* Responsive User Interface
* Mobile-Friendly Navigation

---

# Django Administration

Access the administration dashboard through:

```text
/admin/
```

using your superuser credentials.

## Registered Models

### TailorProfile

Allows administrators to:

* View tailor accounts
* Monitor profile information
* Manage user-related records

### EstimateHistory

Allows administrators to:

* View all garment estimates
* Filter estimate records
* Search historical predictions
* Manage estimate data across all users



# Production Deployment

Before deploying the application to production, complete the following steps:

## 1. Disable Debug Mode

In `settings.py`:

```python
DEBUG = False
```

## 2. Configure a Secure Secret Key

Replace the default secret key with a strong, randomly generated key.

## 3. Configure Allowed Hosts

```python
ALLOWED_HOSTS = ['yourdomain.com']
```

## 4. Collect Static Files

```bash
python manage.py collectstatic
```

## 5. Configure Application Server

Use:

* Gunicorn
* Nginx

for serving the application in production.

## 6. Use PostgreSQL

Replace SQLite with PostgreSQL for improved scalability, reliability, and production readiness.



# Troubleshooting

## Error: No module named 'sklearn'

Install Scikit-learn:

```bash
pip install scikit-learn
```

---

## Model Version Warning

If a model version mismatch is detected, the application automatically retrains the model.

Check the application logs for:

```text
Model retrained.
```



## Migration Errors

Delete the existing database and rerun migrations:

```bash
rm db.sqlite3

python manage.py migrate
```



## Static Files Not Loading

Run:

```bash
python manage.py collectstatic
```

Also verify that the `STATICFILES_DIRS` configuration points to the correct static files directory.

---

# Summary

The Tailor Cost Prediction System is a Django-based web application developed by **University of Zululand Group 7** that combines machine learning and web technologies to estimate garment production costs. The system provides user authentication, profile management, estimation history, natural language input, predictions, and administrative tools while leveraging a Random Forest Regressor for accurate cost estimation.

