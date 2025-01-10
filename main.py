from fastapi import FastAPI
from api.user import router as user_router  # Import the router from api.user

#adding auth_router for jwt authentication
from api.auth import router as auth_router
from api.transactions import router as transactions_router


# Create the FastAPI app instance
app = FastAPI()

# Include the user router
app.include_router(user_router)
# Include auth router
app.include_router(auth_router)

app.include_router(transactions_router)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
