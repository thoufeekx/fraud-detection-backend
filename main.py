from fastapi import FastAPI
from api.user import router as user_router  # Import the router from api.user

# Create the FastAPI app instance
app = FastAPI()

# Include the user router
app.include_router(user_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
