from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.routes.user import router as user_router
from app.api.v1.routes.donor import router as donor_router
from app.api.v1.routes import user
from app.api.v1.routes import blood_request
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(donor_router, prefix="/api/v1/donors", tags=["Donors"])


app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])



app.include_router(
    blood_request.router,
    prefix="/api/v1/requests",
    tags=["Blood Requests"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)