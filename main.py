from fastapi import FastAPI
from api.user import router as user_router  # Import the router from api.user

#adding auth_router for jwt authentication
from api.auth import router as auth_router
from api.transactions import router as transactions_router


# fast api middleware
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI app instance
app = FastAPI()

# Allow origins for your frontend
origins = [
    "http://localhost:5173",  # Vite development server
    "http://127.0.0.1:5173",  # Alternate localhost address
    "http://localhost:8080",  # For Docker (if applicable)
]


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the user router
app.include_router(user_router)
# Include auth router
app.include_router(auth_router)

app.include_router(transactions_router)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
