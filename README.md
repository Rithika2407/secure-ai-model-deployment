
# Secure AI Model Deployment with Role-Based Access Control (RBAC)

A production-style backend for securely deploying Machine Learning models using FastAPI, JWT authentication, and Role-Based Access Control.

This project demonstrates how to protect ML inference endpoints in real-world deployment scenarios.

---

## Overview

Many AI systems expose model endpoints without proper authentication or authorization.  
This project simulates a secure AI backend where:

- Users can access prediction endpoints
- Admins can retrain models
- All routes are protected using JWT tokens
- Role-based permissions are enforced
- Access logs are recorded

---

## Features

- JWT Authentication
- Role-Based Access Control (Admin / User)
- Secure ML Inference Endpoint
- Protected Admin Route
- Structured Logging
- Swagger API Documentation
- Secure Password Hashing (PBKDF2-SHA256)

---

## Architecture

Client → Login → JWT Token Issued  
Client → Authenticated Request → Role Validation → Model Access  

Protected Endpoints:

- `POST /login` → Generate JWT token
- `POST /predict` → Accessible by User role
- `POST /admin/retrain` → Accessible by Admin role

---

## Tech Stack

- Backend: FastAPI
- Server: Uvicorn
- ML Model: Scikit-learn (Logistic Regression)
- Authentication: OAuth2 + JWT
- Password Hashing: Passlib (PBKDF2-SHA256)
- Language: Python 3.12

---

## Installation and Setup

```bash
git clone https://github.com/Rithika2407/secure-ai-model-deployment.git
cd secure-ai-model-deployment

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
````

Open:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Test Credentials

User:

* username: user
* password: user123
* Access: /predict

Admin:

* username: admin
* password: admin123
* Access: /predict and /admin/retrain

---

## Example Flow

1. Login using `/login`
2. Copy the access token
3. Click "Authorize" in Swagger UI
4. Add: `Bearer <your_token>`
5. Access protected routes

---

## Security Considerations

* Token expiration enforced
* Role validation before route execution
* Secure password hashing
* Logging of access attempts
* Separation of authentication and authorization logic

---

## Future Improvements

* PostgreSQL database integration
* Rate limiting
* Docker containerization
* Cloud deployment (Render / AWS / GCP)
* CI/CD integration


---

Now run:

```bash
git add README.md
git commit -m "Refined professional README"
git push
````
