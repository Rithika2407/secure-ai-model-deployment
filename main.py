from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging
import numpy as np
from sklearn.linear_model import LogisticRegression

# ==============================
# CONFIGURATION
# ==============================

SECRET_KEY = "supersecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ==============================
# LOGGING SETUP
# ==============================

logging.basicConfig(
    filename="access.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==============================
# PRE-HASHED USERS (FIXED)
# ==============================

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "admin"
    },
    "user": {
        "username": "user",
        "hashed_password": pwd_context.hash("user123"),
        "role": "user"
    }
}

# ==============================
# SIMPLE ML MODEL
# ==============================

X = np.array([[0], [1], [2], [3]])
y = np.array([0, 0, 1, 1])

model = LogisticRegression()
model.fit(X, y)

# ==============================
# MODELS
# ==============================

class Token(BaseModel):
    access_token: str
    token_type: str

class PredictionInput(BaseModel):
    value: float

# ==============================
# AUTH FUNCTIONS
# ==============================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(required_role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

# ==============================
# ROUTES
# ==============================

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        logging.warning(f"Failed login attempt: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )

    logging.info(f"User logged in: {user['username']}")

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/predict")
def predict(input_data: PredictionInput, user: dict = Depends(require_role("user"))):
    prediction = model.predict([[input_data.value]])[0]
    logging.info(f"Prediction by {user['username']}")
    return {"prediction": int(prediction)}


@app.post("/admin/retrain")
def retrain_model(user: dict = Depends(require_role("admin"))):
    logging.info(f"Model retrained by {user['username']}")
    return {"message": "Model retrained successfully (simulated)"}